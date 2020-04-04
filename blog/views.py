# blog / views.py
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from . import models


class HomeView(TemplateView):
    """
    The Blog homepage
    """
    template_name = 'blog/home.html'
    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        return context

class AboutView(TemplateView):
    # def get(self, request):
    #     return render(request, 'blog/about.html')
    template_name = 'blog/about.html'

def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')

class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')  # Customized queryset

class PostDetailView(DetailView):
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

class TopicListView(ListView):
    model = models.Topic
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class TopicDetailView(DetailView):
    model = models.Topic
    context_object_name = 'topic_details'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        # Create any data and add  to the context
        context['topic_id'] = kwargs
        context['topic_posts'] = models.Post.objects.topic_posts(kwargs)
        return context
