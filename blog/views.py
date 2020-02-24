# Create your views here.
from django.shortcuts import render
from django.db.models import Count
from . import models

def home(request):
    """
    The Blog homepage
    """
    # get last 3 Posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    top_topics = models.Topic.objects.order_by('-blog_posts__count').annotate(Count('blog_posts')).values('name', 'blog_posts__count')
    # Add as context variable "latest_posts"
    context = {'authors' : authors, 'latest_posts': latest_posts, 'topics': top_topics[0:10]}
    return render(request, 'blog/home.html', context)
