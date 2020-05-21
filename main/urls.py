"""moviehub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
import moviehub.settings as settings
from . import views
from django.contrib.staticfiles.urls import static
#from django.contrib.staticfiles.urls import staticfiles_urlpattern

 



app_name = "main"

urlpatterns = [
    path('',views.homepage, name="homepage"),
    path('home/',views.homepage, name="homepage1"),
    path('register/',views.register, name="register"),
    path('logout/',views.logout_request, name="logout"),
    path('login/',views.login_request, name="login"),
    path('account/',views.account, name="account"),

    path('movie/add/', views.Movie_create_view.as_view(), name="movie-create"),
    path('movie/<int:pk>/', views.Movie_detail_view.as_view(), name="movie-detail"),
    path('movie/<int:pk>/update/', views.Movie_update_view.as_view(), name="movie-update"),
    path('movie/<int:pk>/delete/', views.Movie_delete_view.as_view(), name="movie-delete"),
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)