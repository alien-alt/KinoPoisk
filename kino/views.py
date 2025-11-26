from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from .models import User, Movie, Actor, Comment, Rating, Genre
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['authenticated'] = False
        context['genres'] = Genre.objects.all()

        page = self.request.GET.get('page', 1)

        if self.request.user.is_authenticated:
            print("authenticated")
            context['username'] = self.request.user.username
            context['authenticated'] = True

        movies = Movie.objects.all().order_by('-rating')
        paginator = Paginator(movies, 2)
        page_movies = paginator.get_page(page)


        context['movies'] = page_movies

        return context


class GenreMovieView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, genre_id=None, **kwargs):
        context = {}
        context['authenticated'] = False
        context['genres'] = Genre.objects.all()

        if self.request.user.is_authenticated:
            print("authenticated")
            context['username'] = self.request.user.username
            context['authenticated'] = True

        if genre_id:
            genre_is_exists = Genre.objects.filter(id=genre_id).exists()

            if not(genre_is_exists):
                return {}

            genre = Genre.objects.get(id=genre_id)

            movies = genre.movies.all().order_by('-rating')
            context['movies'] = movies

            return context

        context['movies'] = {}

        return context

class SearchMovieView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['authenticated'] = False
        context['genres'] = Genre.objects.all()

        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
            context['authenticated'] = True

        text = self.request.GET.get('search')
        movies = Movie.objects.filter(name__contains=text)

        context['movies'] = movies

        return context



class MovieView(TemplateView):
    template_name = 'movie_page.html'

    def get_context_data(self, **kwargs):
        movie_id = kwargs.get('id')
        movie_is_exists = Movie.objects.filter(id=movie_id).exists()

        if movie_is_exists:
            movie = Movie.objects.get(id=movie_id)
            actors = movie.actors.all()
            comments = movie.comments.all()
            
            context = {
                'movie': movie,
                'actors': actors,
                'comments': comments
            }

            return context

        return redirect('register')


class ActorView(TemplateView):
    template_name = 'actor_page.html'

    def get_context_data(self, *args, **kwargs):
        actor_id = kwargs.get('id')
        actor_is_exists = Actor.objects.filter(id=actor_id).exists()

        if actor_is_exists:
            actor = Actor.objects.get(id=actor_id)

            context = {
                'actor': actor,
                'movies': actor.movies.all(),
            }

            return context

        return redirect('register')


class RegisterView(TemplateView):
    template_name = 'register.html'

class LoginView(TemplateView):
    template_name = 'login.html'

"""
        POST
"""

class MakeRegister(View):
    def post(self, request, *args, **kwargs):
        data = request.POST

        username = data.get('username')
        password = data.get('password')

        fields_is_not_empty = username and password
        username_is_unique = not(User.objects.filter(username=username).exists())

        if fields_is_not_empty and username_is_unique:
            new_user = User.objects.create_user(
                username=username,
                password=password
            )

            login(request, new_user)
            return redirect('home')


class MakeLogin(View):
    def post(self, request, *args, **kwargs):
        data = request.POST

        username = data.get('username')
        password = data.get('password')

        fields_is_not_empty = username and password

        if fields_is_not_empty:
            user_is_exists = User.objects.filter(username=username).exists()

            if user_is_exists:
                user = User.objects.get(username=username)

                if check_password(password, user.password):
                    login(request, user)
                    return redirect("home")

                return redirect("login")

            return redirect('register')

        
        return redirect("login")


class MakeLogout(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class MakeAddComment(View):
    def post(self, request, *args, **kwargs):
        data = request.POST

        comment_text = data.get('text')
        movie_id = kwargs.get('id')

        movie_is_exists = Movie.objects.filter(id=movie_id)

        if request.user.is_authenticated and movie_is_exists:
            user = request.user
            movie = Movie.objects.get(id=movie_id)

            has_commented = Comment.objects.filter(author=user, movie=movie).exists()

            if not(has_commented):
                comment = Comment.objects.create(
                    author=user,
                    movie=movie,
                    text=comment_text,
                )

        return redirect('movie', movie_id)


class MakeAddRating(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        rating = data.get('rating', 10)
        movie_id = kwargs.get('id')
        user = request.user
        movie_is_exists = Movie.objects.filter(id=movie_id).exists()

        if not(user.is_authenticated):
            return redirect('movie', movie_id)

        if not(movie_is_exists):
            return redirect('home')


        movie = Movie.objects.get(id=movie_id)
        has_rated = Rating.objects.filter(user=user, movie=movie).exists()

        if has_rated:
            print('HAS RATED')
            return redirect('movie', movie_id)

        if rating.isdigit():
            if int(rating) > 5 or int(rating) < 1:
                print('RATING OUT OF RANGE')
                return redirect('movie', movie_id)

            Rating.objects.create(user=user, movie=movie, rating=rating)
            movie_ratings = movie.ratings.values_list('rating', flat=True)

            movie_rating = 0
            if movie_ratings:
                movie_rating = sum(movie_ratings) / len(movie_ratings)

            movie.rating = movie_rating
            movie.save()
    
            print(f"movie: {movie.name}\nuser: {user.username}\n rating: {rating}")
            return redirect('movie', movie_id)

        return redirect('movie', movie_id)

