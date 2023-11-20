from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from django.contrib.auth.decorators import login_required
import random
import string
from django.contrib import messages


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        context = {

        }
        user = request.user

        if Student.objects.filter(user=user).count() > 0:
            
            context['type'] = 'Student'
            context['profile'] = Student.objects.filter(user=user)[0]
            context['notifications'] = NotificationS.objects.filter(student=context['profile']).order_by('-pk')
            try:
                context['selections'] = Selection.objects.filter(selected_student=context['profile'])[0]
                context['feedbacks'] = StudentFeedback.objects.filter(selection=context['selections'], student=context['profile'])
            except:
                pass
            context['my_applications'] = Jobs.objects.filter(applied_bys= context['profile'] )
            
        elif  Professor.objects.filter(user=user).count() > 0:
            context['type'] = 'Professor'
            context['profile'] = Professor.objects.filter(user=user)[0]
            my_students = Student.objects.filter(my_professor=context['profile']).order_by('-pk')
            
            s_temp = []
            for s in my_students:
                s.feebacks_set = StudentFeedback.objects.filter(student=s) 
                s_temp.append(s)
            
            context['my_students'] = s_temp
            context['notifications'] = NotificationP.objects.filter(student=context['profile']).order_by('-pk')
            # context['my_applied_jobs'] = Jobs
        elif Company.objects.filter(user=user).count() > 0:
            print('yes')
            context['type'] = 'Company'
            context['profile'] = Company.objects.filter(user=user)[0]
            context['jobs'] = Jobs.objects.filter(posted_by=context['profile']).order_by('-pk')
            context['notifications'] = NotificationC.objects.filter(student=context['profile']).order_by('-pk')
        
        return render(request, 'mainapp/home.html', context)
    return redirect('login')


@login_required(login_url='login')
def add_student(request):
    user = request.user
    if  Professor.objects.filter(user=user).count() > 0:
        profile = Professor.objects.filter(user=user)[0]
        student_email = request.POST.get('student_email')

        if User.objects.filter(username=student_email).count() > 0:
            messages.success(request, 'The Email is Already Registered!')
            return redirect('home')

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
        student_profile.major = request.POST.get('student_major')
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
        # job_description = request.POST.get('job_description')
        number_of_vaccencies = request.POST.get('number_of_vaccencies')
        job_location = request.POST.get('job_location')
        major = request.POST.get('major')

        job = Jobs()
        job.posted_by = profile
        job.job_title = job_title
        # job.job_description = job_description
        job.job_location = job_location
        job.number_of_vaccencies = int(number_of_vaccencies)
        job.major = major
        job.performance_type = request.POST.get('performance_type')
        job.save()

        messages.success(request, 'Successfully Posted The Job!')
    
    return redirect('/')


@login_required(login_url='login')
def delete_job(request, job_id):
    user = request.user
    if Company.objects.filter(user=user).count() > 0:
        profile = Company.objects.filter(user=user)[0]
        job = Jobs.objects.get(pk=job_id)
        if job.posted_by == profile:
            job.delete()
            messages.success(request, 'Successfully Deleted The Job!')
    
    return redirect('home')

@login_required(login_url='login')
def view_a_job(request, job_id):
    context = {

    }
    user = request.user
    context['owner'] = False
    context['job'] = Jobs.objects.get(pk=job_id)

    if Student.objects.filter(user=user).count() > 0:
        context['type'] = 'Student'
        context['profile'] = Student.objects.filter(user=user)[0]
        context['notifications'] = NotificationS.objects.filter(student=context['profile']).order_by('-pk')
    elif  Professor.objects.filter(user=user).count() > 0:
        context['type'] = 'Professor'
        context['profile'] = Professor.objects.filter(user=user)[0]
        context['notifications'] = NotificationP.objects.filter(student=context['profile']).order_by('-pk')
    elif Company.objects.filter(user=user).count() > 0:
        context['type'] = 'Company'
        context['profile'] = Company.objects.filter(user=user)[0]
        context['notifications'] = NotificationC.objects.filter(student=context['profile']).order_by('-pk')
        if context['job'].posted_by == context['profile']:
            context['owner'] = True
            context['selections'] = Selection.objects.filter(job=context['job'])
    
    

    return render(request, 'mainapp/view_a_job.html', context)


@login_required(login_url='login')
def apply_to_job(request, job_id):
    user = request.user
    if Student.objects.filter(user=user).count() > 0:
        profile = Student.objects.filter(user=user)[0]

        the_job = Jobs.objects.filter(pk=job_id)
        if the_job.count() > 0:
            if Selection.objects.filter(selected_student=profile).count() == 0:
                the_job = the_job[0]
                the_job.applied_bys.add(profile)
                the_job.save()

                n = NotificationC()
                n.job = the_job
                n.student = the_job.posted_by
                n.message = f'{profile.user.username} applied for "{the_job.job_title}"'
                n.save()
                messages.success(request, 'Successfully Applied To The Job!')
            else:
                messages.success(request, f'You are already selected for training at {the_job[0].posted_by.name}')
        else:
            # the job does not exists or deleted
            pass
    return redirect('home')


@login_required(login_url='login')
def update_resume(request):
    user = request.user
    if Student.objects.filter(user=user).count() > 0:
        profile = Student.objects.filter(user=user)[0]
        resume = request.FILES.get('resume')

        profile.student_resume = resume
        profile.save()
    return redirect('home')


def browse_jobs(request):
    context = {

    }
    user = request.user
    if user.is_authenticated:
        if Student.objects.filter(user=user).count() > 0:
            context['type'] = 'Student'
            context['profile'] = Student.objects.filter(user=user)[0]
            context['notifications'] = NotificationS.objects.filter(student=context['profile']).order_by('-pk')
        elif  Professor.objects.filter(user=user).count() > 0:
            context['type'] = 'Professor'
            context['profile'] = Professor.objects.filter(user=user)[0]
            my_students = Student.objects.filter(my_professor=context['profile'])
            context['my_students'] = my_students
            context['notifications'] = NotificationP.objects.filter(student=context['profile']).order_by('-pk')
        elif Company.objects.filter(user=user).count() > 0:
            context['type'] = 'Company'
            context['profile'] = Company.objects.filter(user=user)[0]
            context['jobs'] = Jobs.objects.filter(posted_by=context['profile']).order_by('-pk')
            context['notifications'] = NotificationC.objects.filter(student=context['profile']).order_by('-pk')
    else:
        pass

    context['all_jobs'] = Jobs.objects.all().order_by('-pk')
    
    return render(request,'mainapp/browse_jobs.html', context)



@login_required(login_url='login')
def select_student(request, job_id, student_id):
    user = request.user

    if Company.objects.filter(user=user).count() > 0:
        profile = Company.objects.filter(user=user)[0]
        job = Jobs.objects.get(pk=job_id)
        student = Student.objects.get(pk=student_id)
        if job.posted_by == profile:
            s = Selection()
            s.job = job
            s.selected_student = student
            s.save()
            student.status = True
            student.save()

            n = NotificationS()
            n.job = job
            n.student = student
            n.message = f'Congratulations! You Have been selected for training at "{job.posted_by.name}" for "{job.job_title}"'
            n.save()

            n = NotificationP()
            n.job = job
            n.student = student.my_professor
            n.message = f'Congratulations! Your Student {student.user.username} has been selected for training at "{job.posted_by.name}" for "{job.job_title}"'
            n.save()
            messages.success(request, 'Student Selected!')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def send_feedback(request, student_id, job_id):
    message = request.POST.get('message')
    sf = StudentFeedback()
    sf.student = Student.objects.get(pk=student_id)
    sf.selection = Selection.objects.get(selected_student=Student.objects.get(pk=student_id), job=Jobs.objects.get(pk=job_id))
    sf.message = message
    sf.save()

    return redirect('home')

# helpers
def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(6))
    return password