from rest_framework.test import APITestCase
from screenings.models import Movie,Screening,Hall
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse
def create_photo_file():
  data = BytesIO()
  Image.new('RGB', (100, 100)).save(data, 'PNG')
  data.seek(0)
  return SimpleUploadedFile('photo.png', data.getvalue())
class MovieTest(APITestCase):
  def test_user_can_get_all_movies(self):
    photo_file = create_photo_file()
    movies=[
      Movie.objects.create(
        title='New Movie',
        duration='2hrs 40 Mins',
        trailer=photo_file,
        image=photo_file,
        rated=Movie.ratingType.RATED_18,
        genre='comedy',
        director='director joe',
        cast='cast',
        description='describe',
        ),
      Movie.objects.create(
        title='Newest Movie',
        duration='2hrs 30 Mins',
        trailer=photo_file,
        image=photo_file,
        rated=Movie.ratingType.RATED_18,
        genre='film trick',
        director='director jane',
        cast='cast',
        description='describe', 
        ),
      Movie.objects.create(
        title='Newer Movie',
        duration='2hrs 10 Mins',
        trailer=photo_file,
        image=photo_file,
        rated=Movie.ratingType.RATED_18,
        genre='film trick',
        director='director john',
        cast='cast',
        description='describe',
        ),
    ]
    response = self.client.get(reverse('movie:movies_list'))
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    exp_movie_ids = [str(movie.id) for movie in movies]
    act_movie_ids = [movie.get('id') for movie in response.data]
    self.assertCountEqual(act_movie_ids, exp_movie_ids)

  def test_user_can_retrieve_movie_by_id(self):
    photo_file = create_photo_file()
    movie =Movie.objects.create(
        title='Newer Movie',
        duration='2hrs 10 Mins',
        trailer=photo_file,
        image=photo_file,
        rated=Movie.ratingType.RATED_18,
        genre='film trick',
        director='director john',
        cast='cast',
        description='describe',
        )
    hall=Hall.objects.create(
      name='hall 1',
      no_of_seats=5
    )
    screening=Screening.objects.create(
      venue=hall,
      time='18:00:00',
      date='2020-01-20',
      movie=movie,
      price=30.00
    )
    response = self.client.get(movie.get_absolute_url())
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    self.assertEqual(str(movie.id), response.data.get('id'))


class ScreeningTest(APITestCase):
  def test_user_can_get_all_screenings(self):
    photo_file = create_photo_file()
    movie =Movie.objects.create(
        title='Newer Movie',
        duration='2hrs 10 Mins',
        trailer=photo_file,
        image=photo_file,
        rated=Movie.ratingType.RATED_18,
        genre='film trick',
        director='director john',
        cast='cast',
        description='describe',
        )
    hall=Hall.objects.create(
      name='hall 1',
      no_of_seats=5
    )
    screenings=[
      Screening.objects.create(
      venue=hall,
      time='18:00:00',
      date='2020-01-20',
      movie=movie,
      price=30.00
    ),
    Screening.objects.create(
      venue=hall,
      time='18:00:00',
      date='2020-01-20',
      movie=movie,
      price=30.00
    ),
    Screening.objects.create(
      venue=hall,
      time='18:00:00',
      date='2020-01-20',
      movie=movie,
      price=30.00
    )
    ]
    response = self.client.get(reverse('movie:screening_list'))
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    exp_screening_ids = [str(screening.id) for screening in screenings]
    act_screening_ids = [screening.get('id') for screening in response.data]
    self.assertCountEqual(act_screening_ids, exp_screening_ids)
  
  def test_user_can_retrieve_screening_by_id(self):
    photo_file = create_photo_file()
    movie =Movie.objects.create(
        title='Newer Movie',
        duration='2hrs 10 Mins',
        trailer=photo_file,
        image=photo_file,
        rated=Movie.ratingType.RATED_18,
        genre='film trick',
        director='director john',
        cast='cast',
        description='describe',
        )
    hall=Hall.objects.create(
      name='hall 1',
      no_of_seats=5
    )
    screening = Screening.objects.create(
      venue=hall,
      time='18:00:00',
      date='2020-01-20',
      movie=movie,
      price=30.00
    )
    response = self.client.get(screening.get_absolute_url())
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    self.assertEqual(str(screening.id), response.data.get('id'))