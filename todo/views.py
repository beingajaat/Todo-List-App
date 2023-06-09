from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from data.models import *
from django.contrib.auth.decorators import login_required
from data.forms import TaskForm


# Create your views here.


@login_required(login_url='login')
def home_page(request):
    if request.user.is_authenticated:
        user = request.user
        form = TaskForm()
        tasks = task.objects.filter(user = user).order_by('priority')

    return render(request, 'index.html', context={'form' : form, 'tasks' : tasks})


def signup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('password2')

        if password==password2:
            my_user = User.objects.create_user(name, email, password)
            my_user.save()
            return redirect('login') # Redirect to the 'login' URL pattern
        else:
            return HttpResponse('Something wrong with your email')
        
    return render(request, 'signup.html')


def login_page(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') # Redirect to the 'home' URL pattern
        else:
            return HttpResponse('Invalid credentials')
        
    return render(request, 'login.html')



def logout_page(request):
    logout(request)
    return redirect('login')

def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TaskForm(request.POST)
        if form.is_valid:
            todo = form.save(commit=False)
            todo.user =user
            todo.save()
            return redirect('home')
        

def delete_task(request, id):
    task.objects.get(pk = id).delete()
    return redirect('home')


def change_task(request, id, status):
    tsk = task.objects.get(pk = id)
    tsk.status = status
    tsk.save()
    return redirect('home')