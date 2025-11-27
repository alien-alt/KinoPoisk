"""
URL configuration for kino_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# GET Views
from kino.views import (
        HomeView, GenreMovieView, SearchMovieView,
        MovieView, ActorView, RegisterView, LoginView
        )

# POST Views
from kino.views import (
        MakeRegister, MakeLogin, MakeLogout, 
        MakeAddComment, MakeAddRating
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('genre/<int:genre_id>', GenreMovieView.as_view(), name="genre"),
    path('search/', SearchMovieView.as_view(), name="search"),
    path('movie/<int:id>', MovieView.as_view(), name="movie"),
    path('actor/<int:id>', ActorView.as_view(), name="actor"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),

    path('make-register/', MakeRegister.as_view(), name="make_register"),
    path('make-login/', MakeLogin.as_view(), name="make-login"),
    path('make-logout/', MakeLogout.as_view(), name="make-logout"),
    path('make-add-comment/<int:id>', MakeAddComment.as_view(), name="make_add_comment"),
    path('make-add-rating/<int:id>', MakeAddRating.as_view(), name="make_add_rating"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

