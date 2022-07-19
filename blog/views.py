""" blog/views.py"""
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import render
#from django.views import View
from . import models



class HomeView(TemplateView):
    """Home View"""
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)
        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        context.update({'latest_posts': latest_posts})

        return context

class AboutView(TemplateView):
    """About View"""
    template_name = 'blog/about.html'

def terms_and_conditions(request):
    """Terms and Conditions"""
    return render(request, 'blog/terms_and_conditions.html')

class PostListView(ListView):
    """Post List View"""
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')

class TopicListView(ListView):
    """Topic List View"""
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Post.objects.get_topics().order_by('name')

class PostDetailView(DetailView):
    """Post Detail"""
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

class TopicDetailView(DetailView):
    """Topic Detail view"""
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().self()

        # Otherwise, filter on the published date
        return queryset.filter(
            name=self.kwargs['name'],
        )
