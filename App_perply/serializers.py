from rest_framework import serializers
from Apptutor.models import Student, Tutor

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields=('StudentId','FirstName','LastName','Email','Password')

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields=('TutorId','FirstName','LastName','Email','Password')