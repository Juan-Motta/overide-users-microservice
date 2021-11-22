from rest_framework import serializers
from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for GET methods.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',
            'last_name',
            'document',
            'birth',
            'phone',
            'is_active',
            'is_staff',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for POST method.
    """
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
            'last_name',
            'document',
            'password',
            'birth',
            'phone',
        ]

    # Hash the password when the register is created
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for PUT method.
    """
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'last_name',
            'document',
            'birth',
            'phone',
        ]


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for PUT method.
    """
    class Meta:
        model = User
        fields = [
            'password',
        ]

    # Hash the password when the register is updated
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user
