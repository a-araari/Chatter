from django.forms import ModelForm
from .models import Chat


class ChatForm(ModelForm):
	class Meta:
		model = Chat
		fields = ['text']