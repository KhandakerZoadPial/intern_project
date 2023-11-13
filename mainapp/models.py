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
