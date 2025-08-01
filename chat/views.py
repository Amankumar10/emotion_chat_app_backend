from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Thread, Message
from accounts.models import CustomUser
from .serializers import ThreadSerializer, MessageSerializer

class GetOrCreateThread(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            other_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user1 = request.user
        user2 = other_user

        thread = Thread.objects.filter(
            user1__in=[user1, user2],
            user2__in=[user1, user2]
        ).first()

        if not thread:
            thread = Thread.objects.create(user1=user1, user2=user2)

        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

class MessageListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, thread_id):
        messages = Message.objects.filter(thread_id=thread_id).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    # def post(self, request, thread_id):
    #     data = request.data.copy()
    #     data['sender'] = request.user.id
    #     data['thread'] = thread_id
    #     serializer = MessageSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)
