# from asyncio.windows_events import NULL
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Sql(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    query1 = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, related_name="queries" ,on_delete=models.SET_NULL, null=True)
    output = models.CharField(max_length=255, null=True)

    # def __str__(self):
    #     return self.query1
