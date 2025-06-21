# gptbot/models.py
from django.db import models

class Embedding(models.Model):
    text = models.TextField()
    embedding = models.TextField()  # JSON 문자열로 저장

    def __str__(self):
        return self.text[:30]
class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255, blank=True, default="새 대화")
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Bot")])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
