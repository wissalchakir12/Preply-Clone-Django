from django.db import models
from django import forms
import pytz
from django_countries.fields import CountryField
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    StudentId = models.AutoField(primary_key=True)
    photo = models.ImageField(null=True, blank=True)
    FirstName = models.CharField(max_length=200, null = False)
    LastName = models.CharField(max_length=200, null = True)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=128, null = True)

    def __str__(self):
        return self.StudentId


class Tutor(models.Model):
    TutorId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=200, null = False)
    LastName = models.CharField(max_length=200, null = False)
    Email = models.EmailField(max_length=200)
    Password = forms.CharField(widget=forms.PasswordInput, max_length=128)

    def __str__(self):
        return self.TutorId




class Video(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Videos"
