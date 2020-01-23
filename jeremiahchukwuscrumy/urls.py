from django.urls import path
from jeremiahchukwuscrumy import views

urlpatterns = [
    path('', views.index),
    path('movegoal/<int:goal_id>', views.move_goal),
]