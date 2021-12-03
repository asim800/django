from django import forms
from .models import Blog, Comment, Tag
from django.forms.widgets import FileInput

class BlogForm(forms.ModelForm):
	mytags = forms.ModelChoiceField(queryset=Tag.objects.all(), to_field_name='tag', empty_label='Select Keywords')
	tagsObj = list(Tag.objects.all().values_list('tag', flat=True))
	TAGS = [(x, x) for x in tagsObj]
	print(TAGS)
	print("MY T", mytags)
	class Meta:
		model = Blog
		fields = ('title', 'description', 'mytags',  'is_public', 'signature', 'content', 'image' )
		# fields = ('title', 'description', 'author', 'signature', 'content', )
		YES_NO_CHOICES = [(False, False), (True, True)]


		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			# 'tags' : forms.MultipleChoiceField(widget=forms.Select, choices=TAGS),
			# 'tags': forms.Select(choices=YES_NO_CHOICES),
			'tags' : forms.Select(attrs={'class': 'form-control'}),
			'is_public' : forms.Select(choices=YES_NO_CHOICES),
			'description': forms.TextInput(attrs={'class': 'form-control'}),
			'signature': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control'}),

			# 'image': forms.ImageField('photo'=FileInput()),
			# 'author': forms.TextInput(attrs={'class': 'form-control'}),
		}

	# def save(self, user=None):
	# 	user_blog = super(BlogForm, self).save(commit=False)
	# 	# if user:
	# 	# 		user_profile.user = user
	# 	user_blog.save()
	# 	return user_blog



# class UserProfileForm(forms.ModelForm):
#     photo = ImageField(widget=PictureWidget)


			# 'tags' : forms.Select(attrs={'class': 'form-control'}),
			# 'tags' : forms.Select(choices=TAGS),

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text', )
		# fields = ('title', 'description', 'author', 'signature', 'content', )

		widgets = {
			# 'name': forms.TextInput(attrs={'class': 'form-control'}),
			'text': forms.Textarea(attrs={'class': 'form-control'}),
		}