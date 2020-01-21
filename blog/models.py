from django.conf import settings # imports Django's loaded settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True  # No duplicates!
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

class Post(models.Model):
    """
    represents a blog post
    """
    objects = PostQuerySet.as_manager()
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [(DRAFT, 'Draft'), (PUBLISHED, 'Published')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT, help_text='Set to "published" to make this publicly visible',)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True) #sets on create
    updated = models.DateTimeField(auto_now=True) # Updates on each save
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT) # the Django auth user models on_delete=models.PROTECT, # prevent posts from being deleted related_name='blog_posts', #"this" on the user model
    published = models.DateTimeField(null=True, blank=True, help_text='The date & time this article was published',)
    slug = models.SlugField(help_text='reference for the blog post', unique_for_date='published',) #slug is unique for publication date
    topics = models.ManyToManyField(Topic, related_name='blog_posts')
    class Meta:
        # Sort by the `created` field. The `-` prefix
        # specifies to order in descending/reverse order.
        # Otherwise, it will be in ascending order.
        ordering = ['-created']
    def __str__(self):
        return self.title
    def publish(self):
        self.status = self.PUBLISHED
        self.published = timezone.now()
