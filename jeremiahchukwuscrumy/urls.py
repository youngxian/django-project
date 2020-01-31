from django.urls import path
from django.urls import include
from jeremiahchukwuscrumy import views
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

app_name = 'jeremiahchukwuscrumy'

urlpatterns = [
    path('', views.sign_up, name='signup'),
    path('movegoal/<int:goal_id>/', views.move_goal),
    path('addgoal/', views.add_goal, name='add'),
    path('home/', views.home),
    path('success/', TemplateView.as_view(
        template_name='jeremiahchukwuscrumy/success.html'), name='successpage'),
    path('accounts/', include('django.contrib.auth.urls')),
]