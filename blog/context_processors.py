# blog/context_processors.py
from . import models
from blog.models import Topic
from django.db.models import Count

def base_context(request):

    top_10_topics= Topic.objects.annotate(blog_count = Count('blog_posts')).order_by('-blog_count')[:10].values('name','blog_count')
    topics_info = Topic.objects.annotate(blog_count = Count('blog_posts')).order_by('-blog_count')[:10]

    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    return {'top_10_topics':top_10_topics,
            'topics_info': topics_info,
            'authors': authors,}
