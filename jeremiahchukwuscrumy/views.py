from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import ScrumyGoals, GoalStatus, ScrumyHistory
from random import randint
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    scrumyGoals = ScrumyGoals.objects.all()
    output = ', '.join([eachgoal.goal_name for eachgoal in scrumyGoals])
    return HttpResponse(output)


def move_goal(request, goal_id):
    error = {'error':'A record with that goal id does not exist'}
    try:
        obj = ScrumyGoals.objects.get(goal_id=goal_id)
    except Exception as e:
        return render(request, 'jeremiahchukwuscrumy/exception.html', error)
    else:
        return HttpResponse(obj.goal_name)



def add_goal(request):
    randnumber = randint(1000, 9999)
    # goalname = ScrumyGoals.objects.get(goal_id=randnumber)
    weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")
    newuser = User.objects.create(username="Louis Oma")
    saveuser = newuser.save()
    user = User.objects.get(username="Louis Oma")
    scrumygoal = ScrumyGoals(goal_name="Keep Learning Django", goal_id=randnumber, created_by="Louis", moved_by="Louis", owner="Louis", goal_status=weeklygoal, user=user)
    save = scrumygoal.save()
    return HttpResponse(save)


def home(request):
    # templates = loader.get_template('jeremiahchukwuscrumy/home.html')
    scrumgoal = ScrumyGoals.objects.get(goal_name='Learn Django')
    dictionary = {
        'goal_id': scrumgoal.goal_id,
        'goal_name': scrumgoal.goal_name,
        'user': scrumgoal,
    }
    # context = goal_name, goal_id and user of an instance of the ScrumyGoal record “Learn Django”
    return HttpResponse(render(request, 'jeremiahchukwuscrumy/home.html', dictionary))


