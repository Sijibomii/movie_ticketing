from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import Group
from .models import Seat
from .serializers import SeatsSerializer, NestedSeatSerializer
from channels.layers import get_channel_layer
class SeatsConsumer(AsyncJsonWebsocketConsumer): 
  groups = ['test']
  @database_sync_to_async
  def get_user_of_seat(self, pk):
    instance = Seat.objects.get(id=pk)
    print(instance.user.id)
    return instance.user.id

  @database_sync_to_async
  def get_status_of_seat(self, pk):
    instance = Seat.objects.get(id=pk)
    print(instance.status)
    return instance.status


  @database_sync_to_async
  def _remove_seat(self, data):
    instance = Seat.objects.get(id=data.get('seat'))
    serializer = SeatsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.update(instance, serializer.validated_data)

  @database_sync_to_async
  def _assign_seat(self, data):
    instance = Seat.objects.get(id=data.get('seat'))
    serializer = SeatsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.update(instance, serializer.validated_data)
  @database_sync_to_async
  def _add_group(self,user, group):
    user_group, _ = Group.objects.get_or_create(name=group) 
    user.groups.add(user_group)
    user.save()
  @database_sync_to_async
  def _get_seat_data(self, seat):
    return NestedSeatSerializer(seat).data
  @database_sync_to_async
  def _get_user_group(self,user):
    groups=user.groups.values_list('name',flat = True)
    return list(groups)
  async def connect(self): 
    user = self.scope['user']
    if user.is_anonymous:
      await self.close()
    else:
      await self.channel_layer.group_add(group='test',channel=self.channel_name)
      await self.accept()

  async def disconnect(self, code):
    await self.channel_layer.group_discard(group='test',channel=self.channel_name)
    user = self.scope['user']
    user_group = await self._get_user_group(user)
    for group in user_group:
      await self.channel_layer.group_discard(group=group, channel=self.channel_name)
    await super().disconnect(code)

  async def echo_message(self, message): 
    await self.send_json(message)


  async def receive_json(self, content, **kwargs):
    message_type = content.get('type')
    if message_type == 'echo.message':
      await self.echo_message(content)
    elif message_type == 'add.group':
      await self.add_group(content)
    elif message_type == 'assign.seat':
      await self.assign_seat(content)
    elif message_type == 'remove.seat':
      await self.remove_seat(content)
    

  async def remove_seat(self, message):
    data=message.get('data')
    seat_id=data['seat']
    screening_id=data['screening']
    user_id=data['user']
    data['user']=None
    print(data)
    if user_id == await self.get_user_of_seat(seat_id) and await self.get_status_of_seat(seat_id) == 'ASSIGNED':
      seat= await self._remove_seat(data)
      seat_data= await self._get_seat_data(seat)
      message={
      'status': seat_data['status'],
      'id': seat_data['id'],
      }
      await self.channel_layer.group_send(group=screening_id,
        message={
            'type': 'echo.message',
            'data': message,
        }
      )
    else:
      message={
        'error':'The seat is not currently assigned to you'
      }
      await self.channel_layer.group_send(group=screening_id,
        message={
            'type': 'echo.message',
            'data': message,
        }
      )

  async def assign_seat(self, message):
    data = message.get('data')
    seat= await self._assign_seat(data)
    screening_id = f'{seat.screening.id}'
    seat_data= await self._get_seat_data(seat)
    message={
      'status': seat_data['status'],
      'id': seat_data['id']
    }
    await self.channel_layer.group_send(group=screening_id,
        message={
            'type': 'echo.message',
            'data': message,
        }
    ) 
  async def send_to_group(group, message):
    print('ddd')
    layer=get_channel_layer()
    await layer.group_send(group=group,
        message={
            'type': 'echo.message',
            'data': message,
        }
    )
  async def add_group(self, message):
    user = self.scope['user']
    data=message.get('data')
    group=data['group']
    await self._add_group(user, group)
    await self.channel_layer.group_add(group=group, channel=self.channel_name)
    await self.channel_layer.group_send(
        group=group,
        message={
             'type': 'echo.message',
              'data': 'added'
        }
    )

