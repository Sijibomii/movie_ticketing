from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Seat
import threading 
import time
from .serializers import SeatsSerializer
from .consumers import SeatsConsumer
import asyncio
from syncer import sync
def thread_function(id):
  time.sleep(60)
  try:
    seat= Seat.objects.get(pk=id)
  except Seat.DoesNotExist:
    raise ValueError({"seat does not exist"})

  if seat.user and seat.status == 'ASSIGNED':
    data= {
            'user': None,
            'seat': seat.id,
            'status': 'EMPTY'
    }
    instance = Seat.objects.get(id=data.get('seat'))
    serializer = SeatsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    message = serializer.update(instance, serializer.validated_data)
    message_to={
      'status': data['status'],
      'id': data['seat']
    }
    screening_id= f'{seat.screening.id}'
    asyncio.run(last(screening_id,message_to))
  print('completed!')
  
async def last(screening_id, message_to):
  print('yeaa')
  await SeatsConsumer.send_to_group(screening_id, message_to)


@receiver(post_save, sender=Seat)
def reversalHandler(sender, instance, created, **kwargs):
  if created == False:
    print('about to start nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
    x = threading.Thread(target= thread_function, args=(instance.id,))
    x.start()
    print('starteddd')
