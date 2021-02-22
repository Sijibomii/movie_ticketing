from django.urls import path

from .views import download
app_name = 'tickets'
urlpatterns = [
  path('<int:pk>/', download, name='ticket_download')
]   