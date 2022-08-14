from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique=True)
    name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=200, null=True)
    father = models.CharField(max_length=200, null=True)

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000, null=True)
    description = models.TextField(max_length=2000, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    subs = models.ManyToManyField(User, related_name='subs', blank=True)
    status = models.CharField(max_length=100, default='Збір підписів')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name