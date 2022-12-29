from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if not validated_data.get('is_admin'):
            validated_data['is_admin'] = False
        user = User(
            username=validated_data['username'],
            is_admin=validated_data['is_admin']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
