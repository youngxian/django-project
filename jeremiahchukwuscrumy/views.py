from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import ScrumyGoals, GoalStatus, ScrumyHistory, SignupForm, CreateGoalForm, MoveGoalForm
import random
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms



# Create your views here.


@login_required(login_url="/jeremiahchukwuscrumy/accounts/login")
def home(request):
    users = User.objects.all()
    loginuser = request.user
    group = Group.objects.filter(user = request.user)[0].name
    def get_by_status(status_name):
        goals = GoalStatus.objects.get(status_name=status_name)
        status_goals = goals.jeremiahchukwuscrumy.all()
        return status_goals


    daily_goals = get_by_status("Daily Goal")
    weekly_goals = get_by_status("Weekly Goal")
    verify_goals = get_by_status("Verify Goal")
    done_goals = get_by_status("Done Goal")

    dictionary = {
        'users': users,
        'weekly_goals': weekly_goals,
        'daily_goals': daily_goals,
        'verify_goals': verify_goals,
        'done_goals': done_goals,
        'group': group,
        'loginuser': loginuser,
        'owner': 'Owner'
    }
    return render(request, 'jeremiahchukwuscrumy/home.html', dictionary)



def move_goal(request, goal_id):
    
    form = MoveGoalForm
    error = {'error': 'A record with that goal id does not exist'}
    allstatus = GoalStatus.objects.all()
    obj = ScrumyGoals.objects.get(goal_id=goal_id)
    status = GoalStatus.objects.get(status_name=obj.goal_status)
    weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")
    dailygoal = GoalStatus.objects.get(status_name="Daily Goal")
    verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
    donegoal = GoalStatus.objects.get(status_name="Done Goal")
    user = User.objects.get(username=request.user)
    
    # group = user.groups.all()[0].name
    group = Group.objects.filter(user = request.user)[0].name
    goals = {
            'goalss': obj,
            'goal_status': status,
            'goal_name': obj.goal_name,
            'user': user,
            'group':group,
            'allstatus': list(allstatus),
            'weeklygoal': weeklygoal,
            'dailygoal': dailygoal,
            'verifygoal': verifygoal,
            'donegoal': donegoal
            }

    try:
        if request.method == 'POST':
            form = form(request.POST)
            data = request.POST.dict()
        
            obj = ScrumyGoals.objects.get(goal_id=goal_id)
            status = GoalStatus.objects.get(status_name = data['goal_status'])
            obj.goal_status = status
            obj.save()
            return HttpResponseRedirect('/jeremiahchukwuscrumy/home')
        
    except Exception as e:
        return render(request, 'jeremiahchukwuscrumy/exception.html', error)
    # else:
        # return HttpResponse(obj.goal_name)
    return render(request, 'jeremiahchukwuscrumy/movegoal.html', goals)


@login_required(login_url="/jeremiahchukwuscrumy/accounts/login")
def add_goal(request):
    form = CreateGoalForm
    users = User.objects.all()
    currentuser = User.objects.get(username=request.user)
    allstatus = GoalStatus.objects.all()
    group = Group.objects.filter(user=request.user)[0].name
    weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")
    context = {'create_goal': form, 'users': users,
               'goalstatus': allstatus, 'message': "", "group": group, "currentuser": currentuser, "weeklygoal": weeklygoal}
    if request.method == 'POST':
        form = form(request.POST)
        data = request.POST.dict()
        f = forms.CharField()

        try:
            f.clean(data['goal_name'])
            random_list = list(random.sample(range(1000, 9999), 10))
            random.shuffle(random_list)
            random_no = random_list[0]
            status = GoalStatus.objects.get(status_name = data['goal_status'])
            user = User.objects.get(username=data['user'])
            add_goal=ScrumyGoals(
            goal_name = data['goal_name'],
            goal_id = random_no,
            goal_status = status,
            moved_by = user.username,
            created_by = user.username,
            owner = user.username,
            user = user)
            add_goal.save()
            return HttpResponseRedirect('/jeremiahchukwuscrumy/home')
        except Exception as e:
            context = {
                        'create_goal': form,
                        'users': users,
                        'goalstatus': allstatus,
                        'message': "Goal name can't be empty",
                        "group": group,
                        "currentuser": currentuser
                    }
            return render(request, 'jeremiahchukwuscrumy/addgoal.html', context)
    
    return render(request, 'jeremiahchukwuscrumy/addgoal.html', context)

        
        
    
    



def index(request):
    form = SignupForm
    groups = Group.objects.all()
    error ={
                'Message' : 'Cannot create user',
            }
    context = {'form': form, 
               'groups': ["sknba","skankla"]}
    if(request.method == 'POST'):
        data = request.POST.dict()
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        user.last_name = data['last_name']
        user.first_name = data['first_name']
        user.save()
        new_user = User.objects.get(username=data['username'])
        developer = Group.objects.get(name='Developer')
        developer.user_set.add(new_user)
        return redirect('/jeremiahchukwuscrumy/success/')
        # except Exception as e:
            # return render(request, 'registration/signup.html', error)
    else:
        return render(request, 'registration/index.html', error)

    return render(request, 'registration/index.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/jeremiahchukwuscrumy/accounts/login')
