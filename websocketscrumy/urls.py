from django.urls import path
from websocketscrumy import views

app_name = 'websocketscrumy'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('connect/', views.connect, name='connect'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path('send_message/', views.send_message, name='send_message'),
    path('istyping/', views.isTyping, name='isTyping'),
    path('getRecentMessages', views.getRecentMessages, name='getRecentMessages')
]
