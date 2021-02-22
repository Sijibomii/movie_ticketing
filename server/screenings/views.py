from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from .models import Movie,Screening
from .serializers import  MoviesSerializer, ScreeningSerializer, NestedScreeningSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

class MoviesView(viewsets.ReadOnlyModelViewSet):
  queryset = Movie.objects.all().filter(is_published=True)
  serializer_class = MoviesSerializer
  lookup_field = 'id' 
  lookup_url_kwarg = 'movie_id'
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    data=serializer.data
    screening= Screening.objects.all().filter(movie=instance.id)
    screening_data= ScreeningSerializer(screening, many=True).data
    screen=[]
    for item in screening_data:
      obj={}
      for key, value in item.items():
        obj[key]=value
      screen.append(obj)
    data['screening']=screen
    return Response(data)

class ScreeningsView(viewsets.ReadOnlyModelViewSet):
  queryset= Screening.objects.all().filter(is_screened=False)
  serializer_class=NestedScreeningSerializer
  lookup_field='id'
  lookup_url_kwarg = 'screening_id' 


@api_view(['GET'])
@permission_classes(())
def screeningsByMovieList(request, movie_id):
  try: 
    screenings= Screening.objects.all().filter(movie=movie_id).filter(is_screened=False)
  except Screening.DoesNotExist:
    return Response({"error": "Invalid Operation"})
  if request.method=='GET':
    serializer= ScreeningSerializer(screenings, many=True)
    return Response(serializer.data)  