from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from accounts.views import SignUpView
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import SignUpView, LogInView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sign_up/', SignUpView.as_view(), name='sign_up'),
    path('api/log_in/', LogInView.as_view(), name='log_in'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/movie/', include('screenings.urls', 'movie',)),
    path('api/seats/', include('seats.urls','seats')),
    path('api/tickets/', include('tickets.urls','tickets'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
  