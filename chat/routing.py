from django.urls import re_path, path
from . import consumers
from private_chat.consumers import PrivateChatConsumer


websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<slug:room_name>/', consumers.ChatConsumer.as_asgi()),
    # path('ws/<int:id>/', PersonalChatConsumer.as_asgi())
    # re_path('ws/private-chat/<str:me>/<str:username>/', PrivateChatRoom.as_asgi()),
    path('ws/private_chat/', PrivateChatConsumer.as_asgi()),

]
