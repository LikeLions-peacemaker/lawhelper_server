from django.urls import path
from .views import chatbot_api, chat_page, load_history, list_sessions

urlpatterns = [
    path('response/', chatbot_api, name='chatbot_api'),
    path('chat_page/', chat_page, name='chat_page'),
    path('history/', load_history, name='load_history'),
    path('sessions/', list_sessions, name='list_sessions'),
]