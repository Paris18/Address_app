
# django imports
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

# app level imports
from .models import Address


class AddressCreateSerializer(serializers.ModelSerializer):
    """
    Creating the new address
    """
    name = serializers.CharField(required=True, min_length=2)
    address = serializers.CharField(required=True, min_length=5)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Address
        fields = ('id', 'name', 'address', 'user', )

    def create(self, validated_data):
        user = Address.objects.create(**validated_data)
        return user


class ListAddressSerializer(serializers.ModelSerializer):
    """
    list the addresses
    """
    class Meta:
        model = Address
        fields = ('id','name','address',)

class UpdateAddressSerializer(serializers.ModelSerializer):
    """
    update the given address
    """
    name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = ('id','name','address',)

    def validate(self, data):
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.address = validated_data.get('address',instance.name)
        instance.save()
        return instance