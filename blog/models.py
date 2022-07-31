"""blog/models"""
from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

class PostQuerySet(models.QuerySet):
    """PostQuerySet"""
    def published(self):
        """PUBLISHED"""
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        """DRAFT"""
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        """Get Authors"""
        user = get_user_model()
        return user.objects.filter(blog_posts__in=self).distinct()

class Topic(models.Model):
    """Blog Topics"""
# Table fields
    name = models.CharField(
        max_length=50,
        unique=True
    )
    slug = models.SlugField(unique=True)
# Self
    def __str__(self):
        return self.name
# Define URL
    def get_absolute_url(self):
        """get abolust url"""
        return reverse('topic-detail', kwargs={'pk':self.pk})
# Sort Order
    class Meta:
        ordering = ['name']

class Post(models.Model):
    """
    Represents a blog post
    """
# Status choices
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

#Table headings
    title = models.CharField(
        max_length=255,
        null=False,
        )
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices = STATUS_CHOICES,
        null=False,
        default=DRAFT,
        help_text='Set to published to make this post publicly visible',
    )
    content = models.TextField()
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date and time this article was published',
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

#objects = PostManager()
    objects = PostQuerySet.as_manager()

#Set sort order
    class Meta:
        """Order by created"""
        ordering = ['-created']

# Self Title
    def __str__(self):
        return self.title

# Set current date time when published
    def publish(self):
        """Publish this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now() # The current datetime with TIME_ZONE

# Construct URL
    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)

# Create your models here.
class Comment(models.Model):
    """Blog Comments"""
# Table fields
    name = models.CharField(
        max_length=50,
        null=False,
        )
    email = models.CharField(
        max_length=255,
        null=False,
        )
    post = models.ForeignKey(
        'Post',
        on_delete=models.PROTECT,
        related_name='comments',
        null=False,
    )
    text = models.TextField(
        max_length=1000,
        null=False,
        )
    approved = models.BooleanField(
        default=True
        )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

# Sort Order
    class Meta:
        """Order comments by created"""
        ordering = ['-created']
# Define self
    def __str__(self):
        return f'{self.name} {self.updated}'

#I think this is not needed
"""
class PostManager(models.Manager):
    """"""Post manager""""""
    def get_queryset(self):
        """"""queryset - exclude deleted""""""
        queryset = super().get_queryset() #Get the initial get_queryset
        return queryset.exclude(deleted=True) # Exclude deleted records
        """
