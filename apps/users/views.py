from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer, UserUpdateSerializer, ProfilePictureSerializer
from .models import User, EmailVerificationToken
from rest_framework.permissions import AllowAny

from ..materials.models import Lecturer, Subject
from ..materials.serializers import SubjectSerializer, LecturerSerializer


User = get_user_model()

class VerifyEmailView(APIView):
    def get(self, request, verification_code):
        user_data = cache.get(verification_code)

        if not user_data:
            return Response({"error": "Срок действия ссылки истек или она недействительна."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(**user_data, is_active=True)

        # Remove cached data
        cache.delete(verification_code)

        return Response({"message": "Email подтвержден! Теперь вы можете войти."}, status=status.HTTP_201_CREATED)



class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()  # Это наш `return {...}` в `create()`

        return Response(response_data, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        #by id
        user = self.request.user
        searching_user = self.get_object()
        serializer = UserUpdateSerializer(searching_user)
        data = serializer.data
        if data["username"] == user.username:

            favorite_subjects = SubjectSerializer(searching_user.favorite_subjects.all(), many=True).data
            favorite_lecturer = LecturerSerializer(searching_user.favorite_lecturer).data if searching_user.favorite_lecturer else None

            filtered_data = {
                "username": data.get("username"),
                "email": data.get("email"),
                "profile_picture": data.get("profile_picture"),
                "bio": data.get("bio"),
                "favorite_subject": favorite_subjects,
                "favorite_lecturer": favorite_lecturer,
            }
            return Response(filtered_data, status=status.HTTP_200_OK)
        return Response({'message': "You cannot see data of other people"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = self.request.user
        user_serializer = self.get_serializer(user)
        user_data = user_serializer.data

        changing_user = self.get_object()
        serializer = UserUpdateSerializer(changing_user, data=request.data, partial=True)
        if serializer.is_valid():
            if user_data['username'] == changing_user.username:
                serializer.save()
                return Response(serializer.data)
            return Response({'message': "You cannot change data of other people"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        user = self.request.user
        deleting_user = self.get_object()
        serializer = self.get_serializer(user)
        data = serializer.data
        if data['username'] == deleting_user.username:
            user.delete()
            return Response({"message":"User deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': "You cannot delete account of other people"}, status=status.HTTP_400_BAD_REQUEST)


class UserFavoriteSubjectsUpdateDeleteView(APIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        """
                ✅ Обновление любимых предметов.
                Ожидает в теле запроса {"subject_id": 1}, где 1 - id subjecta.
        """
        user = request.user
        subject_id = request.data.get('subject_id')

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({'message': "Subject doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

        if subject_id not in user.favorite_subjects.all():
            return Response({'message': "This subject is already your favorite subject"}, status=status.HTTP_400_BAD_REQUEST)

        user.favorite_subjects.add(subject)
        user.save()
        return Response({'message': f"Subject {subject.name} added to favorites"}, status=status.HTTP_200_OK)


    def delete(self, request):
        user = request.user
        subject_id = request.data.get('subject_id')

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({'message': "Subject doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

        if subject_id not in user.favorite.subjects.all():
            return Response({'message': "This subject is not in your favorite subjects list"}, status=status.HTTP_400_BAD_REQUEST)
        user.favorite.subjects.remove(subject)
        return Response({'message': f"Subject {subject.name} deleted successfully"}, status=status.HTTP_200_OK)

class UserFavoriteLecturerUpdateDeleteView(generics.GenericAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request):
        """
                ✅ Обновление любимого преподавателя.
                Ожидает в теле запроса {"lecturer_id": 1}, где 1 - id преподавателя.
        """
        user = self.get_object()
        lecturer_id = request.data.get('lecturer_id')
        try:
            lecturer = Lecturer.objects.get(id=lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({'message': "Lecturer doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        user.favorite_lecturer = lecturer
        user.save()
        return Response({'message': "Lecturer updated successfully"}, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.favorite_lecturer is None:
            return Response({'message': "You already do not have lecturer"}, status=status.HTTP_400_BAD_REQUEST)
        user.favorite_lecturer = None
        user.save()
        return Response({'message': "Lecturer deleted successfully"}, status=status.HTTP_200_OK)


class ProfilePictureUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs ):
        user = request.user
        serializer = ProfilePictureSerializer(user, data=request.data, partial=True)

        if user.profile_picture:
            user.profile_picture.delete(save=False) #s3 delete if its already exists

        if serializer.is_valid():
            serializer.save()
            return Response({'profile_picture_url': user.profile_picture.url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePictureDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request):
        try:
            user = User.objects.get(id=request.user.id)
            if user.profile_picture:
                user.profile_picture.delete(save=False) #s3
                user.profile_picture = None #postgre
                user.save()

            return Response({"message": "Avatar deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
