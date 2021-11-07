import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from django.http import HttpResponse
from django.urls import reverse


from .models import Blog
from .forms import BlogForm

import ipdb

# Create your views here.


def blogs_home(request):
	# top_blogs = Blog.objects.order_by('-date')[5]
	top_blogs = Blog.objects.all().order_by('-created_at')[:5]
	

	return render(request, 'blogs/home.html', {'blogs': top_blogs})


def blog_detail(request, blog_id):
	blog = get_object_or_404(Blog, pk=blog_id)
	# return render(request, 'blog/detail.html', {'id':blog_id})
	return render(request, 'blogs/detail.html', {'blog':blog})


class HomeView(ListView):
	model = Blog
	template_name = 'blogs/home_view.html'
	ordering = ['-created_at']


class ArticleDetailView(DetailView):
	model = Blog
	template_name = 'blogs/article_detail.html'

class AddBlogView(CreateView):
	model = Blog
	template_name = 'blogs/add_blog.html'
	fields = '__all__'




class UpdateBlogView(UpdateView):
	model = Blog
	template_name = 'blogs/update_blog.html'
	# fields = ['title', 'content']
	form_class = BlogForm

	def get_object(self):
		pk_ = self.kwargs.get("blog_id")
		# print('getobj update view ', self.kwargs)
		return get_object_or_404(Blog, pk=pk_)


class DeleteBlogView(DeleteView):
	model = Blog
	template_name = 'blogs/delete_blog.html'
	# fields = ['title', 'content']
	form_class = BlogForm

	def get_object(self):
		pk_ = self.kwargs.get("blog_id")
		# print('getobj update view ', self.kwargs)
		return get_object_or_404(Blog, pk=pk_)

	def get_absolute_url(self):
		# return reverse('blog-detail-view', args=(str(self.id)))
		return reverse('blog-home')

	def get_success_url(self):
		return reverse('blog-home')



##############################################

# from django.views import View
# class CourseView(View):
# 	template_name = 'about.html'
# 	# GET method
# 	def get(self, request, *args, **kwargs):
# 		context = {}
# 		if id is not None:
# 			obj = get_object_or_404(Course, id=id)
# 			context['object'] = obj
# 		return render(request, 'about.html', context)

# 	# POST method
# 	def post(self, request, *args, **kwargs):
# 		return render(self, request, self.template_name, {})



# class UpdateBlogView2(UpdateView):
# 	model = Blog
# 	template_name = 'blogs/update_blog.html'
# 	# fields = ['title', 'content']
# 	form_class = BlogForm


# 	blog1 = Blog.objects

# 	my_form = BlogForm()
# 	if my_form.is_valid():
# 		print('Valid.....', my_form.cleaned_data)
# 	else:
# 		print('Valid errors...', my_form.errors)

# 	# ipdb.set_trace()
# 	# print(blog1.get(pk=1))
# 	# print(dir(__module__))
# 	print(blog1.get(pk=2))
# 	# fields = ['title', 'description', 'content', 'image']

# 	def form_valid(self, form):
# 		print("URL ", self.get_success_url())
# 		blog = form.save(commit=False)


# 		# blog.content = "abcd"
# 		print('FORM 1111', blog)

# 		# print('FORM.....      ', dir(self))
# 		# print('FORM.....      ', form)
# 		# ipdb.set_trace()
# 		return super(UpdateBlogView, self).form_valid(form)



# 	# def get_object(self, **kwargs):
# 	# 	print('0000000', self.kwargs)
# 	# 	self.object = self.get_object()
# 	# 	return super().get(request, *args, **kwargs)
# 	# 	# return Blog.objects.get(id=self.kwargs['pk'])


# 	def post2(self, request, *args, **kwargs):
# 		if request.method == 'POST':
# 			print('POSSSST')
# 		# self.object = self.get_object()
# 		# print('post0....', self.object)
# 		# print('post....', self.object.created_at)
# 		print('post', dir(self))
# 		print('post1', self.__class__)
# 		obj = self.get_object()
# 		print('post2', dir(obj))
# 		print('post3', obj.created_at)
# 		print("GETTTTTT  TTTTTTTT", request.GET)
# 		print("POST", request.POST)


# 		self.object = self.get_object()
# 		if self.object.created_at is None:
# 			self.object.created_at = datetime.datetime.now()
# 			print('CREATED AT UPDATED')
# 		print('created at ', self.object.created_at)

# 		my_form = BlogForm(request.POST)
		
# 		if my_form.is_valid():
# 			print('Valid.....', my_form.cleaned_data)
# 		else:
# 			print('Valid errors...', my_form.errors)

# 		# return HttpResponse("return this string")
# 		return super().post(request, *args, **kwargs)




# 	def product_create_view(request):
# 		my_form = BlogForm(request.POST or None)

# 		if my_form.is_valid():
# 			form.save()
# 			form = BlogForm()
		
# 		context = {
# 			'form': my_form,
# 		}
# 		return render(request, 'blogs/add_blog.html', context)


# class todoDetailView(DetailView):
# model = models.todo
# # context_object_name = 'todo_detail'

#  def get_object(self, **kwargs):
#     print(kwargs)
#     return models.todo.objects.get(id=self.kwargs['id'])
	# title = models.CharField(max_length=255)
	# description = models.CharField(max_length=255, blank=True)
	# author = models.CharField(max_length=255, blank=True)
	# signature = models.CharField(max_length=255, blank=True)
	# content = models.TextField()
	# image = models.ImageField(null=True, blank=True, upload_to='blogs/images/')
	# created_at = models.DateTimeField(auto_now_add=True)
	# updated_at = models.DateTimeField(auto_now=True)



	# https://stackoverflow.com/questions/41708360/passing-url-variables-to-a-class-based-view
	# class Journal_Article_List(ListView):
  #   template_name = "journal_article_list.html"
  #   model = Articles
  #   queryset = Articles.objects.filter(JOURNAL_ID = journal_id)
  #   paginate_by = 12

  #   def get_context_data(self, **kwargs):
  #       context = super(Journal_Article_List, self).get_context_data(**kwargs)
  #       context['range'] = range(context["paginator"].num_pages)
  #       return context


	# 			def get_queryset(self):
  #   return Articles.objects.filter(JOURNAL_ID=self.kwargs['journal_id'])