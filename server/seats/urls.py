from django.urls import path

from .views import SeatBookedView, SeatsView,seatsByScreeningList,seatsUpdateToPaid#,SeatByScreening
app_name = 'seats'
urlpatterns = [
    path('', SeatsView.as_view({'get': 'list'}), name='seats_list'),
    path('booked/', SeatBookedView.as_view({'get': 'list'}), name='seats_booked_list'),
    path('screening/<uuid:screening_id>/', seatsByScreeningList, name='seats_by_screening_list'),
    path('screening/pay/<int:user_id>/', seatsUpdateToPaid, name='seats_pay')
    # path('screening/<uuid:screening_id>/', SeatByScreening.as_view({'get': 'list'}), name='seats_by_screening_list')
]  