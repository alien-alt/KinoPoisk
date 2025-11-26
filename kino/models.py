from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    email = None
    EMAIL_FIELD = None
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Genre(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='movies')
    image = models.ImageField(upload_to="media/movie_images")
    release_date = models.DateField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Actor(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(max_length=255)
    biography = models.TextField()
    photo = models.ImageField(upload_to="media/actors_photos")
    movies = models.ManyToManyField(Movie, related_name='actors', blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()


"""
    Модель для определения ставили ли пользователь рейтинг фильму
"""


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField()

