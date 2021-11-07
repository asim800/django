from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Chat(models.Model):
	text = models.TextField()

class OHLCV(models.Model):
	# id    = models.SmallIntegerField(null=False)
	symbol= models.CharField(max_length=24, primary_key=True)
	date 	= models.DateField()
	time  = models.TimeField()
	open	= models.DecimalField(max_digits=18, decimal_places=4)
	high	= models.DecimalField(max_digits=18, decimal_places=4)
	low 	= models.DecimalField(max_digits=18, decimal_places=4)
	Close	= models.DecimalField(max_digits=18, decimal_places=4)
	volume= models.IntegerField()
	_DATABASE = 'fin_db'
	
	def __str__(self):
		return self.symbol + ' | ' + str(self.date)


	def get_absolute_url(self):
		# return reverse('blog-detail-view', args=(str(self.id)))
		return reverse('chat-home')

	# def total_likes(self):
	# 	return self.likes.count()

	def __unicode__(self):
			return u"%s" % self.user

