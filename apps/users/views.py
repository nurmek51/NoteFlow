from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserUpdateSerializer
from .models import User
from rest_framework.permissions import AllowAny
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
        serializer = self.get_serializer(user)
        data = serializer.data
        if data["username"] == searching_user.username:

            favourite_subjects = SubjectSerializer(searching_user.favorite_subjects.all(), many=True).data
            favourite_lecturers = LecturerSerializer(searching_user.favorite_lecturers.all(), many=True).data

            filtered_data = {
                "username": data.get("username"),
                "email": data.get("email"),
                "profile_picture": data.get("profile_picture"),
                "bio": data.get("bio"),
                "favourite_subject": favourite_subjects,
                "favourite_lecturer": favourite_lecturers,
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
