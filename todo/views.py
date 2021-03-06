from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', { 'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'],"", request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signup.html', {'form':UserCreationForm(), 'errMsg':"The username already exist. try another one!"})
            
        else:
            return render(request, 'todo/signup.html', {'form':UserCreationForm(), 'errMsg':"The password and verification are diferents, try again!"})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, 'todo/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', { 'form': AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST['username'], 
            password=request.POST['password1']
        )

        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), "errMsg":'Username and password are incorrect'})
        else:
            login(request,user)
            return redirect('currenttodos')

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def createtodos(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', { 'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            render(request, "todo/createtodo.html",{ 'form': TodoForm(), 'errMsg':'Bad data passed in. try again'})

@login_required
def viewtodo(request, todo_id):
    todo = get_object_or_404(Todo,pk=todo_id,user=request.user)
    if request.method == "GET":
        form = TodoForm(request.POST, instance=todo) ####
        return render(request, 'todo/viewtodo.html',{'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'errMsg':'Bad information...'} )

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def completetodo(request, todo_id):
    todo = get_object_or_404(Todo,pk=todo_id,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_id):
    todo = get_object_or_404(Todo,pk=todo_id,user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

def handler404(request, exception):
    return render(request, '404.html', status=404)
