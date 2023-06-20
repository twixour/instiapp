from django.shortcuts import render, get_object_or_404

from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authtoken.models import Token


from .serializers import StudentSerializer, StudentProfileSerializer

from .models import Student, StudentProfile,User
# Create your views here.

@api_view(['GET'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated])
def student_list(request):
    students = Student.student.all()
    studentsList = {}
    for stud in students:
        studentsList[f'{stud.username}']={
            "id": stud.id,
            "username": stud.username,
            "first_name":stud.studentprofile.first_name,
            "last_name":stud.studentprofile.last_name,
            "gender": stud.studentprofile.gender,
            "age":stud.studentprofile.age,
            "email":stud.studentprofile.email,
            "blood_group":stud.studentprofile.blood_group,
            "phone_number":stud.studentprofile.phone_number,
            "address":stud.studentprofile.address,
            "pincode":stud.studentprofile.pincode,
            "city":stud.studentprofile.city,
            "state_and_ut":stud.studentprofile.state_and_ut,
            "country":stud.studentprofile.country
        }
        
    print(studentsList)
    studentsSerializer = StudentSerializer(instance=students, many=True)
    return Response({
        'students': studentsList
    })


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def student_detail(request,id):
    user = request.user
    if user.username == "devel":
        student = get_object_or_404(Student,pk=id)
        userProfile = student.studentprofile
        prof = StudentProfileSerializer(instance=userProfile)
        print(userProfile)
        return Response(prof.data)
    else:
        prof = StudentProfileSerializer(instance=user.studentprofile)
        return Response(prof.data)

@api_view(['POST',])
def registration_view(request):
    if request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user = account).key
            data['response'] = "Successfully registered a new student."
            data['username'] = account.username
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST',])
def profile_creation_view(request,id):
    student = get_object_or_404(Student, pk=id)
    profile = get_object_or_404(StudentProfile, user = student)
    serializer = StudentProfileSerializer(instance=profile, data = request.data)
    print(profile.id)
    if serializer.is_valid():
        serializer.save()
    return Response({})



@api_view(['GET'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated])
def profile_list(request, format=None):
    user = request.user
    profileSerializer = StudentProfileSerializer(instance = user.studentprofile)
    if profileSerializer.is_valid():
        profileSerializer.save()
    
    return Response(profileSerializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated])
def profile_edit(request, format=None):
    if request.method == "POST":
        user = request.user
        profileSerializer = StudentProfileSerializer(instance = user.studentprofile, data=request.data)
        if profileSerializer.is_valid():
            profileSerializer.save()
    
        return Response(profileSerializer.data)
    


#delete user
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated]) 
def delete_user(request,id):
    #logged in user
    user = request.user
    print(id)
    if (user.username == "devel"):
        print('Username')
        user_delete = get_object_or_404(User, pk=11)
        print('res',user_delete)
        if user_delete:
            user_delete.delete()
        
        else:
            return Response({'error':'detail not found'})
        return Response({'response': 'Deleted Successfully'})
    else:
        return Response({'error':"Admin login required"})