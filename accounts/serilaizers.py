# django imports
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

# app level imports
from .models import (
                    Profile,
                    )




class UserLoginRequestSerializer(serializers.Serializer):
    """
    UserLoginSerializer
    """
    mobile = serializers.IntegerField(
        required=False,
        min_value=5000000000,
        max_value=9999999999,
    )
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True, min_length=5)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'is_verified', 'is_active', 'email'
        )


class UserRegSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        )
    password = serializers.CharField(required=True, min_length=5)
    first_name = serializers.CharField(required=True, min_length=2)
    last_name = serializers.CharField(required=True, min_length=2)
    mobile = serializers.IntegerField(
        required=True,
        min_value=5000000000,
        max_value=9999999999,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    class Meta:
        model = User
        fields = ('id', 'password', 'email', 'first_name', 'last_name',"mobile")
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self,data):
        print(data)
        return data


    def create(self, validated_data):
        mobile = validated_data.pop('mobile')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.mobile = mobile
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active','username')


class UserUpdateRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    email = serializers.EmailField(required=False)


    def validate(self,data):
        return data

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name','is_active')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

class UserPassUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','password',)
    
    def validate(self,data):
        return data

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance



class ProfileListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'mobile', 'gender', 'profile_image','user')

class ProfileUpdateSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(required=False)
    user = UserListSerializer(required=False)
    profile_image = serializers.ImageField(required=False)
    mobile = serializers.IntegerField(
        required=False,
        min_value=5000000000,
        max_value=9999999999,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )


    def validate(self,data):
        return data

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ('id', 'mobile', 'gender', 'profile_image','user')