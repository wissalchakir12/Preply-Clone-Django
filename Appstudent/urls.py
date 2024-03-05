from django.contrib import admin
from django.urls import path ,include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('findtutor/', views.findtutor, name='findtutor'),
    path('logout/', views.logout, name='logout'),
    path('logout_student/', views.logout_student, name='logout_student'),
    path('tutor_video/<str:email>', views.tutor_video, name='tutor_video'),
   
]