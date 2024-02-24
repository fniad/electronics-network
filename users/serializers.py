""" Сериалайзеры для users """
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """ Сериалайзер пользователя """
    class Meta:
        model = User
        fields = ['username', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
