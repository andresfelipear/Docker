from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
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
            password=request.POST['password']
        )

        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), "errMsg":'Username and password are incorrect'})
        else:
            login(request,user)
            return redirect('currenttodos')

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')