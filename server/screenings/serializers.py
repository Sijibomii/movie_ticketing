from rest_framework import serializers
from .models import Movie,Screening,Hall


class MoviesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = '__all__'
    read_only_fields = ('id',)

class ScreeningSerializer(serializers.ModelSerializer):
  class Meta:
    model = Screening
    fields = '__all__'
    read_only_fields = ('id',)

class HallSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hall
    fields = '__all__'
    read_only_fields = ('id',)
 

class NestedScreeningSerializer(serializers.ModelSerializer):
  movie = MoviesSerializer
  venue= HallSerializer
  class Meta:
    model = Screening
    fields = '__all__'
    depth = 1