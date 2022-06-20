"""blog/models"""
from django.conf import settings
from django.db import models

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

class Post(models.Model):
    """Blog Post"""
    #Create choices for Status
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
