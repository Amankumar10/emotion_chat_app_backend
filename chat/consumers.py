import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Thread
from accounts.models import CustomUser
from asgiref.sync import sync_to_async
import tensorflow as tf
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load model and tools
model = tf.keras.models.load_model('saved_model/emotion_model.keras')
tokenizer = joblib.load('saved_model/tokenizer.joblib')
label_encoder = joblib.load('saved_model/label_encoder.joblib')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.thread_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        # Get sender and thread
        sender = await sync_to_async(CustomUser.objects.get)(id=sender_id)
        thread = await sync_to_async(Thread.objects.get)(id=self.thread_id)

        # Emotion prediction
        emotion = await sync_to_async(self.detect_emotion)(message)

        # Save message to DB
        msg_obj = await sync_to_async(Message.objects.create)(
            thread=thread,
            sender=sender,
            text=message,
            emotion=emotion
        )

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'emotion': emotion,
                'sender': sender.username,
                'timestamp': str(msg_obj.timestamp),
            }
        )

    def detect_emotion(self, text):
        try:
            seq = tokenizer.texts_to_sequences([text])
            padded = pad_sequences(seq, maxlen=50)
            prediction = model.predict(padded, verbose=0)
            emotion = label_encoder.inverse_transform([prediction.argmax(axis=1)[0]])[0]
            print(f"[EMOTION] '{text}' → {emotion}")
            return emotion
        except Exception as e:
            print(f"[ERROR] Emotion detection failed: {e}")
            return "unknown"

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'emotion': event['emotion'],
            'timestamp': event['timestamp']
        }))

