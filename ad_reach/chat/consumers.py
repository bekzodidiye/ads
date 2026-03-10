import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from contracts.models import Contract
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.contract_id = self.scope['url_route']['kwargs']['contract_id']
        self.room_group_name = f'chat_{self.contract_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        user_id = self.scope['user'].id

        # Save message to database
        msg = await self.save_message(user_id, self.contract_id, message_text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_id': user_id,
                'created_at': str(msg.created_at)
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, user_id, contract_id, text):
        user = User.objects.get(id=user_id)
        contract = Contract.objects.get(id=contract_id)
        return Message.objects.create(sender=user, contract=contract, text=text)
