from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView


from django.http import HttpResponse

import datetime
from django.db.models import Count
# from reviews.models import Review
# from .models import Blog

# Create your views here.
import random
# from plotly.offline import plot
# import plotly.graph_objects as graphs

import matplotlib.pyplot as plt, mpld3

from .chatbot import Chat, pairs, reflections


eliza_chatbot = Chat(pairs, reflections)

def matplotfig(x, y):
	# plt.figure(figsize=(20,8))
	plt.figure()
	plt.plot(x, y)

	mpldobj = mpld3.fig_to_html(plt.gcf())

	return mpldobj





def plotlyfig(x, y):
	# Generate figure
	figure = graphs.Figure()
	scatter = graphs.Scatter(x=x, y=y)
	figure.add_trace(scatter)
	figure.update_layout(xaxis_title='Month', yaxis_title='Price')
	
	plot_html = plot(figure, output_type='div')

	return plot_html

def converse(self, quit="quit"):
	input_str = ""
	while input_str != quit:
		input_str = quit
		try: 
			input_str = input(">")
		except EOFError:
				print(input_str)
		if input_str:
			while input_str[-1] in "!.": 
				input_str = input_str[:-1]
			print(self.respond(input_str))

def chat_home(request):

	x = range(10)
	y = [2, 1, 7, 3, 6,]
	y = random.sample(range(0,100), len(x))

	# Add to template

	# Check the form is submitted or not
	plot_html = None
	if request.method == 'POST':

		# Check the form data are valid or not

		# Read the submitted values
		query = request.POST.get("query")

		response = None
		if query != "":
			response = eliza_chatbot.converse2(query)
			plot_html = matplotfig(x, y)
		# value = request.POST.get("value")

		# Return the form values as response
		return render(request, 'chat/home.html', {'response': query, 'chat_figure': plot_html})
		# return render(request, 'chat/home.html', {'response': response, 'chat_figure': plot_html})


	else:
		return render(request, 'chat/home.html', {'response': '', 'chat_figure': None})

