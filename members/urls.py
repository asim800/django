from django.urls import path
from . import views



urlpatterns = [
	path('register/', views.UserRegisterView.as_view(), name='register'),
	path('', views.member_home, name='member-home'),
]

