from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

from django.db.models import Count
# from reviews.models import Review
# from .models import Blog


import numpy as np
import pandas as pd
import datetime
import random
# from plotly.offline import plot
# import plotly.graph_objects as graphs

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
from matplotlib.pyplot import figure

# import matplotlib.dates as mdates
# import matplotlib.ticker as ticker
# import plotly.express as px



from .models import Symbols, OHLCV
from .models import Portfolio, PortfolioSymbol
from .chatbot import Chat, pairs, reflections

from .putils import raw_return, annualized_return, duration, max_drawdown, calmar_ratio,  sortino_ratio, annualized_standard_deviation, sharpe_ratio
# from pyutils import *


import ipdb


eliza_chatbot = Chat(pairs, reflections)

def matplotfig(x, y, title=None):
	# plt.figure(figsize=(20,8))
	# plt.figure()
	# plt.clf()
	# plt.xticks(rotation=50)
	# plt.gca().tick_params(axis='x', rotation=50)
	# fig = figure(figsize=(6,6))
	# ax = fig.subplots()

	fig, ax = plt.subplots(figsize=(5,5))
	ax.plot(x, y)
	ax.xaxis_date()
	# ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
	# fig.autofmt_xdate()
	ax.set_title(title)

	# print(ax.xaxis.get_major_formatter())

	
	# ax.xaxis.set_tick_params(rotation=90)
	# mpld3.show(fig)
	# mpldobj = mpld3.fig_to_html(fig, figid="mplplot")

	mpldobj = mpld3.fig_to_html(fig)

	# plt1 = px.plot(x, y)

	return mpldobj

def matplotfig2(x, y, z=None):
	fig, ax = plt.subplots(figsize=(5,5))
	ax.plot( [2, 1, 7, 3])
	ax.grid()

	mpldobj = mpld3.fig_to_html(fig)
	# mpldobj = None

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

#########################################
def _portfolio_id(request):
	portfolio_id = request.session.session_key
	print('Port id found', portfolio_id)
	if not portfolio_id:
		portfolio_id = request.session.create()
		print('Port id created', portfolio_id)
	return portfolio_id

def portfolio_home(request):
	return render(request, 'chat/portfolio.html')

def add_symbol(request, symbol, pct=10):
	symbol = Symbols.objects.get(pk=symbol)
	portfolio, *b = Portfolio.objects.get_or_create(portfolio_id=_portfolio_id(request))

	portfolio_symbol, *b = PortfolioSymbol.objects.get_or_create(portfolio=portfolio, symbol=symbol, pct=pct/100.0)

	portfolio_symbol.save()

	portfolio.save()

def update_symbol(request, symbol, pct=1):
	symbol = Symbols.objects.get(pk=symbol)
	pp = _portfolio_id(request)
	print('update sym', symbol, pp)
	portfolio, *b = Portfolio.objects.get_or_create(portfolio_id=_portfolio_id(request))
	print('port stuff', portfolio)


	portfolio_symbol = PortfolioSymbol.objects.filter(portfolio=portfolio, symbol=symbol)
	# if pct:
	if portfolio_symbol:
		portfolio_symbol = portfolio_symbol.first() # qs -> obj
		print("PCCCCCCCCCCCCCCCCTTTTTTTTTTTTT", pct)
		if not pct or pct==0:
			portfolio_symbol.delete()
			# portfolio_symbol.save()
			# print("AAAAAAAAAAAAAAAAA")
		else:
			portfolio_symbol.pct = pct
			portfolio_symbol.save()
			# print(type(portfolio_symbol), 'PPPPPPPPPPPPPPPPPPP22222222222222')

	else:
		portfolio_symbol, *b = PortfolioSymbol.objects.get_or_create(portfolio=portfolio, symbol=symbol, pct=pct)

		print(type(portfolio_symbol), 'PPPPPPPPPPPPPPPPPPPP')
		
		portfolio.save()

def delete_symbol(request, symbol):
	# symbol = get_object_or_404(portfolio_id=_portfolio_id(request))
	portfolio = Portfolio.objects.get(portfolio_id=_portfolio_id(request))
	if PortfolioSymbol.objects.filter(portfolio_id=portfolio.id).exists():
		symbol = get_object_or_404(PortfolioSymbol, portfolio_id=portfolio.id, symbol=symbol)
		symbol.delete()


#########################################
def chat_home(request):

	num_visits = request.session.get('num_visits', 0) + 1
	request.session['num_visits'] = num_visits


	query_symbols = Symbols.objects.all()
	syms = []
	for sym in query_symbols:
		syms.append(sym.symbol)

	# Add to template

	# Check the form is submitted or not
	plot_html = None
	if request.method == 'POST':

		# Check the form data are valid or not

		# Read the submitted values
		user_text = request.POST.get("query")
		print(request.POST)
#########################################
		tickers_port = request.POST.getlist('tickers', [])
		pcts_port   = request.POST.getlist('pcts', [])
		pcts_port   = list(map(lambda x: 0 if x=='' else float(x), pcts_port))
#########################################
	

		response = None
		symbols = None
		portfolio_symbols = None
		print('USER  ', user_text)
		if user_text:
			user_text = user_text.upper()
			if user_text in syms:
				
				# add_symbol(request, user_text)
				query_ohlcv = OHLCV.objects.filter(symbol=user_text).values('date', 'close')

				dates = []
				close = []
				for row in query_ohlcv:
					close.append(float(row['close']))
					dates.append(row['date'])
				# close = OHLCV.objects.values_list('Close', flat=True)
				print("DATES...", user_text)
				x = range(len(close))
				plot_html = matplotfig(dates, close, user_text)
				symbols = syms
				response = None
			else:
				response = eliza_chatbot.converse2(user_text)
				plot_html = None #matplotfig(x, y)

		portfolio_id = _portfolio_id(request)
		portfolio_qs = Portfolio.objects.filter(portfolio_id=portfolio_id)
		if portfolio_qs.exists():
			portfolio = portfolio_qs.first()
			portfolio_symbols = PortfolioSymbol.objects.filter(portfolio_id=portfolio.id).all()

		return render(request, 'chat/chat.html', {'response': response, 'symbols': symbols, 'portfolio_symbols': portfolio_symbols, 'chat_figure': plot_html, 'num_visits': num_visits})
		# return render(request, 'chat/home.html', {'response': response, 'chat_figure': plot_html})


	else:
		return render(request, 'chat/chat.html', {'response': '', 'chat_figure': None})


def portfolio_home(request):
	plot_html = None

	query_symbols = Symbols.objects.all()
	symbols = []
	for sym in query_symbols:
		symbols.append(sym.symbol)
	# hard coded for now
	symbols = ['AAPL', 'AMZN', 'BA', 'FB', 'GOOGL', 'MSFT', 'NVDA', 'PFE', 'PG', 'PYPL', 'QCOM', 'SPY', 'TSLA', 'GS', 'RTX', 'XOM']


	response = None
	portfolio_symbols = None

	if request.method == 'POST':

		# Check the form data are valid or not

		# Read the submitted values
		user_text = request.POST.get("query")
		print('POST : ', request.POST)

		symbol = request.POST.get('tickers')
		pct    = request.POST.get('pcts')
		print('BEFORE PORT ID')
		if symbol and pct:
			update_symbol(request, symbol, pct=float(pct))


		portfolio_id = _portfolio_id(request)
		print("PORT ID", portfolio_id)
		portfolio_qs = Portfolio.objects.filter(portfolio_id=portfolio_id)
		if portfolio_qs.exists():
			portfolio = portfolio_qs.first()
			portfolio_symbols = PortfolioSymbol.objects.filter(portfolio_id=portfolio.id)
			
			portfolio_symbols_val = portfolio_symbols.values('symbol_id')


			# rets = OHLCV.objects.values_list('symbol__exch', 'date', 'ret')

			portfolio_symbols = list(portfolio_symbols.all())
			wts = [float(items.pct)/100.0 for items in portfolio_symbols]
			pcts_total = np.round(sum(wts*100),2)

			# print(type(portfolio_symbols[0]), type(portfolio_symbols))
			print(portfolio_symbols, "PORTFOLIO SYMNOBLS")
			portfolio_symbols.append({'symbol_id': "TOTAL: ", "pct": pcts_total})
			rets = list(OHLCV.objects.filter(symbol__in=portfolio_symbols_val).values('symbol', 'date', 'ret'))
			retdf = pd.DataFrame(rets)


			rets2 = retdf.set_index(['date', 'symbol'])
			print(rets2.dtypes)
			retdf = rets2.astype(float)
			retdf = retdf.unstack()

			# print(rets3.head(5))

			# grped = retdf.groupby('symbol', as_index=False)[('date', 'ret')]
			
			# # retdf2 = pd.merge(map(lambda x: x[1].set_index('date'), grped), left_on='date', right_on='date')
			# retdf = pd.concat(map(lambda x: x[1].drop('symbol',axis=1).set_index('date'), grped),axis=1, ignore_index=True).astype(float)
			# retdf.columns = list(grped.groups.keys())

			print(wts, retdf.head(3))

			retdf_scaled = retdf * wts

			# retwdf = retdf_scaled.sum(axis=1)
			retwdf = retdf_scaled.agg(['sum'], axis=1)
			retwdf.columns = ['Ret']

			RR  = raw_return(retwdf)
			DUR = duration(retwdf)
			AR  = annualized_return(retwdf)
			SHR = sharpe_ratio(retwdf)
			ASR = annualized_standard_deviation(retwdf)
			CR  = calmar_ratio(retwdf)
			SR  = sortino_ratio(retwdf)

			print(retwdf.head(3), type(retwdf))
			print(retwdf.isnull().values.any(), "NULLLLLLL")
			print(AR, SHR, "NNNNNNNNNNNNNNNNNNNNNN")

			html_table  = "<div> <table id='res_table' width=350px border='1'> <th> </ht> <th> </th> "
			html_table += "<tr> <td> Portfolio Anualized Return (%) </td> <td>" + str(np.round((AR.values[0][1]*100.0),2)) + "</td></tr>"
			html_table += "<tr> <td> Portfolio Sharpe Ratio </td> <td>" + str(np.round((SHR.values[0][1]),4)) + "</td></tr>"
			html_table += "<tr> <td> Annualized Std Deviation </td> <td>" + str(np.round((ASR.values[0][1]*100.0),2)) + "</td></tr>"
			html_table += "<tr> <td> Portfolio Raw Return (%) </td> <td>" + str(np.round((RR.values[0][1]*100.0),2)) + "</td></tr>"
			html_table += "<tr> <td> Time Series Duration (Years) </td> <td>" + str(np.round(DUR,2)) + "</td></tr>"
			html_table += "<tr> <td> Portfolio Calmer Ratio (%) </td> <td>" + str(np.round((CR.values[0][1]*100.0),2)) + "</td></tr>"
			html_table += "<tr> <td> Portfolio Sortino Ratio (%) </td> <td>" + str(np.round((SR.values[0][1]*100.0),2)) + "</td></tr>"


			html_table += "</table> </div>"

			plot_html = html_table


			cov = retdf.cov()
			plot_html += "<br><br> RETURN COVARIANCE "
			plot_html += cov.style.background_gradient(cmap='coolwarm').render()
			print(type(plot_html))
			plot_html += "<br><br> RETURN CORR "
			corr = retdf.corr()
			plot_html += corr.style.background_gradient(cmap='coolwarm').set_precision(3).render()



	return render(request, 'chat/portfolio.html', {'response': response, 'symbols': symbols, 'portfolio_symbols': portfolio_symbols, 'port_figure': plot_html})



#### misc. #######

def sessfun(request):
	num_visits = request.session.get('num_vists', 0) + 1
	request.session['num_visits'] = num_visits
	if num_visits > 4:
		del(request.session['num_visits'])
	return HttpResponse('view count = ' + str(num_visits))

def cookie(request):
	print(request.COOKIES)
	resp = HttpResponse('C is for cookie and ... ')
	resp.set_cookie('zap', 24) # no expired date
	resp.set_cookie('asim', 42, max_age=1000) # seconds until expires
	return resp 

'''
console.log(document.getElementById("port_table").rows[1].cells[2].innerHTML)



'''