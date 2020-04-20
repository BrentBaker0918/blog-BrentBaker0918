from django.conf import settings # imports Django's loaded settings
from django.db import models
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
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
    def save(self, *args, **kwargs):
        strip_name = self.name.replace(" ", "")
        self.slug = slugify(strip_name)
        super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("topic_detail", kwargs={"slug", self.slug})
class PostQuerySet(models.QuerySet): # querys for Post class
    def published(self): # filter to the published items
        return self.filter(status=self.model.PUBLISHED)
    def drafts(self): # filter to the draft items
        return self.filter(status=self.model.DRAFT)
    def contains(self, test_word): #filter to items containing test text
        local_test_word = str(test_word).lower()
        return self.filter(Q(title__icontains=local_test_word)|Q(content__icontains=local_test_word))
    def top_user(self): # find the user with the most posts
        users = User.objects.anotate(total_posts=Count('blog_posts'))
        myQuerySet = users.order_by('-total_posts').values('username', 'total_posts')
        return myQuerySet[0]
    def delete_post_and_comments(self, post): # delete a post and all comments
        post.delete() # as comments are set to cascade all comments are deleted
    def get_all_authors(self):
        # Get the authors for all posts
        Post.objects.all().get_authors()
    def get_my_topics(self):
        return models.Topic.filter(name=self.blog_posts)
    def get_published_authors(self):
        # Get the authors for published posts only (use existing `published()` query)
        Post.objects.published().get_authors()

    def get_authors_published_today(self):
        Post.objects.published() \
        .filter(published__gte=timezone.now().date()) \
        .get_authors()

    def get_authors(self):
        User = get_user_model()
        #get the author of this QuerySet
        return User.objects.filter(blog_posts__in=self).distinct()

    def topic_posts(self, a_topic):
        post_ids = []
        my_object = Topic.objects.filter(name=a_topic.get('object'))
        # print(my_object.values('pk'))
        # print(my_object.values('pk').values_list('pk')[0][0])
        for my_post in Post.objects.published().order_by('-published'):
            for topics in my_post.topics.all():
                # .filter(status=self.model.PUBLISHED)
                if my_object.values('pk').values_list('pk')[0][0] == topics.id:
                    post_ids.append(Post.objects.filter(pk=my_post.id))
        return post_ids

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
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True) #sets on create
    updated = models.DateTimeField(auto_now=True) # Updates on each save
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='blog_posts', null=False, )# the Django auth user models on_delete=models.PROTECT, # prevent posts from being deleted related_name='blog_posts', #"this" on the user model
    published = models.DateTimeField(null=True, blank=True, help_text='The date & time this article was published',)
    slug = models.SlugField(help_text='reference for the blog post', unique_for_date='published',) #slug is unique for publication date
    topics = models.ManyToManyField(Topic, related_name='blog_posts')

    banner = models.ImageField(blank=True, null=True, help_text='A banner image for the post')

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
class CommentQuerySet(models.QuerySet):
    def approved(self): # filter to published comments
        return self.filter(approved=self.model.PUBLISHED)
    def statusPending(self): # filter to draft comments
        return self.filter(approved=self.model.DRAFT)
    def most_active_post(self): # post with most comments
        posts = Post.objects.annotate(total_comments=Count('comments'))
        my_query_set = posts.order_by('-total_comments')
        return my_query_set[0]
    def make_comment(self, post): # add a comment to a given post
        comment = Comment.objects.create(name='Brent', post=post, approved=False, email='myemail@hotmail.com', text='here is a comment', )
        return comment
    def make_comment_draft(self, comment): # set status of a post to draft
        comment.approved = False
        comment.save()

class Comment(models.Model):

    objects = CommentQuerySet.as_manager()
    DRAFT = False
    PUBLISHED = True
    STATUS_CHOICES = [(DRAFT, False), (PUBLISHED, 'approved')]
    approved = models.BooleanField(max_length=1, choices=STATUS_CHOICES, default=DRAFT, help_text='Set to "published" to make this approved',)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', null=False, )# link comments to a post with the common name of comments
    name = models.CharField(
        max_length=50,
        unique=True, # No duplicates!
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        null=False,
    )
    text = models.TextField(
        max_length=2000,
        null=False,
    )

    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created']
class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'

class PhotoContest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    photo = models.ImageField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'
