# blog/views.py

from django.shortcuts import render
from . import models



def home(request):
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    topics = models.Post.objects.get_topics()[:10]
    # Add as context variable "latest_posts"
    context = {
        'topics': topics,
        'latest_posts': latest_posts
    }
    return render(request, 'blog/home.html', context)
