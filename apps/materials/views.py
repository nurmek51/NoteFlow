from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import Subject, Lecturer, StudyMaterial, Tag, Comment, Vote
from .serializers import (
    SubjectSerializer, LecturerSerializer, StudyMaterialSerializer,
    TagSerializer, CommentSerializer, VoteSerializer
)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def subject_list(request):
    """
    - GET: Получить список всех предметов.
    """
    if request.method == 'GET':
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def subject_detail(request, pk):
    """
    - GET: Получить детали конкретного предмета.
    """
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'GET':
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def material_list(request):
    """
    - GET -> get list of all materials.
    - POST: upload material.
    """
    if request.method == 'GET':
        materials = StudyMaterial.objects.all()
        serializer = StudyMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudyMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)  # Привязываем материал к пользователю
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def filtered_material_list(request):
    '''get -> get list of materials on some subject with some tag if there is one'''
    if request.method == 'GET':
        tags = request.data.get('tags', None)
        subject = request.data.get('subjects', None)

        materials = StudyMaterial.objects.all()

        if tags:
            materials = materials.filter(tags__name__in=tags)
        if subject:
            materials = materials.filter(subjects__name__in=subject)

        serializer = StudyMaterialSerializer(materials, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def material_detail(request, pk):
    """
    - GET -> get details of material.
    - PUT-> edit uploaded material.
    - DELETE -> delete uploaded material.
    """
    material = get_object_or_404(StudyMaterial, pk=pk)

    if request.method == 'GET':
        serializer = StudyMaterialSerializer(material)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if material.uploaded_by != request.user:
            return Response({"error": "You can only edit your own materials."}, status=status.HTTP_403_FORBIDDEN)

        serializer = StudyMaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if material.uploaded_by != request.user:
            return Response({"error": "You can only delete your own materials."}, status=status.HTTP_403_FORBIDDEN)

        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def vote_material(request, material_id):
    """
    - POST: set like(1) or dislike(-1) on a material.
    - if user already set a vote, it changes.
    """
    material = get_object_or_404(StudyMaterial, id=material_id)
    user = request.user
    vote_value = request.data.get('vote')  # Ожидает 1 (лайк) или -1 (дизлайк)

    if vote_value not in [1, -1]:
        return Response({"error": "Invalid vote value"}, status=status.HTTP_400_BAD_REQUEST)

    # create or edit vote
    vote, created = Vote.objects.update_or_create(user=user, material=material, defaults={'vote': vote_value})

    return Response({"message": f"Vote {'updated' if not created else 'added'} successfully"},
                    status=status.HTTP_200_OK)


# comments
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def comment_list(request, material_id):
    """
    - GET -> get comments on a material.
    - POST -> upload comment on a material.
    """
    material = get_object_or_404(StudyMaterial, id=material_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(material=material)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, material=material)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaterialUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        material_id = request.data.get('id')

        if material_id:
            try:
                material = StudyMaterial.objects.get(id=material_id, uploaded_by=request.user)

                if material.file:
                    material.file.delete(save=False)

                serializer = StudyMaterialSerializer(material, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": f"Material successfully updated: {request.data}"}, status=status.HTTP_200_OK)

            except StudyMaterial.DoesNotExist:
                return Response({"error": "Material not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudyMaterialSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response({"message": f"Material successfully created: {request.data}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request,material_id):    # DELETE http://127.0.0.1:8000/upload/material/5/
        try:
            material = StudyMaterial.objects.get(id = material_id,uploaded_by=request.user)

            if material.file:
                material.file.delete(save=False) #from s3
            material.delete() # from postgre

            return Response({'message':"Material deleted succsessfully"},status=status.HTTP_204_NO_CONTENT)
        except StudyMaterial.DoesNotExist:
            return Response({"error": "Material not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)
