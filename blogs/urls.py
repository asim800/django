from django.urls import path
from . import views



urlpatterns = [
	path('', views.BlogHomeView.as_view(), name='blog-home'),
	path('view/', views.HomeView.as_view(), name='blog-home-view'),
	path('article/<int:pk>', views.ArticleDetailView.as_view(), name='blog-detail-view'),
	path('add_blog/', views.AddBlogView.as_view(), name='add-blog'),
	path('add_comment/<int:blog_id>', views.AddCommentView.as_view(), name='add-comment'),
	path('article/edit/<int:blog_id>/', views.UpdateBlogView.as_view(),  name='update-blog'),
	path('article/delete/<int:blog_id>/', views.DeleteBlogView.as_view(),  name='delete-blog'),
	# path('', views.blogs_home, name='blog-home'),
	path('<int:blog_id>/', views.blog_detail, name='detail'),
	path('like/<int:pk>', views.like_blog, name='like-blog')

]
	# path('article/edit/<int:pk>/', views.UpdateBlogView.as_view(), {'columns': {'a': 1}}, name='update-blog'),

