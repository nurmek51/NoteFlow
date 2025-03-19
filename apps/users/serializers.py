from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.users.models import EmailVerificationToken

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {"password": {"write_only": True}, "username": {"required": True}, "email": {"required": True}}

    def validate_email(self, value):
        if not value.endswith("@sdu.edu.kz"):
            raise serializers.ValidationError("Регистрация возможна только с почтой @sdu.edu.kz")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован.")
        return value

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password and password2:
            if data['password'] != data['password2']:
                raise serializers.ValidationError({'password': 'Passwords do not match'})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password confirmation

        # Generate verification code and cache user data for later verification
        verification_code = get_random_string(32)
        cache.set(verification_code, validated_data, timeout=86400)  # Store for 24 hours

        confirm_link = f"http://127.0.0.1:8000/api/verify-email/{verification_code}/"
        send_mail(
            subject="Подтверждение Email",
            message=f"Привет {validated_data['username']}! Подтвердите ваш email: {confirm_link}",
            from_email="noreply@sdu.edu.kz",
            recipient_list=[validated_data['email']],
        )

        return {
            "message": "На ваш email отправлено письмо для подтверждения.",
            "username": validated_data["username"],
            "email": validated_data["email"]
        }


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
