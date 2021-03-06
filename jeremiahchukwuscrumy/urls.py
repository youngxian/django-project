from django.urls import path
from django.urls import include
from jeremiahchukwuscrumy import views
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

app_name = 'jeremiahchukwuscrumy'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index),
    path('movegoal/<int:goal_id>/', views.move_goal, name='movegoal'),
    path('addgoal/', views.add_goal, name='add'),
    path('home/', views.home),
    path('logout/', views.logout_view, name='logout'),
    path('success/', TemplateView.as_view(
        template_name='jeremiahchukwuscrumy/success.html'), name='successpage'),
        path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]