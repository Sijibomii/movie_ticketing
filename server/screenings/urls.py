from django.urls import path

from .views import MoviesView,ScreeningsView,screeningsByMovieList
app_name = 'movie'
urlpatterns = [
    path('', MoviesView.as_view({'get': 'list'}), name='movies_list'),
    path('<uuid:movie_id>/', MoviesView.as_view({'get': 'retrieve'}), name='movie_detail'),
    path('screenings/all/', ScreeningsView.as_view({'get': 'list'}), name='screening_list'),
    path('screening/<uuid:screening_id>/', ScreeningsView.as_view({'get': 'retrieve'}), name='screening_detail'),
    path('screening/movie/<uuid:movie_id>/', screeningsByMovieList)
] 