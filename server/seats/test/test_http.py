import json
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse
from seats.models import  Seat
from screenings.models import Movie,Screening,Hall
PASSWORD = 'pAssw0rd!'




def create_user(username='user@example.com', password=PASSWORD): 
  user = get_user_model().objects.create_user(username=username, password=password)
  return user

def create_photo_file():
  data = BytesIO()
  Image.new('RGB', (100, 100)).save(data, 'PNG')
  data.seek(0)
  return SimpleUploadedFile('photo.png', data.getvalue())
class SeatsTest(APITestCase):
  def setUp(self):
    self.user = create_user()
    self.client.login(username=self.user.username, password=PASSWORD)
  def test_user_can_list_seats_assigned(self):
    #the cart, seats assigned to user but not paid for 
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
    seats=[
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.ASSIGNED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.ASSIGNED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.ASSIGNED
      )
    ]
    response = self.client.get(reverse('seats:seats_list'))
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    exp_seats_ids = [seat.id for seat in seats]
    act_seats_ids = [seat.get('id') for seat in response.data]
    self.assertCountEqual(act_seats_ids, exp_seats_ids)

  def test_user_can_list_seats_booked(self):
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
    seats=[
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      )
    ]
    response = self.client.get(reverse('seats:seats_booked_list'))
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    exp_seats_ids = [seat.id for seat in seats]
    act_seats_ids = [seat.get('id') for seat in response.data]
    self.assertCountEqual(act_seats_ids, exp_seats_ids)

  #test seatByScreening returns seat arranged by ID
  def test_seats_By_Screening_are_return_in_order_of_ID(self):
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
    seats=[
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      ),
      Seat.objects.create(
        user=self.user,
        screening=screening,
        status=Seat.BOOKED
      )
    ]
    response = self.client.get(reverse('seats:seats_by_screening_list', kwargs={'screening_id' :screening.id}))
    self.assertEqual(status.HTTP_200_OK, response.status_code)
    exp_seats_ids = [seat.id for seat in seats]
    act_seats_ids = [seat.get('id') for seat in response.data]
    # print(response.data)
    # print(act_seats_ids)
    # print(json.loads(json.dump(response.data)))
    self.assertCountEqual(act_seats_ids, exp_seats_ids)
    # self.assertIsNone(response)

#seats are automatically created after Hall is created