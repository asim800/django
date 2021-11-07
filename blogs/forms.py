from django import forms
from .models import Blog
from django.forms.widgets import FileInput

class BlogForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ('title', 'description', 'author', 'signature', 'content', 'image')
		# fields = ('title', 'description', 'author', 'signature', 'content', )

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.TextInput(attrs={'class': 'form-control'}),
			'author': forms.TextInput(attrs={'class': 'form-control'}),
			'signature': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control'}),
			# 'image': forms.ImageField('photo'=FileInput()),
		}

	# def save(self, user=None):
	# 	user_blog = super(BlogForm, self).save(commit=False)
	# 	# if user:
	# 	# 		user_profile.user = user
	# 	user_blog.save()
	# 	return user_blog



# class UserProfileForm(forms.ModelForm):
#     photo = ImageField(widget=PictureWidget)