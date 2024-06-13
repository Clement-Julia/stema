import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, UserProfile
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        # # Notify participants about the user's connection
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'user_connected',
                'user_id': self.user.id,
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        # # Notify participants about the user's disconnection
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'user_disconnected',
                'user_id': self.user.id,
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        sender_username = await self.get_user(sender_id)
        # Save the message to the database
        conversation = await self.get_conversation(self.conversation_id)
        await self.create_message(conversation, self.scope['user'], message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_username': sender_username.username,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username
        }))

    async def user_connected(self, event):
        user_id = event['user_id']

        # Notify the client about the user connection
        await self.send(text_data=json.dumps({
            'type': 'user_connected',
            'user_id': user_id
        }))

    async def user_disconnected(self, event):
        user_id = event['user_id']

        # Notify the client about the user disconnection
        await self.send(text_data=json.dumps({
            'type': 'user_disconnected',
            'user_id': user_id
        }))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        return get_object_or_404(Conversation, id=conversation_id)
    @database_sync_to_async
    def get_user(self, sender_id):
        return get_object_or_404(User, id=sender_id)

    @database_sync_to_async
    def create_message(self, conversation, user, message):
        return Message.objects.create(conversation=conversation, sender=user, content=message)
