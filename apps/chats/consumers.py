from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.db.models import Q
from apps.chats.models import ChatMessage
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # close connection if user not authed
        if not self.scope.get("user") or not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f'private_{self.room_name}'


        try:
            parts = self.room_name.split("_")
            # parts[0] = "private", parts[1] = "chat", parts[2] и parts[3] — ID
            user_id1 = int(parts[2])
            user_id2 = int(parts[3])
        except Exception as e:
            await self.close()
            return

        print(user_id1, user_id2)
        # Identifies the user of current chat
        current_user_id = self.scope["user"].id
        if current_user_id == user_id1:
            self.other_user_id = user_id2
        elif current_user_id == user_id2:
            self.other_user_id = user_id1
        else:
            # User not member of this chat
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Load the message history and send to client
        messages = await self.get_chat_history(current_user_id, self.other_user_id)
        for msg in messages:
            await self.send(text_data=json.dumps({
                "message": msg.message,
                "sender": msg.sender.username,
                "timestamp": msg.timestamp.isoformat(),
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        sender = self.scope["user"].username if self.scope["user"].is_authenticated else "not auth"

        # Saving the message in DB
        await self.save_message(self.scope["user"].id, self.other_user_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            }
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def get_chat_history(self, user_id, other_user_id):
        qs = ChatMessage.objects.filter(
            Q(sender_id=user_id, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver_id=user_id)
        ).select_related('sender').order_by("timestamp")
        return list(qs)

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        # Making image of message in DB
        ChatMessage.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message,
        )