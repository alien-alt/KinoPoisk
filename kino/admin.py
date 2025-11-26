from django.contrib import admin
from .models import Movie, Actor, Genre

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'image',
        'release_date'
    ]

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'last_name',
        'birth_date',
        'biography',
        'photo',
    ]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
