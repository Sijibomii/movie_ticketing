from django.db import models
from django.conf import settings
from screenings.models import Screening
from seats.models import Seat
from django.utils.timezone import now
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
# Create your models here.
#filename = obj.model_attribute_name.path
class Ticket(models.Model):
  user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  screening=models.ForeignKey(Screening, on_delete=models.CASCADE)
  seat=models.ForeignKey(Seat, on_delete=models.CASCADE)
  date_time=models.DateField(default=now)
  qr_code=models.ImageField(upload_to='qr_codes/%m/%d/', blank=True, null=True)

  def __str__(self):
    return self.user.username 

  def save(self, *args, **kwargs):
    data={
      "username": self.user.username,
      "firstname": self.user.first_name,
      "lastname": self.user.last_name,
      "email": self.user.email,
      "seat": self.seat.id,
      "date": self.date_time,
      "Movie_to_screen": self.screening.movie.title,
      "isScreened": self.screening.is_screened,
      "Screening_time": self.screening.time,
      "screening_date": self.screening.date,
      "Screening_venue":self.screening.venue
    }
    qr__code=qrcode.make(data)
    canvas= Image.new('RGB',(290,290),'white')
    draw=ImageDraw.Draw(canvas)
    canvas.paste(qr__code)
    fname=f'qr_code_for-{self.user.username}_seat{self.seat.id}.png'
    buffer=BytesIO()
    canvas.save(buffer,'PNG')
    self.qr_code.save(fname, File(buffer),save=False)
    canvas.close()
    super().save(*args, **kwargs)


