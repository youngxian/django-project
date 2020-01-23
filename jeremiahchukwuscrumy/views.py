from django.shortcuts import render
from django.http import HttpResponse
from .models import ScrumyGoals, GoalStatus, ScrumyHistory
from random import randint

# Create your views here.

def index(request):
    goal = ScrumyGoals.objects.filter(goal_name="Learn Django")
    return HttpResponse(goal)

def move_goal(request, goal_id):
    goal_name = ScrumyGoals.objects.get(goal_id = goal_id)
    return HttpResponse(goal_name.goal_name)
