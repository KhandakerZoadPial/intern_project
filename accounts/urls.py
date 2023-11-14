from django.urls import path
from . import views

urlpatterns = [
   path('login', views.login, name='login'),
   path('student_signup', views.student_signup, name='student_signup'),
   path('user_logout', views.user_logout, name='user_logout'),
   path('professor_signup', views.professor_signup, name='professor_signup'),
   path('company_signup', views.company_signup, name='company_signup'),
   path('update_profile', views.update_profile, name='update_profile'),
   path('change_passowrd', views.change_passowrd, name='change_passowrd')
]