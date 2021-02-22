from screenings.serializers import ScreeningSerializer
from seats.serializers import DoubleNestedSeatSerializer
from accounts.serializers import UserSerializer
from rest_framework import serializers
from .models import Ticket
class DoubleNestedTicketSerializer(serializers.ModelSerializer):
  screening = ScreeningSerializer
  user = UserSerializer
  seat=DoubleNestedSeatSerializer
  class Meta:
    model = Ticket
    fields = '__all__'
    depth = 2