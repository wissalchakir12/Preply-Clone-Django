from django.conf import settings
from django.contrib import admin
from django.urls import path ,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static






urlpatterns = [
    path('become_tutor/', views.become_tutor, name='become_tutor'),
    path('tutor_signup/', views.tutor_signup, name='tutor_signup'),
    path('logout/', views.logout_view, name='logout'),
    path('lessons/', views.lessons, name='lessons'),
    path('add_lessons/', views.add_lessons, name='add_lessons'),
    path('', include('Appstudent.urls'))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)