from django.urls import path

from .views import index, get_messages, delete_message


urlpatterns = [
    path('', index, name='index'),
    path('messages/', get_messages, name='get_messages'),
    path('delete/<int:pk>/', delete_message, name='delete_messages')
]
