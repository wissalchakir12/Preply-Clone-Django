from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from Apptutor.models import Student, Tutor



def Navbar(request):
    context={}
    return render(request,'Navbar.html',context)

def findtutor2(request):
    context={}
    return render(request,'findtutor2.html',context)
def findtutor3(request):
    context={}
    return render(request,'findtutor3.html',context)