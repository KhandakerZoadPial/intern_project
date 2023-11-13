from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    picture = models.ImageField(upload_to='professor_images/', blank=True, null=True)
    gender = models.CharField(max_length=20,  blank=True, null=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    picture = models.ImageField(upload_to='student_images/', blank=True, null=True)
    gender = models.CharField(max_length=20,  blank=True, null=True)
    my_professor = models.ForeignKey(Professor, blank=True, null=True, on_delete=models.CASCADE)
    student_resume = models.FileField(upload_to='student_resumes/', blank=True, null=True)
    status = models.BooleanField(default=False)


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    picture = models.ImageField(upload_to='company_images/', blank=True, null=True)

