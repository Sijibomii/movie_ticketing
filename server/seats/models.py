from django.db import models
from django.conf import settings
from screenings.models import Screening,Hall
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
class Seat(models.Model):
  BOOKED='BOOKED'
  ASSIGNED='ASSIGNED'
  EMPTY='EMPTY'
  
  STATUSES = (
        (BOOKED, BOOKED),
        (ASSIGNED, ASSIGNED),
        (EMPTY, EMPTY),
  )
  user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='seat_user'
    )
  screening=models.ForeignKey(Screening, on_delete=models.CASCADE,blank=True, null=True)
  status=models.CharField(max_length=50, choices=STATUSES, default=EMPTY)
  time_assigned= models.DateTimeField(default=now)
  seat_number=models.IntegerField(blank=True, null=True)
  def __str__(self):
    return self.screening.movie.title


@receiver(post_save, sender=Screening)
def create_seats(sender, instance, created, **kwargs):
  if created:
    i=0
    for x in range(instance.venue.no_of_seats):
      Seat.objects.create(screening=instance, seat_number=i)
      i=i+1
    print('seats created!!!!!!!!!!')
