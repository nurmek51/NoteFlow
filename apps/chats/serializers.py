from rest_framework import serializers
from ..users.models import StudyGroup
from .models import ChatMessage

class StudyGroupSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'members', 'members_count', 'created_at']

    def get_members_count(self, obj):
        return obj.members.count()

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_username', 'group', 'message', 'timestamp']
