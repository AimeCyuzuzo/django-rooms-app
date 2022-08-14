from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from traitlets import default




class Topic(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Profile(models.Model):
    owner = models.OneToOneField(User, blank=True,null=True, on_delete=models.CASCADE)
    profilePicture = models.ImageField(default='avatar.png',null=True,blank=True)
    bio = models.TextField(null=True, blank=True)
    firstname = models.CharField(max_length=35,null=True)
    othernames = models.CharField(max_length=35, null=True)
    gender = models.CharField(max_length=6,null=True)
    age = models.CharField(max_length=3,null=True)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.email


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']


    def __str__(self):
        return self.name



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

