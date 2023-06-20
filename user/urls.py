from django.urls import path,include

from rest_framework.authtoken.views import obtain_auth_token


from .views import (
    registration_view,
    profile_creation_view,
    profile_list,
    profile_edit,
    delete_user,
    student_list,
    student_detail,
)

urlpatterns = [
    
    path('register', registration_view , name='register'),
    path('login', obtain_auth_token, name='login'),

    path('students-list',student_list,name='students-list'),
    path('student-detail/<int:id>',student_detail,name='student-detail'),

    path('create-profile/<int:id>', profile_creation_view, name='create-profile'),
    
    path('profile_list', profile_list, name='profile_list'),
    path('profile-edit', profile_edit, name='profile-edit' ),
    path('delete/<int:id>',delete_user,name='user-delete'),
]
