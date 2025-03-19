from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from ..users.models import StudyGroup, User
from .models import ChatMessage
from .serializers import StudyGroupSerializer, ChatMessageSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of study groups",
        description="Returns a list of all available study groups.",
        responses={200: StudyGroupSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create a new study group",
        description="Allows authenticated users to create a new study group.",
        responses={201: StudyGroupSerializer}
    ),
    retrieve=extend_schema(
        summary="Retrieve details of a study group",
        description="Returns the details of a specific study group based on its ID.",
        responses={200: StudyGroupSerializer}
    ),
    update=extend_schema(
        summary="Update a study group",
        description="Allows the group owner to update the study group details.",
        responses={200: StudyGroupSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update a study group",
        description="Allows the group owner to partially update the study group details.",
        responses={200: StudyGroupSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a study group",
        description="Allows the group owner to delete a study group.",
        responses={204: OpenApiResponse(description="Group deleted successfully")}
    ),
)
class StudyGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Study Groups.
    """

    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Create a Study Group",
        description="Allows an authenticated user to create a new study group.",
        responses={201: StudyGroupSerializer}
    )
    def perform_create(self, serializer):
        """ When a study group is created, the creator is automatically added as a member. """
        group = serializer.save()
        group.members.add(self.request.user)

    @extend_schema(
        summary="Delete a Study Group",
        description="Allows only the group owner to delete the study group.",
        responses={204: OpenApiResponse(description="Study group deleted successfully")}
    )
    def destroy(self, request, *args, **kwargs):
        """ Only the group owner can delete the study group. """
        group = self.get_object()
        if request.user not in group.members.all():
            return Response({'detail': 'You cannot delete this group'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Join a Study Group",
        description="Allows an authenticated user to join a specific study group.",
        responses={200: OpenApiResponse(description="Successfully joined the study group")}
    )
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """ API endpoint to join a study group. """
        group = get_object_or_404(StudyGroup, pk=pk)
        group.members.add(request.user)
        return Response({'message': 'Successfully joined the group'})

    @extend_schema(
        summary="Leave a Study Group",
        description="Allows an authenticated user to leave a specific study group.",
        responses={200: OpenApiResponse(description="Successfully left the study group")}
    )
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """ API endpoint to leave a study group. """
        group = get_object_or_404(StudyGroup, pk=pk)
        if request.user in group.members.all():
            group.members.remove(request.user)
            return Response({'message': 'Successfully left the group'})
        return Response({'detail': 'You are not a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="List Study Groups of the Authenticated User",
        description="Retrieves a list of study groups where the authenticated user is a member.",
        responses={200: StudyGroupSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def my_groups(self, request):
        """ API endpoint to retrieve all study groups where the current user is a member. """
        groups = StudyGroup.objects.filter(members=request.user)
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get WebSocket Chat Link",
        description="Returns the WebSocket URL to join the chat for a specific study group.",
        responses={200: OpenApiResponse(description="WebSocket link for the group chat")}
    )
    @action(detail=True, methods=['get'])
    def chat_link(self, request, pk=None):
        """ API endpoint to generate a WebSocket chat link for a study group. """
        group = get_object_or_404(StudyGroup, pk=pk)
        if request.user not in group.members.all():
            return Response({'detail': 'You are not a member of this group'}, status=status.HTTP_403_FORBIDDEN)

        # Get the current host
        current_host = request.get_host()

        # Determine WebSocket protocol (ws/wss)
        ws_protocol = "wss" if request.is_secure() else "ws"

        # Generate dynamic WebSocket URL
        websocket_url = f"{ws_protocol}://{current_host}/ws/group/{group.id}/?token={request.auth}"

        return Response({'websocket_url': websocket_url})
