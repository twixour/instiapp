from django.urls import path
from .views import (
    get_todo,
    create_todo,
    update_todo,
    delete_todo,
)
urlpatterns = [
    
    path('list', get_todo, name='todo'),
    path('create', create_todo, name='create'),
    path('update/<int:id>', update_todo, name='update'),
    path('delete/<int:id>', delete_todo,name='delete'),
]
