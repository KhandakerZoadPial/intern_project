from django.db import models
from accounts.models import *

# Create your models here.
class Jobs(models.Model):
    posted_by = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    job_title = models.TextField(blank=True)
    job_description = models.TextField(blank=True)
    job_location = models.TextField(blank=True)
    number_of_vaccencies = models.IntegerField(default=1)
    applied_bys = models.ManyToManyField(Student, blank=True, null=True)
    date_posted = models.DateField(auto_now_add=True)
    major = models.TextField(blank=True)
    performance_type = models.TextField(blank=True)
    

class Selection(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, blank=True, null=True)
    selected_student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    approved_by_professor = models.BooleanField(default=False)


class NotificationS(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    when = models.DateTimeField(auto_now_add=True)


class NotificationP(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    student = models.ForeignKey(Professor, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    when = models.DateTimeField(auto_now_add=True)


class NotificationC(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    student = models.ForeignKey(Company, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    when = models.DateTimeField(auto_now_add=True)


class StudentFeedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    when = models.DateTimeField(auto_now_add=True)