import json
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
	reciever_id = request.GET.get('reciever_id', None)
	if not reciever_id:
		if sender.is_superuser:
			users = User.objects.all().exclude(pk=sender.id)
			return render(request, 'base/choose.html', context={'users': users})
		else:
			reciever_id = User.objects.filter(is_superuser=True).first().id


	reciever = User.objects.filter(pk=reciever_id).first()
	
	form = ChatForm()
	if request.method == 'POST':
		form = ChatForm(request.POST)
		chat = form.save(commit=False)
		chat.sender = sender
		chat.reciever = reciever
		chat.save()

	messages = Chat.objects.filter(sender__in=[sender, reciever], reciever__in=[reciever, sender]).order_by('created_at')
	return render(request, 'base/index.html', context={
		'form': form,
		'messages': messages,
		'reciever': reciever
	})


@login_required
def get_messages(request):
	sender = request.user
	reciever_id = request.GET.get('reciever_id', None)
	if sender.is_superuser and not reciever_id:
		users = User.objects.all().exclude(pk=sender.id)
		return JsonResponse({'message': 'Wrong type of url'});

	reciever = User.objects.filter(pk=reciever_id).first()
	messages = Chat.objects.filter(sender__in=[sender, reciever], reciever__in=[reciever, sender]).order_by('created_at')
	
	data = []
	for message in messages:
		data.append({
			'id': message.id,
			'text': message.text,
			'sender': message.sender.username,
			'sender_id': message.sender.id,
			'reciever': message.reciever.username,
			'reciever_id': message.reciever.id,
			'created_at': message.created_at.strftime('%H:%M'),
		})
	return JsonResponse(json.dumps(data), safe=False)


@login_required
def delete_message(request, pk):
	message = Chat.objects.get(pk=pk)
	message.delete()
	return JsonResponse({}, safe=False)
