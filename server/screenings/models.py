from django.db import models
import uuid
from django.shortcuts import reverse
from django.utils.timezone import now

class Hall(models.Model):
  name= models.CharField(max_length=255)
  no_of_seats=models.IntegerField()
  def __str__(self):
    return self.name


class Movie(models.Model):
  class ratingType(models.TextChoices):
    RATED_PG='PG'
    RATED_18='18+'
    RATED_16='16+'
    RATED_21='21+'
    RATED_13='13+'
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title=models.CharField(max_length=150)
  duration=models.CharField(max_length=150)
  trailer=models.FileField(upload_to='videos/%Y/%m/%d/', blank=True, null=True)
  image=models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
  rated=models.CharField(max_length=50, choices=ratingType.choices, default=ratingType.RATED_PG)
  genre=models.CharField(max_length=100)
  director=models.CharField(max_length=250)
  cast=models.TextField()
  description=models.TextField()
  release_date=models.DateField(default=now, blank=True)
  is_published=models.BooleanField(default=True)
  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('movie:movie_detail', kwargs={'movie_id': self.id})

 
class Screening(models.Model):
  id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  venue= models.ForeignKey(Hall ,on_delete=models.CASCADE)
  time= models.TimeField(null=True)
  date= models.DateField(null=True)
  movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
  is_screened=models.BooleanField(default=False)
  price=models.FloatField(blank=True, null=True)
  
  def __str__(self):
    return self.movie.title

  def get_absolute_url(self):
    return reverse('movie:screening_detail', kwargs={'screening_id': self.id})
