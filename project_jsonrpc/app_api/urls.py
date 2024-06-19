from .views import api_call
from django.urls import path


urlpatterns = [
    path('', api_call, name='api_call')
]

