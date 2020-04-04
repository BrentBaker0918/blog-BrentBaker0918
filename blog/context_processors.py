from django.shortcuts import render
from django.db.models import Count
from django.views.generic.base import TemplateView
from . import models
# blog/context_processors.py

def base_context(request):
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    top_topics = models.Topic.objects.order_by('-blog_posts__count').annotate(Count('blog_posts')).values('id','name','slug', 'blog_posts__count')
    all_topics = models.Topic.objects.order_by('-blog_posts__count').annotate(Count('blog_posts')).values('name', 'slug')
    all_posts = models.Post.objects.published().order_by('-published')
    return {'authors' : authors, 'latest_posts': latest_posts, 'topics': top_topics[0:10],'all_posts':all_posts, 'all_topics':all_topics}
