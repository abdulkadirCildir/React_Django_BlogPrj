from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# class ProfileSerializer
class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = (
        "username",
        "email"
    )

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='user-profile',
        lookup_field='id'
    )
    
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "image",
            "bio",
            "detail_url"
        )
        lookup_field = "id"

class ProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    update_url = serializers.HyperlinkedIdentityField(
        view_name='user-profile-update',
        lookup_field='id'
    )
    
    class Meta:
        model = Profile
        fields = (
            "user",
            "image",
            "bio",
            "update_url"        
        )
        lookup_field = "id"
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'image', 
            'bio'
        )        
    

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user