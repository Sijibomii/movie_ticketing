from rest_framework import serializers
from .models import Seat
from screenings.serializers import HallSerializer,ScreeningSerializer,MoviesSerializer
from accounts.serializers import UserSerializer

class SeatsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Seat
    fields = '__all__'

class NestedSeatSerializer(serializers.ModelSerializer):
  screening = ScreeningSerializer
  user = UserSerializer
  hall= HallSerializer
  class Meta:
    model = Seat
    fields = '__all__'
    depth = 1


class DoubleNestedSeatSerializer(serializers.ModelSerializer):
  movie= MoviesSerializer
  screening = ScreeningSerializer
  user = UserSerializer
  hall= HallSerializer
  venue=HallSerializer
  class Meta:
    model = Seat
    fields = '__all__'
    depth = 2
