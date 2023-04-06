from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers

from .forms import ChatForm
from .models import Chat


User = get_user_model()

@login_required
def index(request):
	sender = request.user
	reciever = User.objects.first()
	form = ChatForm()
	messages = Chat.objects.all()

	if request.method == 'POST':
		form = ChatForm(request.POST)
		chat = form.save(commit=False)
		chat.sender = sender
		chat.reciever = reciever
		chat.save()

	return render(request, 'base/index.html', context={'form': form, 'messages': messages})


@login_required
def get_messages(request):
	data = serializers.serialize("json", Chat.objects.all())
	return JsonResponse(data, safe=False)