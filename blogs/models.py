from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


# Create your models here.
class Tag(models.Model):
	tag = models.CharField(max_length=16)

	def __str__(self):
		return self.tag

class Blog(models.Model):
	title = models.CharField(max_length=255)
	tags = models.ForeignKey(Tag, on_delete=models.PROTECT, null=True, blank=True)
	description = models.CharField(max_length=255, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	signature = models.CharField(max_length=255, blank=True)
	content = RichTextField()
	image = models.ImageField(null=True, blank=True, upload_to='blogs/images/')
	likes = models.ManyToManyField(User, related_name='blog_post')
	is_public = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.title + ' | ' + str(self.author)

	def get_absolute_url(self):
		# return reverse('blog-detail-view', args=(str(self.id)))
		return reverse('blog-home')

	def __unicode__(self):
		return u"%s" % self.user

	def likes_count(self):
		return self.likes.count()


class Comment(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
	# inherit user from the Blog model - related field
	# user = models.ForeignKey(User, on_delete=models.CASCADE)

	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name 


class BlogImage(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None, related_name='images')
	images = models.ImageField(null=True, blank=True, upload_to='blogs/images/')
	# images = models.FileField(upload_to='blogs/images')



# class Vote(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


# class Post(models.Model):
# 	title = models.CharField(max_length=255)
# 	title_tag = models.CharField(max_length=255)
# 	author = models.ForeignKey(User, on_delete=models.CASCADE)
# 	body = RichTextField(blank=True, null=True)
# 	post_date = models.DateField(auto_now_add=True)
# 	category = models.CharField(max_length=255)
# 	likes = models.ManyToManyField(User, related_name='blog_posts')



	# MEMBERSHIP_CHOICES = [('B', 'Bronze'), ('S', 'Silver'), ('T', True)]
	# public = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')

	# other_name = models.CharField(max_length=255, blank=True)
	# content = models.TextField()
	# created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	# description = models.CharField(max_length=255, default="My super blog")
	# url   = models.URLField(blank=True)
	# currentdate= models.DateField(default=timezone.now)
