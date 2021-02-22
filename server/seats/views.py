from rest_framework import permissions, viewsets,serializers
from .serializers import SeatsSerializer, NestedSeatSerializer,DoubleNestedSeatSerializer
from .models import Seat
from tickets.models import Ticket
from django.db.models import Q
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from tickets.models import Ticket
from tickets.serializers import DoubleNestedTicketSerializer
class SeatsView(viewsets.ReadOnlyModelViewSet):
  #seats that are currently in cart
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = DoubleNestedSeatSerializer
  def get_queryset(self): 
    user = self.request.user
    return Seat.objects.filter(Q(user=user), Q(status=Seat.ASSIGNED))

class SeatBookedView(viewsets.ReadOnlyModelViewSet):
  #seats that are have been booked by user
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = DoubleNestedTicketSerializer
  def get_queryset(self): 
    user = self.request.user
    return Ticket.objects.filter(Q(user=user))
   

#seats by screening view, must have nested user serializer
# class SeatByScreening(viewsets.ReadOnlyModelViewSet):
#   permission_classes = (permissions.IsAuthenticated,)
#   serializer_class = NestedSeatSerializer
#   lookup_field='screening'
#   lookup_url_kwarg = 'screening_id'
#   def get_queryset(self): 
#     screening= self.request.query_params.get('screening_id', None)
#     print(screening)
#     print(self.request.query_params)
#     print(Seat.objects.all().filter(screening=screening))
#     return Seat.objects.all().filter(screening=screening).order_by('id')
  #arrange them by ID in get_queryset

@api_view(['GET'])
@permission_classes(())
def seatsByScreeningList(request, screening_id):
  try: 
    seats= Seat.objects.all().filter(screening=screening_id).order_by('id')
  except Seat.DoesNotExist:
    return Response({"error": "Invalid Operation"})
  if request.method=='GET':
    serializer= NestedSeatSerializer(seats, many=True)
    return Response(serializer.data)  


@api_view(['POST'])
@permission_classes(())
def seatsUpdateToPaid(request, user_id):
  user=User.objects.get(pk=user_id)
  try: 
    seats=Seat.objects.filter(Q(user=user), Q(status=Seat.ASSIGNED))
  except Seat.DoesNotExist:
    return Response({"error": "Invalid Operation"})
  if request.method=='POST':
    for seat in seats:
      seat.status= Seat.BOOKED
      seat.save()
      ticket=Ticket(user=user, screening=seat.screening, seat=seat)
      ticket.save()
  return Response({'success': 'you have successfully checked out!'})