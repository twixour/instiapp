from django.shortcuts import render, get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from .serializers import TodoSerializer 

from .models import Todo, User
# Create your views here.


@api_view(['GET'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated])
def get_todo(request):
    user = request.user
    todos = user.todos.all()
    todosSerializer = TodoSerializer(instance=todos, many=True)

    return Response({
        'todos': todosSerializer.data
    })
    




@api_view(['POST'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated])
def create_todo(request):
    if request.method == "POST":
        user = request.user
        request.data['user'] = user.id
        todo_serializer = TodoSerializer(data = request.data)
        data = {}
        if todo_serializer.is_valid():
            newtodo = todo_serializer.save(user=user)
            data['id'] = newtodo.id
            data['user'] = newtodo.user.id
            data['title'] = newtodo.title
            data['completed'] = newtodo.completed
        else:
            data = todo_serializer.errors
    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated])    
def update_todo(request,id):
    if request.method == "POST":
        user = request.user
        todo = get_object_or_404(Todo,pk=id, user=user)
        request.data['user'] = user.id
        request.data['title'] = todo.title
        todo_serializer = TodoSerializer(instance=todo, data=request.data)
        data = {}
        if(todo_serializer.is_valid()):
            todo_serializer.save()
            data = todo_serializer.data
        else:
            data = todo_serializer.errors
        return Response(data)
    

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication ])
@permission_classes([IsAuthenticated]) 
def delete_todo(request,id):
    user = request.user
    todo = get_object_or_404(Todo, pk=id,user=user)
    if todo:
        todo.delete()
    else:
        return Response({'error':'detail not found'})
    return Response({'response': 'Deleted Successfully'})