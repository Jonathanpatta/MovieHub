from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.contrib.admin.models import LogEntry,ADDITION,DELETION,CHANGE
from django.contrib.auth.decorators import login_required

from .models import Movie,UserProfile



class Movie_detail_view(DetailView):
    model = Movie
    fields = ['title','description','directed_by','imdb_rating','rotten_tomatoes_rating','length_in_mins','release_date']
    
    def get(self,request,*args,**kwargs):
        movie = self.get_object()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=1,
            object_id=movie.id,
            object_repr=request.user.username,
            action_flag=0)
        user = UserProfile.objects.get(id=request.user.id)
        user.history.add(movie)
        return render(request,'main/Movie_detail.html',{'movie':movie})

class Movie_create_view(LoginRequiredMixin,CreateView):
    model = Movie
    fields = ['title','description','directed_by','imdb_rating','rotten_tomatoes_rating','length_in_mins','release_date','cover']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class Movie_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    fields = ['title','description','directed_by','imdb_rating','rotten_tomatoes_rating','length_in_mins','release_date','cover']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.created_by:
            return True
        return False


class Movie_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    success_url = '/'

    def test_func(self):
        movie = self.get_object()
        if self.request.user == movie.created_by:
            return True
        return False



def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"movies":Movie.objects.all})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"{username} account created!")
            login(request, user)
            return redirect("main:homepage")
          
        else:
            for msg in form.error_messages:
                messages.error(request,f"{msg}:{form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request,"logged out!")
    return redirect("main:homepage")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})



def movie_details(request,pk):
    #movie = Movie.objects.get(id=pk)
    movie = get_object_or_404(Movie,pk=pk)
    if movie is not None:
        return HttpResponse(Movie_detail_view.as_view())
    messages.info(request,"movie does not exist")
    return redirect("main:homepage")


@login_required
def account(request):
    viewed = LogEntry.objects.filter(action_flag=0).filter(user=request.user)
    viewed_movies=[]
    for le in viewed:
        if le.content_type.name == 'movie':
            viewed_movies.append(le.get_edited_object())
    changed = LogEntry.objects.filter(action_flag=CHANGE).filter(user=request.user)
    changed_movies=[]
    for le in changed:
        if le.content_type.name == 'movie':
            try:
                changed_movies.append(le.get_edited_object())
            except:
                pass
    added = LogEntry.objects.filter(action_flag=ADDITION).filter(user=request.user)
    added_movies=[]
    for le in added:
        if le.content_type.name == 'movie':
            try:
                added_movies.append(le.get_edited_object())
            except:
                pass
    '''deleted = LogEntry.objects.filter(action_flag=DELETION).filter(user=request.user)
    deleted_movies=[]
    for le in deleted:
        if le.content_type.name == 'movie':
            deleted_movies.append(le.get_edited_object())'''
    


    context = {
        "viewed":viewed_movies,
        "changed":changed_movies,
        "added":added_movies,
        #"deleted":deleted_movies,
        "user":request.user,
    }
    return render(request,'main/account.html',context)
