import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async

from .models import ChatMessage, PrivateChatRoom as Private

from django.contrib.auth import get_user_model


User = get_user_model()


class PrivateChatRoom(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.private_room = None
        self.user = None

    @database_sync_to_async
    def _room_online_add(self, user):
        # return print(user)
        return self.private_room.join(user)

    @database_sync_to_async
    def _room_online_remove(self, user):
        return self.private_room.leave(user)

    @database_sync_to_async
    def _get_private_room(self, room_name):
        return Private.objects.get(name=room_name)

    # @database_sync_to_async is used with asynchronous code

    @database_sync_to_async
    def save_message(self, message):
        print("Message going to saved")
        new_message = ChatMessage.objects.create(
            sender=self.user, message=message, room=self.private_room)
        new_message.save()
        return "Succes"

    async def connect(self):
        self.user = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        not_me = self.scope['url_route']['kwargs']['me']
        print(other_username)
        if self.user.username == other_username:
            self.room_name = f'{not_me}-{other_username}'
        else:
            self.room_name = f'{self.user.username}-{other_username}'
            
        # print(room_name)
        self.room_group_name = f'private_chat_{self.room_name}'
        self.private_room = await self._get_private_room(self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if self.user.is_authenticated:
            # send the join event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join_private_chat',
                    'user': self.user.username,
                }
            )
            await self._room_online_add(self.user)

    async def disconnect(self, code):

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave_private_chat',
                'user': self.user.username,
            }
        )
        await self._room_online_remove(self.user)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        if not self.user.is_authenticated:
            # print("here")
            return
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'private_chat_message',
                'message': message,
                'username': username
            }
        )
        await self.save_message(message)

    async def private_chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'type': 'private_chat_message',
            'message': message,
            'username': username,
            # 'user_id':user_id
        }))
        # print(f"{user_obj.username} : Message Sent")

    async def user_join_private_chat(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_leave_private_chat(self, event):
        await self.send(text_data=json.dumps(event))
