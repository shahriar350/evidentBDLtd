from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class UserInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="get_user_input")
    input = models.IntegerField()
    date_created = models.DateTimeField()
