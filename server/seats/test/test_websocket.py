import pytest
from channels.testing import WebsocketCommunicator
from movie.routing import application
from channels.layers import get_channel_layer
from django.core.management import call_command
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from seats.models import  Seat
import asyncio
from screenings.models import Movie,Screening,Hall
TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@database_sync_to_async
def _get_seat_data(pk):
  return Seat.objects.get(pk=pk)
@database_sync_to_async
def create_user(username, password):
  user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
  access = AccessToken.for_user(user)
  return user, access
@database_sync_to_async
def create_seat():
  data = BytesIO()
  Image.new('RGB', (100, 100)).save(data, 'PNG')
  data.seek(0)
  photo_file= SimpleUploadedFile('photo.png', data.getvalue())
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
  seat=Seat.objects.create(screening=screening ,status=Seat.EMPTY )
  return seat

@database_sync_to_async
def get_seat_screening(seat):
  seat= Seat.objects.get(pk=seat)
  sc=seat.screening
  return sc


@database_sync_to_async
def create_screening():
  data = BytesIO()
  Image.new('RGB', (100, 100)).save(data, 'PNG')
  data.seek(0)
  photo_file= SimpleUploadedFile('photo.png', data.getvalue())
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
  return screening
@database_sync_to_async
def create_photo_file():
  data = BytesIO()
  Image.new('RGB', (100, 100)).save(data, 'PNG')
  data.seek(0)
  return SimpleUploadedFile('photo.png', data.getvalue())
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
  async def test_can_connect_to_server(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    _, access = await create_user('test.user@example.com', 'pAssw0rd')
    screening='234'
    communicator = WebsocketCommunicator(application=application,path=f'/movie/?token={access}')
    connected, _ = await communicator.connect()
    assert connected is True
    await communicator.disconnect()

  async def test_can_send_and_receive_messages(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    _, access = await create_user('test.user@example.com', 'pAssw0rd')
    communicator = WebsocketCommunicator(application=application,path=f'/movie/?token={access}')
    connected, _ = await communicator.connect()
    message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == message
    await communicator.disconnect()

  async def test_can_send_and_receive_broadcast_messages(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    _, access = await create_user('test.user@example.com', 'pAssw0rd')
    communicator = WebsocketCommunicator(application=application,path=f'/movie/?token={access}')
    connected, _ = await communicator.connect()
    message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
    channel_layer = get_channel_layer()
    await channel_layer.group_send('test', message=message)
    response = await communicator.receive_json_from()
    assert response == message
    await communicator.disconnect()

  async def test_cannot_connect_to_socket(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    communicator = WebsocketCommunicator(
            application=application,
            path='/movie/'
        )
    connected, _ = await communicator.connect()
    assert connected is False
    await communicator.disconnect()

  async def test_can_be_added_to_screening_group(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    user, access = await create_user(
        'test.user@example.com', 'pAssw0rd'
    )
    screening= await create_screening()
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/movie/?token={access}'
    )
    connected, _ = await communicator.connect()
    await communicator.send_json_to({
        'type': 'add.group',
        'data': {
            'group': str(screening.id)
        }
    })
    response = await communicator.receive_json_from()
    assert response == {'data': 'added', 'type': 'echo.message'}

    channel_layer = get_channel_layer()
    message = {
        'type': 'echo.message',
        'data': 'This is a test message.',
    }
    await channel_layer.group_send(f'{screening.id}', message=message)
    response = await communicator.receive_json_from()
    assert response == message
    await communicator.disconnect()

  async def test_user_can_assign_seat(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    user, access = await create_user(
        'test.user@example.com', 'pAssw0rd'
    )
    seat= await create_seat()
    screening=await get_seat_screening(seat.id)
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/movie/?token={access}'
    )
    connected, _ = await communicator.connect()
    await communicator.send_json_to({
        'type': 'add.group',
        'data': {
            'group': str(screening.id)
        }
    })
    response = await communicator.receive_json_from()
  
    await communicator.send_json_to({
        'type': 'assign.seat',
        'data': {
            'screening': str(screening.id),
            'user': user.id,
            'seat': seat.id,
            'status': 'ASSIGNED'
        },
    })
    response = await communicator.receive_json_from()
    response_data = response.get('data')
    assert response_data['status'] == 'ASSIGNED'
    assert response_data['id'] is not None
    await communicator.disconnect()

  #system revokes assignment after 1Min
  async def test_seats_becomes_empty_after_one_min(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    user, access = await create_user(
        'test.user@example.com', 'pAssw0rd'
    )
    seat= await create_seat()
    screening=await get_seat_screening(seat.id)
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/movie/?token={access}'
    )
    connected, _ = await communicator.connect()
    await communicator.send_json_to({
        'type': 'add.group',
        'data': {
            'group': str(screening.id)
        }
    })
    response = await communicator.receive_json_from()
  
    await communicator.send_json_to({
        'type': 'assign.seat',
        'data': {
            'screening': str(screening.id),
            'user': user.id,
            'seat': seat.id,
            'status': 'ASSIGNED'
        },
    })
    response = await communicator.receive_json_from()
    await asyncio.sleep(70)
    seat_data= await _get_seat_data(seat.id)
    assert seat_data.user is None
    assert seat_data.status == 'EMPTY'
    #NOT SENDING MESSAGE TO GROUP AFTER REMOVAL
    # response = await communicator.receive_json_from()
    # response_data = response.get('data')
    # assert response_data is not None
    await communicator.disconnect()


#user can unassign a seat himself
  async def test_user_can_unassign_seat(self,settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    user, access = await create_user(
        'test.user@example.com', 'pAssw0rd'
    )
    seat= await create_seat()
    screening=await get_seat_screening(seat.id)
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/movie/?token={access}'
    )
    connected, _ = await communicator.connect()
    await communicator.send_json_to({
        'type': 'add.group',
        'data': {
            'group': str(screening.id)
        }
    })
    response = await communicator.receive_json_from()
  
    await communicator.send_json_to({
        'type': 'assign.seat',
        'data': {
            'screening': str(screening.id),
            'user': user.id,
            'seat': seat.id,
            'status': 'ASSIGNED'
        },
    })
    response = await communicator.receive_json_from()
    await communicator.send_json_to({
        'type': 'remove.seat',
        'data': {
            'screening': str(screening.id),
            'user': user.id,
            'seat': seat.id,
            'status': 'EMPTY'
        },
    })
    response = await communicator.receive_json_from()
    response_data = response.get('data')
    assert response_data is not None
    await communicator.disconnect()

#seats are automatically created after a screening is created-http