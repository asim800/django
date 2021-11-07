
from django.shortcuts import render


from django.http import HttpResponse

# Create your views here.
# from .models import Project

def index_mysite(request):
	projects = {} # Project.objects.all()

	return render(request, 'mysite/index.html', {'projects': projects})