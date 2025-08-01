from django.urls import path
from .views import GetOrCreateThread, MessageListCreate

urlpatterns = [
    path('thread/<int:user_id>/', GetOrCreateThread.as_view()),  # POST
    path('messages/<int:thread_id>/', MessageListCreate.as_view()),  # GET
]
