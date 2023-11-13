from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('add_student', views.add_student, name='add_student'),
   path('post_jobs', views.post_jobs, name='post_jobs'),
   path('delete_job/<int:job_id>', views.delete_job, name='delete_job'),
   path('apply_to_job/<int:job_id>', views.apply_to_job, name='apply_to_job'),
   path('view_a_job/<int:job_id>', views.view_a_job, name='view_a_job'),
   path('browse_jobs', views.browse_jobs, name='browse_jobs')
   
]