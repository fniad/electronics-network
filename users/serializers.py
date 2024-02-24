""" Сериалайзеры для users """
from rest_framework import serializers

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """ Сериалайзер пользователя """
    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'is_superuser']