# Generated by Django 2.2.6 on 2020-05-17 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200517_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover',
            field=models.ImageField(height_field=100, null=True, upload_to='media/moviecovers', verbose_name='cover', width_field=100),
        ),
    ]
