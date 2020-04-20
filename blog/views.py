# blog / views.py

from django.shortcuts import render
from django.views.generic.base import TemplateView
from . import forms, models
from django.views.generic import DetailView, CreateView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages

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
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)

class FormViewExample(FormView):
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        self.messages.add_message(self.request, messages.SUCCESS, 'Thank you for signing up!', )
        # Continue with default behaviour
        return super().form_valid(form)

def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})

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

class FormViewPhotoContest(CreateView):
    model = models.PhotoContest
    template_name = 'blog/PhotoContest.html'
    # template_name = 'blog/form_photo_contest.html'
    # form_class = forms.PhotoContestForm
    success_url = reverse_lazy('home')
    fields = ['first_name', 'last_name', 'email', 'photo', ]
    def form_valid(self, form):
        self.messages.add_message(self.request, messages.SUCCESS, 'Thank you for submitting your photo to our contest', )
        # Continue with default behaviour
        return super().form_valid(form)

# def form_PhotoContest(request):
#     # Handle the POST
#     if request.method == 'POST':
#         # Pass the POST data into a new form instance for validation
#         form = forms.PhotoContestForm(request.POST)
#
#         # If the form is valid, return a different template.
#         if form.is_valid():
#             # form.cleaned_data is a dict with valid form data
#             cleaned_data = form.cleaned_data
#
#             return render(
#                 request,
#                 'blog/form_PhotoContest_success.html',
#                 context={'data': cleaned_data}
#             )
#     # If not a POST, return a blank form
#     else:
#         form = forms.PhotoContestForm()
#
#     # Return if either an invalid POST or a GET
#     return render(request, 'blog/form_photo_contest.html', context={'form': form})

# def form_example(request):
#     # Handle the POST
#     if request.method == 'POST':
#         # Pass the POST data into a new form instance for validation
#         form = forms.ExampleSignupForm(request.POST)
#
#         # If the form is valid, return a different template.
#         if form.is_valid():
#             # form.cleaned_data is a dict with valid form data
#             cleaned_data = form.cleaned_data
#
#             return render(
#                 request,
#                 'blog/form_example_success.html',
#                 context={'data': cleaned_data}
#             )
#     # If not a POST, return a blank form
#     else:
#         form = forms.ExampleSignupForm()
#
#     # Return if either an invalid POST or a GET
#     return render(request, 'blog/form_example.html', context={'form': form})
