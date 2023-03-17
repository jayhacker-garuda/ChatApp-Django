from django.urls import path
from . import views

app_name = 'private_social'

urlpatterns = [
    # path('<str:me>/<str:username>/',
    #      views.PrivateChatView.as_view(), name='private_chat_room'),
    path('users/', views.UserInboxList.as_view(), name='user_inbox'),
    path('messages/', views.MessagesRoom.as_view(), name='all_messages_list'),
    path('messages/inbox/<dialog_with>/',
         views.MessagesRoom.as_view(), name='messages_list'),
    path('dialogs/', views.DialogsModelList.as_view(), name='dialogs_list'),
    path('self/', views.SelfInfoView.as_view(), name='self_info'),
]
