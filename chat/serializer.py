
from rest_framework import routers, serializers, viewsets

from .models import Chat


class chatAPI(serializers.ModelSerializer):
	model = Chat
	fields = ['text']

	