from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    directed_by = models.CharField(max_length=200,null=True)
    imdb_rating = models.FloatField(null=True)
    rotten_tomatoes_rating = models.IntegerField(null=True)
    length_in_mins = models.IntegerField()
    release_date = models.DateTimeField("release date",null=True)
    cover = models.ImageField("cover",null=True,upload_to="moviecovers")
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:movie-detail', kwargs={'pk':self.pk})


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    history = models.ManyToManyField(Movie,blank=True)

    def __str__(self):
        return str(self.user)
