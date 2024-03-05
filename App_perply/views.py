from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from Apptutor.models import Student, Tutor
from App_perply.serializers import StudentSerializer, TutorSerializer



@csrf_exempt
def StudentApi(request, id=0):
    if request.method == 'GET':
        students = Student.objects.all()
        student_serializer = StudentSerializer(students, many=True)
        return JsonResponse(student_serializer.data, safe=False)
    elif request.method == 'POST':
        student_data = JSONParser().parse(request)
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        student_data = JSONParser().parse(request)
        try:
            student = Student.objects.get(StudentId=student_data['StudentId'])
        except Student.DoesNotExist:
            return JsonResponse("Student not found", status=404)
        student_serializer = StudentSerializer(student, data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", status=400)
    elif request.method == 'DELETE':
        student_data = JSONParser().parse(request)
        try:
            student = Student.objects.get(StudentId=student_data['StudentId'])
        except Student.DoesNotExist:
            return JsonResponse({"message": "Student not found"}, status=404)
        student.delete()
        return JsonResponse({"message": "Deleted Successfully"}, safe=False)
    
@csrf_exempt
def TutorApi(request, id=0):
    if request.method == 'GET':
        tutors = Tutor.objects.all()
        tutor_serializer = TutorSerializer(tutors, many=True)
        return JsonResponse(tutor_serializer.data, safe=False)
    elif request.method == 'POST':
        tutor_data = JSONParser().parse(request)
        tutor_serializer = TutorSerializer(data=tutor_data)
        if tutor_serializer.is_valid():
            tutor_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse(tutor_serializer.errors, status=400)
    elif request.method == 'PUT':
        tutor_data = JSONParser().parse(request)
        try:
            tutor = Tutor.objects.get(TutorId=tutor_data['TutorId'])
        except Tutor.DoesNotExist:
            return JsonResponse("Tutor not found", status=404)
        tutor_serializer = TutorSerializer(tutor, data=tutor_data)
        if tutor_serializer.is_valid():
            tutor_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse(tutor_serializer.errors, status=400)
    elif request.method == 'DELETE':
        tutor_data = JSONParser().parse(request)
        try:
            tutor = Tutor.objects.get(TutorId=tutor_data['TutorId'])
        except Tutor.DoesNotExist:
            return JsonResponse({"message": "tutor not found"}, status=404)
        tutor.delete()
        return JsonResponse({"message": "Deleted Successfully"}, safe=False)





