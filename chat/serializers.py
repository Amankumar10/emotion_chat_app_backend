from rest_framework import serializers
from .models import Thread, Message
from accounts.models import CustomUser

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class ThreadSerializer(serializers.ModelSerializer):
    user1 = UserSimpleSerializer(read_only=True)
    user2 = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'user1', 'user2', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'thread', 'sender', 'text', 'emotion', 'timestamp']
