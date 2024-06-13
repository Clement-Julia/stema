# # app_chat/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.shortcuts import get_object_or_404
# from .models import Conversation, Message

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
#         self.conversation_group_name = f'chat_{self.conversation_id}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.conversation_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.conversation_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Save the message to the database
#         conversation = await self.get_conversation(self.conversation_id)
#         await self.create_message(conversation, self.scope['user'], message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.conversation_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

#     @database_sync_to_async
#     def get_conversation(self, conversation_id):
#         return get_object_or_404(Conversation, id=conversation_id)

#     @database_sync_to_async
#     def create_message(self, conversation, user, message):
#         return Message.objects.create(conversation=conversation, sender=user, content=message)
# app_chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from .models import Conversation, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']

        # Save the message to the database
        conversation = await self.get_conversation(self.conversation_id)
        await self.create_message(conversation, self.scope['user'], message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        return get_object_or_404(Conversation, id=conversation_id)

    @database_sync_to_async
    def create_message(self, conversation, user, message):
        return Message.objects.create(conversation=conversation, sender=user, content=message)
