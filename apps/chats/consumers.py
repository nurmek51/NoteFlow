from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.db.models import Q
from apps.chats.models import ChatMessage
from ..users.models import User, StudyGroup
class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Initializing connect to WSocket """
        if not self.scope.get("user") or not self.scope["user"].is_authenticated:
            print(f"User is not authenticated: {self.scope.get('user')}")
            await self.close()
            return

        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.group_name = f"group_{self.group_id}"
        self.user = self.scope["user"]

        # Checking that user in the group
        is_member = await self.check_membership(self.user.id, self.group_id)
        if not is_member:
            print(f"User {self.user.id} is not a member of group {self.group_id}")
            await self.close()
            return

        # Adding user to group channel
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Sendign chat history
        messages = await self.get_chat_history(self.group_id)
        for msg in messages:
            await self.send(text_data=json.dumps({
                "message": msg.message,
                "sender": msg.sender.username,
                "timestamp": msg.timestamp.isoformat(),
            }))

    async def disconnect(self, close_code):
        """ Initializing disconnect to WebSocket """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """ Initializing receiving message """
        data = json.loads(text_data)
        message = data.get("message", "")

        # Saving message to DB
        await self.save_message(self.user.id, self.group_id, message)

        # Sending the message to all members
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def check_membership(self, user_id, group_id):
        """ Checking the membershio"""
        return StudyGroup.objects.filter(id=group_id, members__id=user_id).exists()

    @database_sync_to_async
    def get_chat_history(self, group_id):
        return list(ChatMessage.objects.filter(group_id=group_id).select_related('sender').order_by("timestamp"))

    @database_sync_to_async
    def save_message(self, sender_id, group_id, message):
        group = StudyGroup.objects.get(id=group_id)
        ChatMessage.objects.create(sender_id=sender_id, group=group, message=message)