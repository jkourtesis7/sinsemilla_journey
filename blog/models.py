"""blog/models"""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count

# Create your models here.
class Comment(models.Model):
    """Blog Comments"""
    post = models.ForeignKey(
        'Post',
        on_delete=models.PROTECT,
        related_name='comments',
        null=False,
    )
    name = models.CharField(
        max_length=50,
        null=False,
        )
    email = models.CharField(
        max_length=255,
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

    class Meta:
        """Order comments by created"""
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} {self.updated}'

class Topic(models.Model):
    """Blog Topics"""
    name = models.CharField(
        max_length=50,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class PostManager(models.Manager):
    """
    Post manager
    """
    def get_queryset(self):
        """
        queryset - exclude deleted
        """
        queryset = super().get_queryset() #Get the initial get_queryset
        return queryset.exclude(deleted=True) # Exclude deleted records

class PostQuerySet(models.QuerySet):
    """
    PostQuerySet
    """
    def published(self):
        """
        PUBLISHED
        """
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        """
        DRAFT
        """
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        """
        Get Authors
        """
        user = get_user_model()
        return user.objects.filter(blog_posts__in=self).distinct()

    def get_topics(self):
        """
        Get Topics
        """
        topics = Topic.objects.annotate(total_posts=Count('blog_posts'))
        return  topics.order_by('-total_posts').values('name','total_posts')

class Post(models.Model):
    """
    Represents a blog post
    """
    def publish(self):
        """Publish this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now() # The current datetime with TIME_ZONE

    objects = PostQuerySet.as_manager()
    #objects = PostManager()
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
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices = STATUS_CHOICES,
        null=False,
        default=DRAFT,
        help_text='Set to published to make this post publicly visible',
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date and time this article was published',
    )
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    #Set sort order
    class Meta:
        """Order by created"""
        ordering = ['-created']

    def __str__(self):
        return self.title
