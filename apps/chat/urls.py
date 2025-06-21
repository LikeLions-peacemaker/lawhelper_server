from django.urls import path
from .views import chatbot_api, chat_page, load_history, list_sessions, chat_summaries

urlpatterns = [
    path('response/', chatbot_api, name='chatbot_api'),
    path('chat_page/', chat_page, name='chat_page'),
    path('history/', load_history, name='load_history'),
    path('sessions/', list_sessions, name='list_sessions'),
    path('summaries/', chat_summaries, name='chat_summaries'),
    path('summaries/<str:session_id>', chat_summaries, name='chat_summaries'),

]