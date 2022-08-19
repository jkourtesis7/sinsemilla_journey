""" api/urls.py """

# Create an app-specific urls.py for the API inside its app.
# Then include it in the blog/urls.py module

from django.urls import path
from . import views

# Namespace for the API app
app_name = 'api'

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/like/', views.CommentLikeView, name='comment-like'),
    path('comments/<int:pk>/dislike/', views.CommentDislikeView, name='comment-dislike'),
]
