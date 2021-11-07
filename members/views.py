\
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy



from django.http import HttpResponse



# Create your views here.



def member_home(request):
	# top_blogs = Blog.objects.order_by('-date')[5]	
	return render(request, 'members/home.html')




class UserRegisterView(generic.CreateView):
	form_class = UserCreationForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')


