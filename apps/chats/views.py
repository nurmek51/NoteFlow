from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..users.models import StudyGroup, User
from .models import ChatMessage
from .serializers import StudyGroupSerializer, ChatMessageSerializer


class StudyGroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD StudyGroup
    """
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """ Adding owner to the members too """
        group = serializer.save()
        group.members.add(self.request.user)

    def destroy(self, request, *args, **kwargs):
        """ Only group owner can delete  """
        group = self.get_object()
        if request.user not in group.members.all():
            return Response({'detail': 'Вы не можете удалить эту группу'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """ API for join the group """
        group = get_object_or_404(StudyGroup, pk=pk)
        group.members.add(request.user)
        return Response({'message': 'Вы успешно вступили в группу'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """ API for leaving from the group """
        group = get_object_or_404(StudyGroup, pk=pk)
        if request.user in group.members.all():
            group.members.remove(request.user)
            return Response({'message': 'Вы покинули группу'})
        return Response({'detail': 'Вы не состоите в этой группе'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_groups(self, request):
        """ Get group list where the current user is member """
        groups = StudyGroup.objects.filter(members=request.user)
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def chat_link(self, request, pk=None):
        """ API for get link for connection to chat """
        group = get_object_or_404(StudyGroup, pk=pk)
        if request.user not in group.members.all():
            return Response({'detail': 'Вы не состоите в этой группе'}, status=status.HTTP_403_FORBIDDEN)

        # Get the current host
        current_host = request.get_host()

        # Initializing protocol (http / https) and change it to wss/ws
        if request.is_secure():
            ws_protocol = "wss"
        else:
            ws_protocol = "ws"

        # Forming dynamic url for WebSocket
        websocket_url = f"{ws_protocol}://{current_host}/ws/group/{group.id}/?token={request.auth}"

        return Response({'websocket_url': websocket_url})
