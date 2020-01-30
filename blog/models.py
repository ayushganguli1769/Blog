from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
class article(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(null= True, max_length= 100)
    description = models.TextField(null= True, blank= True)
    image = models.FileField(null= True, blank= True)
    time = models.DateTimeField(auto_now_add = True )
    private = models.BooleanField(default= False)
    def __str__(self):
        return self.user.username + " Article " + str(self.id)
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id')