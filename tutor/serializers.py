from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class userserializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class studentprofileserializer(serializers.ModelSerializer):

    user = userserializer(read_only = True)

    class Meta:
        model = studentprofile
        fields = '__all__'

class learninglogserializer(serializers.ModelSerializer):

    class Meta:
        model = learningLog
        fields = '__all__'
