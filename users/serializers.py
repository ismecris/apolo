from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone', 'department', 'company', 'avatar')
        read_only_fields = ('id',)


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'role', 'phone', 'department', 'company')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = User
        fields = ('username', 'email', 'password', 'role', 'department')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
