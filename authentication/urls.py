from django.urls import path, re_path

from . import views
app_name = 'auth'
urlpatterns = [
    path('register/', views.CustomRegisterView.as_view(), name='chat_register'),
    path('login/', views.CustomLoginView.as_view(), name='chat_login'),
    re_path(
        r'activate/(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,34})', views.EmailVerification.as_view(), name='chat_activate'),
    path('logout/', views.CustomAuthLogout.as_view(),name='chat_logout')
    
]   
