
from django.urls import path
from . import views



urlpatterns = [
	path('', views.chat_home, name='chat-home'),
	path('qport', views.portfolio_home, name='portfolio-home'),
]

