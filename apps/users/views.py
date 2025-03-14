from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer, UserUpdateSerializer
from .models import User
from rest_framework.permissions import AllowAny

from ..materials.models import Lecturer, Subject
from ..materials.serializers import SubjectSerializer, LecturerSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handles user registration by validating and creating a new user.
            """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "username": user.username
            },
            status=status.HTTP_201_CREATED
        )

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
