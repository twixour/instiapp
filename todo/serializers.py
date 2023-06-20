from rest_framework import serializers
from .models import Todo
from user.models import User

class TodoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Todo
        fields = ['title','user','completed']