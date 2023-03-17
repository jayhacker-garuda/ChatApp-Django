from django.urls import path
from . import views
app_name = 'social'
urlpatterns = [
    path('', views.ChatHome.as_view(), name='index'),
    path('<slug:room_name>/', views.ChatRoom.as_view(), name='chat_room'),
    path('create/room', views.ChatRoomCreate.as_view(), name='chat_room_create'),
]
