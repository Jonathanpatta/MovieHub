# Generated by Django 2.2.6 on 2020-05-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_movie_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rating',
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_rating',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='rotten_tomatoes_rating',
            field=models.IntegerField(null=True),
        ),
    ]
