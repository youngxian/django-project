from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import ScrumyGoals, GoalStatus, ScrumyHistory, SignupForm, CreateGoalForm
import random
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/jeremiahchukwuscrumy/accounts/login")
def home(request):
    users = User.objects.all()

    def get_by_status(status_name):
        goals = GoalStatus.objects.get(status_name=status_name)
        status_goals = goals.scrumygoals_set.all()
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
    }
    return render(request, 'jeremiahchukwuscrumy/home.html', dictionary)



def move_goal(request, goal_id):
    error = {'error':'A record with that goal id does not exist'}
    try:
        obj = ScrumyGoals.objects.get(goal_id=goal_id)
    except Exception as e:
        return render(request, 'jeremiahchukwuscrumy/exception.html', error)
    else:
        return HttpResponse(obj.goal_name)


@login_required(login_url="/jeremiahchukwuscrumy/accounts/login")
def add_goal(request):
    form = CreateGoalForm
    users = User.objects.all()
    if request.method == 'POST':
        random_list = list(random.sample(range(1000, 9999), 10))
        random.shuffle(random_list)
        random_no = random_list[0]
        status = GoalStatus.objects.get(status_name="Daily Goal")

        form = form(request.POST)
        data = request.POST.dict()
        print(data['user']+" the user")
        user = User.objects.get(username=data['user'])
        add_goal=ScrumyGoals(
            goal_name = data['goal_name'],
            goal_id = random_no,
            goal_status = status,
            moved_by = user.username,
            created_by = user.username,
            owner = user.username,
            user = user
            )
        add_goal.save()
        return HttpResponseRedirect('/jeremiahchukwuscrumy/home')
    context = {
        'create_goal': form,
        'users': users
    }

    return render(request, 'jeremiahchukwuscrumy/addgoal.html', context)



def sign_up(request):
    form = SignupForm
    error ={
                'Message' : 'Cannot create user',
            }
    if(request.method == 'POST'):
    #     form = SignupForm()
    # #    // try:

    #     form = SignupForm(request.POST)
        data = request.POST.dict()
        user = User.objects.create_user(data['username'], data['email'], data['password'], data['first_name'], data['last_name'])
        user.save()
        new_user = User.objects.get(username=data['username'])
        developer = Group.objects.get(name='Developer')
        developer.user_set.add(new_user)
        return redirect('/jeremiahchukwuscrumy/success/')
        # except Exception as e:
            # return render(request, 'registration/signup.html', error)
    else:
        return render(request, 'registration/signup.html', error)

    return render(request, 'registration/signup.html', {'form': form})
