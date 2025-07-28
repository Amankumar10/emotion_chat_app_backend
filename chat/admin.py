from django.contrib import admin
from .models import Thread, Message

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    list_filter = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'sender', 'text', 'emotion', 'timestamp')
    search_fields = ('text', 'sender__username', 'emotion')
    list_filter = ('timestamp', 'emotion')
