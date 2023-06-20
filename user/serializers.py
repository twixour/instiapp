from rest_framework import serializers, viewsets

from .models import Student, StudentProfile

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'password']
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class StudentProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['first_name','last_name','image','student_rkv_id','fathers_name','mothers_name','gender','date_of_birth','age','email','blood_group','class_name','school_name','phone_number','pincode','address','city','state_and_ut','country']


