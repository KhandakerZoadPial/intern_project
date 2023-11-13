from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from django.contrib.auth.decorators import login_required
import random
import string


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        context = {

        }
        user = request.user

        if Student.objects.filter(user=user).count() > 0:
            
            context['type'] = 'Student'
            context['profile'] = Student.objects.filter(user=user)[0]
        elif  Professor.objects.filter(user=user).count() > 0:
            context['type'] = 'Professor'
            context['profile'] = Professor.objects.filter(user=user)[0]
            my_students = Student.objects.filter(my_professor=context['profile'])
            context['my_students'] = my_students
        elif Company.objects.filter(user=user).count() > 0:
            print('yes')
            context['type'] = 'Company'
            context['profile'] = Company.objects.filter(user=user)[0]
            context['jobs'] = Jobs.objects.filter(posted_by=context['profile']).order_by('-pk')
        
        return render(request, 'mainapp/home.html', context)
    return redirect('login')


@login_required(login_url='login')
def add_student(request):
    user = request.user
    if  Professor.objects.filter(user=user).count() > 0:
        profile = Professor.objects.filter(user=user)[0]
        student_email = request.POST.get('student_email')

        student_user = User()
        student_user.username = student_email
        password = generate_password()
        student_user.set_password(password)
        student_user.save()

        print(student_email, password)
        

        student_profile = Student()
        student_profile.user = student_user
        student_profile.email = student_email
        student_profile.my_professor = profile
        student_profile.save()

        # now send the email to the student
        # -----------

    return redirect('home')


@login_required(login_url='login')
def post_jobs(request):
    user = request.user
    if Company.objects.filter(user=user).count() > 0:
        profile = Company.objects.filter(user=user)[0]

        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        number_of_vaccencies = request.POST.get('number_of_vaccencies')
        job_location = request.POST.get('job_location')

        job = Jobs()
        job.posted_by = profile
        job.job_title = job_title
        job.job_description = job_description
        job.job_location = job_location
        job.number_of_vaccencies = int(number_of_vaccencies)
        job.save()
    
    return redirect('/')


@login_required(login_url='login')
def delete_job(request, job_id):
    user = request.user
    if Company.objects.filter(user=user).count() > 0:
        profile = Company.objects.filter(user=user)[0]
        job = Jobs.objects.get(pk=job_id)
        if job.posted_by == profile:
            job.delete()
    
    return redirect('home')

@login_required(login_url='login')
def view_a_job(request, job_id):
    context = {

    }
    user = request.user
    context['owner'] = False
    context['the_job'] = Jobs.objects.get(pk=job_id)

    if Student.objects.filter(user=user).count() > 0:
        context['type'] = 'Student'
        context['profile'] = Student.objects.filter(user=user)[0]
    elif  Professor.objects.filter(user=user).count() > 0:
        context['type'] = 'Professor'
        context['profile'] = Professor.objects.filter(user=user)[0]
    elif Company.objects.filter(user=user).count() > 0:
        context['type'] = 'Company'
        context['profile'] = Company.objects.filter(user=user)[0]
        if context['the_job'].posted_by == context['profile']:
            context['owner'] = True
    
    

    return render(request, 'mainapp/view_a_job.html', context)


@login_required(login_url='login')
def apply_to_job(request, job_id):
    user = request.user
    if Student.objects.filter(user=user).count() > 0:
        profile = Student.objects.filter(user=user)[0]

        the_job = Jobs.objects.filter(pk=job_id)
        if the_job.count() > 0:
            the_job = the_job[0]
            the_job.applied_bys.add(profile)
            the_job.save()
        else:
            # the job does not exists or deleted
            pass
    return redirect('home')

@login_required(login_url='login')
def browse_jobs(request):
    context = {

    }
    user = request.user

    if Student.objects.filter(user=user).count() > 0:
        context['type'] = 'Student'
        context['profile'] = Student.objects.filter(user=user)[0]
    elif  Professor.objects.filter(user=user).count() > 0:
        context['type'] = 'Professor'
        context['profile'] = Professor.objects.filter(user=user)[0]
        my_students = Student.objects.filter(my_professor=context['profile'])
        context['my_students'] = my_students
    elif Company.objects.filter(user=user).count() > 0:
        context['type'] = 'Company'
        context['profile'] = Company.objects.filter(user=user)[0]
        context['jobs'] = Jobs.objects.filter(posted_by=context['profile']).order_by('-pk')

    context['all_jobs'] = Jobs.objects.all().order_by('-pk')
    
    return render(request,'mainapp/browse_jobs.html', context)

# helpers
def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(6))
    return password