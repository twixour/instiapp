from django.db import models
from user.models import User
# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="todos")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
    