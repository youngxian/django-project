from django.urls import path
from django.urls import include
from websocketscrumy import views
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

app_name = 'websocketscrumy'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('connect/', views.connect, name='connect'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path('send_message/', views.send_message, name='send_message')
]
