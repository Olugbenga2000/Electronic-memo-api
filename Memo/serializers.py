from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import Memo, Department, StarMemo, ReadMemo, Staff


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name', 'pk')


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ('department',)
        depth = 1


class StarMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarMemo
        fields = ('user', 'isStarred')


class ReadMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadMemo
        fields = ('user', 'isRead', 'created_at')


# class Memo_Attachments_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attachments
#         fields = ('id', 'images')

class UserSerializer(serializers.ModelSerializer):
    users = StaffSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'users')


class MemoSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Memo
        fields = '__all__'
        depth = 1


# User Serializer


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'password', 'first_name', 'last_name', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True},
                        'is_superuser': {}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'],
            validated_data['first_name'], validated_data['last_name'])

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = "User is deactivated."
                    raise raise_exceptions.ValidationError(msg)
            else:
                msg = "Incorrect password or username."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data
