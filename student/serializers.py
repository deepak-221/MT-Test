from rest_framework import serializers
from .models import StudentClass, User
from django.shortcuts import get_object_or_404

class AddClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentClass
        fields = "__all__"


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password too short.",
        },
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'confirm_password'},
        error_messages={
            "blank": "Confirm password cannot be empty.",
            "min_length": "Confirm_password too short.",
        },
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'is_active',  'image',
                  'student_class', 'password', 'confirm_password']
        read_only_fields = ['is_active']

    def validate(self, data):
        print(data)
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'password and confirm password does not match.'})
        return data

    def create(self, validated_data):
        print(self.context['request'].data['password'])
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            image=validated_data['image'],
            student_class=get_object_or_404(StudentClass, pk=validated_data['student_class']),
        )
        user.set_password(self.context['request'].data['password'])
        user.save()
        return user


class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'image']
