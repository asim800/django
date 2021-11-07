from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


# Create your models here.

class Blog(models.Model):
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255, blank=True)
	# description = models.CharField(max_length=255, default="My super blog")
	author = models.CharField(max_length=255, blank=True)
	signature = models.CharField(max_length=255, blank=True)
	content = RichTextField()
	# content = models.TextField()
	image = models.ImageField(null=True, blank=True, upload_to='blogs/images/')
	created_at = models.DateTimeField(auto_now_add=True)
	# created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True)
	# url   = models.URLField(blank=True)
	# currentdate= models.DateField(default=timezone.now)
	_DATABASE = "blog_db"

	def __str__(self):
		return self.title + ' | ' + str(self.author)


	def get_absolute_url(self):
		# return reverse('blog-detail-view', args=(str(self.id)))
		return reverse('blog-home')

	# def total_likes(self):
	# 	return self.likes.count()

	def __unicode__(self):
			return u"%s" % self.user

class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	_DATABASE = "blog_db"






# class Post(models.Model):
# 	title = models.CharField(max_length=255)
# 	title_tag = models.CharField(max_length=255)
# 	author = models.ForeignKey(User, on_delete=models.CASCADE)
# 	body = RichTextField(blank=True, null=True)
# 	post_date = models.DateField(auto_now_add=True)
# 	category = models.CharField(max_length=255)
# 	likes = models.ManyToManyField(User, related_name='blog_posts')



