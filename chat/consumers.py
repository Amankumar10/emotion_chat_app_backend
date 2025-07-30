import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Thread
from accounts.models import CustomUser
from asgiref.sync import sync_to_async


import tensorflow as tf
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences

from django.contrib.auth import get_user_model


model = tf.keras.models.load_model('saved_model/emotion_model.keras')
tokenizer = joblib.load('saved_model/tokenizer.joblib')
label_encoder = joblib.load('saved_model/label_encoder.joblib')

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.thread_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        sender = await sync_to_async(CustomUser.objects.get)(id=sender_id)
        thread = await sync_to_async(Thread.objects.get)(id=self.thread_id)

        msg_obj = await sync_to_async(Message.objects.create)(
            thread=thread, sender=sender, text=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': str(msg_obj.timestamp)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))





# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.contrib.auth import get_user_model
# from .models import Message, Thread

# import tensorflow as tf
# import joblib
# from tensorflow.keras.preprocessing.sequence import pad_sequences

# # Load model and tools
# model = tf.keras.models.load_model('saved_model/emotion_model.keras')
# tokenizer = joblib.load('saved_model/tokenizer.joblib')
# label_encoder = joblib.load('saved_model/label_encoder.joblib')

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.thread_id = self.scope['url_route']['kwargs']['thread_id']
#         self.room_group_name = f"chat_thread_{self.thread_id}"

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_text = data.get('message')

#         sender = self.scope["user"]
#         if not sender.is_authenticated:
#             await self.send(text_data=json.dumps({"error": "Unauthorized"}))
#             return

#         # Emotion prediction
#         emotion = await sync_to_async(self.detect_emotion)(message_text)

#         # Save message
#         await sync_to_async(self.save_message)(sender, message_text, emotion)

#         # Broadcast
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message_text,
#                 'sender': sender.username,
#                 'emotion': emotion,
#             }
#         )

#     def detect_emotion(self, text):
#         seq = tokenizer.texts_to_sequences([text])
#         padded = pad_sequences(seq, maxlen=50)
#         prediction = model.predict(padded, verbose=0)
#         return label_encoder.inverse_transform([prediction.argmax(axis=1)[0]])[0]

#     def save_message(self, sender, text, emotion):
#         thread = Thread.objects.get(id=self.thread_id)
#         Message.objects.create(
#             thread=thread,
#             sender=sender,
#             text=text,
#             emotion=emotion
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#             'emotion': event['emotion']
#         }))
