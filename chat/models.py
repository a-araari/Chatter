from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Chat(models.Model):
	text = models.TextField()
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'sent by {self.sender.username} to {self.reciever.username}: {self.text}'
