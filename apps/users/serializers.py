from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email','password','password2']


    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password and password2:
            if data['password'] != data['password2']:
                raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture', 'favorite_lecturer', 'favorite_subjects']


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()  # ✅ Correct: Directly call save() on the instance
        return instance