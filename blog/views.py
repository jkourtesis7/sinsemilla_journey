from django.shortcuts import render
from . import forms, models
from blog.models import Topic
from django.db.models import Count
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages

def terms_and_conditions(request):
    """Terms and Conditions"""
    return render(request, 'blog/terms_and_conditions.html')

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

class PostListView(ListView):
    """Post List View"""
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')

class TopicListView(ListView):
    """Topic List View"""
    model = models.Topic
    context_object_name = 'topics'
    queryset = Topic.objects.annotate(blog_count = Count('blog_posts')).order_by('name')#.values('name','slug')

class TopicDetailView(DetailView):
    """Topic Detail view"""
    model = models.Topic

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = models.Post.objects.filter(topics=self)
        if 'pk' in self.kwargs:
            return queryset

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

def form_example(request):
    """ Form Example"""
    # Handle the Post
    if request.method =='POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.clearned_data is a dict with valid form clearned_data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})

class FormViewExample(FormView):
    """ Form View Example """
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)

class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)

class PhotoContestFormView(CreateView):
    model = models.PhotoContest
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'photo',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            'Thank you! Your photo submission has been received.'
        )
        return super().form_valid(form)
