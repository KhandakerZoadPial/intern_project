from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        user = authenticate(username=username, password=password)
        # u = User.objects.all()[0]
        # u.set_password('ppppp111')
        # u.save()
      

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'Successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Please provide valid credentials!')
            return redirect('login')
    
    else:
        return render(request, 'accounts/login.html')


def student_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is Already Taken.')
            return redirect('student_signup')
        else:
            user = User()
            user.username = username
            user.set_password(password)
            user.save()
            student = Student()
            student.user = user
            student.email = request.POST.get('email')
            student.name = request.POST.get('full_name')
            student.gender = request.POST.get('gender')
            student.picture = request.FILES.get('picture')
            student.save()
            messages.success(request, 'Account Created Successfully.')
            return redirect('login')

    return render(request, 'accounts/student_signup.html')


def professor_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is Already Taken.')
            return redirect('student_signup')
        else:
            user = User()
            user.username = username
            user.set_password(password)
            user.save()
            student = Professor()
            student.user = user
            student.email = request.POST.get('email')
            student.name = request.POST.get('full_name')
            student.gender = request.POST.get('gender')
            student.picture = request.FILES.get('picture')
            student.save()
            messages.success(request, 'Account Created Successfully.')
            return redirect('login')

    return render(request, 'accounts/professor_signup.html')


def company_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is Already Taken.')
            return redirect('company_signup')
        else:
            user = User()
            user.username = username
            user.set_password(password)
            user.save()
            student = Company()
            student.user = user
            student.email = request.POST.get('email')
            student.name = request.POST.get('full_name')
            student.picture = request.FILES.get('picture')
            student.save()
            messages.success(request, 'Account Created Successfully.')
            return redirect('login')

    return render(request, 'accounts/company_signup.html')


@login_required(login_url='login')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('login')


@login_required(login_url='login')
def update_profile(request):
    user = request.user
    if Student.objects.filter(user=user).count() > 0:
        profile = Student.objects.filter(user=user)[0]
    elif  Professor.objects.filter(user=user).count() > 0:
        profile = Professor.objects.filter(user=user)[0]
    elif Company.objects.filter(user=user).count() > 0:
        profile = Company.objects.filter(user=user)[0]
    
    profile.name = request.POST.get('name')
    profile.email = request.POST.get('email')

    if request.FILES.get('picture'):
        profile.picture = request.FILES.get('picture')
    
    profile.save()
    return redirect('home')


@login_required(login_url='login')
def change_passowrd(request):
    user = request.user
    user.set_password(request.POST.get('password'))
    user.save()

    return redirect('home')