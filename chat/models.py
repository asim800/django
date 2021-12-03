from django.db import models
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User


class Chat(models.Model):
	text = models.TextField()

class Symbols(models.Model):
	symbol= models.CharField(max_length=8, primary_key=True, null=False)	
	name 	= models.CharField(max_length=25, null=True, blank=True)
	exch  = models.CharField(max_length=8, null=True, blank=True)

class OHLCV(models.Model):
	# id    = models.SmallIntegerField(null=False)
	symbol= models.ForeignKey(Symbols, on_delete=models.CASCADE, db_column='symbol')
	# symbol= models.ForeignKey(Symbols, on_delete=models.CASCADE)
	date 	= models.DateField()
	time  = models.TimeField()
	open	= models.DecimalField(max_digits=10, decimal_places=4)
	high	= models.DecimalField(max_digits=10, decimal_places=4)
	low 	= models.DecimalField(max_digits=10, decimal_places=4)
	close	= models.DecimalField(max_digits=10, decimal_places=4)
	ret  	= models.DecimalField(max_digits=10, decimal_places=6)

	volume= models.IntegerField()

	class Meta:
		unique_together = ['symbol', 'date', 'time']
	
	def __str__(self):
		return self.symbol + ' | ' + str(self.date)


	def get_absolute_url(self):
		# return reverse('blog-detail-view', args=(str(self.id)))
		return reverse('chat-home')

	def __unicode__(self):
			return u"%s" % self.user


class Portfolio(models.Model):
	portfolio_id = models.CharField(max_length=250, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	# generate random id if no user info
	# user = models.ForeignKey(User, on_delete=models.CASCADE)


class PortfolioSymbol(models.Model):
	portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT) # TODO
	symbol = models.ForeignKey(Symbols, on_delete=models.PROTECT)  # TODO not sure PROTECT is right
	pct    = models.DecimalField(max_digits=5, decimal_places=2)


###############################

class ratios(models.Model):
	symbol 	= models.OneToOneField(Symbols, primary_key=True, on_delete=models.CASCADE)  # TODO not sure PROTECT is right
	date 		= models.DateField()
	profitMargins			= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	grossMargins			= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	operatingMargins	= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	ebitdaMargins			= models.DecimalField(max_digits=8, decimal_places=4, null=True)

	returnOnAssets		= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	returnOnEquity		= models.DecimalField(max_digits=8, decimal_places=4, null=True)

	forwardEps				= models.DecimalField(max_digits=8, decimal_places=3, null=True)
	trailingEps				= models.DecimalField(max_digits=8, decimal_places=3, null=True)
	forwardPE					= models.DecimalField(max_digits=8, decimal_places=3, null=True)
	trailingPE				= models.DecimalField(max_digits=8, decimal_places=3, null=True)

	quickRatio				= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	currentRatio			= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	
	beta							= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	debtToEquity			= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	payoutRatio				= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	priceToBook				= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	shortRatio				= models.DecimalField(max_digits=8, decimal_places=4, null=True)
	pegRatio					= models.DecimalField(max_digits=8, decimal_places=4, null=True)

	revenuePerShare  	= models.DecimalField(max_digits=8, decimal_places=3, null=True)
	revenueGrowth			= models.DecimalField(max_digits=8, decimal_places=3, null=True)
	earningsGrowth		= models.DecimalField(max_digits=8, decimal_places=3, null=True)
	totalCashPerShare	= models.DecimalField(max_digits=8, decimal_places=3, null=True)

	class Meta:
		unique_together = ['symbol', 'date']


class stocks(models.Model):
	symbol = models.OneToOneField(Symbols, primary_key=True, on_delete=models.CASCADE)  # TODO not sure PROTECT is right
	date 		= models.DateField()
	ebitda							= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	grossProfits				= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	freeCashflow				= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	totalCash						= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	totalRevenue				= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	totalDebt						= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	sharesOutstanding		= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	netIncomeToCommon		= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	averageVolume				= models.DecimalField(max_digits=18, decimal_places=0, null=True)
	averageVolume10days	= models.DecimalField(max_digits=18, decimal_places=0, null=True)

	class Meta:
		unique_together = ['symbol', 'date']







###############################


# class Customer(models.Model):
# 	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
# 	email = models.CharField(max_length=100, null=True, blank=True)
# 	device= models.CharField(max_length=200, null=True, blank=True)

# 	def __str__(self):
# 		if self.name:
# 			name = self.name
# 		else:
# 			name = self.device

# 		return str(name)

	# class Meta:
	# 	db_table = 'ohlcv'
'''
## model.py

from django.db import models
from carts.models import Cart
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save


ORDER_STATUS_CHOICES= (
    ('Not Yet Shipped', 'Not Yet Shipped'),
    ('Shipped', 'Shipped'),
    ('Cancelled', 'Cancelled'),
    ('Refunded', 'Refunded'),
    )

class Order(models.Model):
    order_id= models.CharField(max_length=120, blank= True)
    cart= models.ForeignKey(Cart)
    status= models.CharField(max_length=120, default='Not Yet Shipped', choices= ORDER_STATUS_CHOICES)
    shipping_total= models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


## utils.py
import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    order_new_id= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(order_id= order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_new_id

'''