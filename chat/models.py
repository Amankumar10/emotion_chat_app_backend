from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Thread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user1', 'user2']

    def __str__(self):
        return f"Thread between {self.user1.username} & {self.user2.username}"

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    emotion = models.CharField(max_length=50, blank=True)  # Output from your AI model
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender}: {self.text[:20]}..."





# from django.db import models
# from django.conf import settings
# from django.utils import timezone

# User = settings.AUTH_USER_MODEL

# class Thread(models.Model):
#     user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_user1')
#     user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_user2')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user1', 'user2']

#     def __str__(self):
#         return f"Thread between {self.user1} and {self.user2}"

# class Message(models.Model):
#     thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()
#     emotion = models.CharField(max_length=50, blank=True, null=True)  # Output from your AI model
#     timestamp = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.sender}: {self.text[:20]}..."