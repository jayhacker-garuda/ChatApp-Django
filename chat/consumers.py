import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Room, Message
from django.utils import  timezone

class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        # self.user_inbox = None

    @database_sync_to_async
    def _save_message(self, message):
        return Message.objects.create(user=self.user, room=self.room, content=message)

    @database_sync_to_async
    def _get_room(self, room_name):
        return Room.objects.get(slug=room_name)

    @database_sync_to_async
    def _room_online_add(self, user):
        # return print(user)
        return self.room.join(user)

    @database_sync_to_async
    def _room_online_remove(self, user):
        return self.room.leave(user)

    @sync_to_async
    def _get_users_online(self):
        # self.room.online.remove(user)
        # temp = []

        data = [user.username for user in self.room.online.all()]
        # res = **data
        # temp.append()
        # print(type(data))
        return data

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # self.user_inbox = f'inbox_{self.user.username}'
        self.room = await self._get_room(self.room_name)
        self.user = self.scope['user']
        # joining room group

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # send the user list to the newly joined user
        # print(self.room)
        # database_sync_to_async(print)(self._get_users_online())()
        await self.send(json.dumps({
            'type': 'user_list',
            'users': await self._get_users_online(),
        }))

        if self.user.is_authenticated:
            # send the join event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            await self._room_online_add(self.user)
            # -------------------- new --------------------
            # create a user inbox for private messages
            # await self.channel_layer.group_add(
            #     self.user_inbox,
            #     self.channel_name,
            # )
            # ---------------- end of new ----------------
            # print(self.user)
            # print('Room => {}'.format(self.room))

    async def disconnect(self, code):
        # Leaving room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'user': self.user.username,
            }
        )
        await self._room_online_remove(self.user)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Receiving message from websocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        if not self.user.is_authenticated:
            # print("here")
            return
        # Sending message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                # 'sent_at': timezone.datetime.now()
            }
        )
        await self._save_message(message)
        # print(True, 'Message added')

    async def chat_message(self, event):
        # Receive message from room group
        message = event['message']
        username = event['username']
        # sent_at = event['sent_at']
        # print(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username,
            # 'sent_at': sent_at
        }))
        # print(True, 'Message send')

    async def user_join(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps(event))
