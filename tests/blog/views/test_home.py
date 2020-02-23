# tests/blog/views/test_home.py
from model_mommy import mommy
import pytest

from blog.models import Post, Topic, Count

# Needed for database
pytestmark = pytest.mark.django_db


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_top_topics_working(client, django_user_model):
    cosmo = mommy.make(
        django_user_model,
        username='ckramer',
        first_name='Cosmo',
        last_name='Kramer'
    )
    my_topics = mommy.make(Topic,
        _quantity=15)
    count = 0
    test_topics=[]
    for a_topic in my_topics:
        count += 1
        for item in range(count):
            test_topics = test_topics + [mommy.make(
                'Post',
                status=Post.PUBLISHED,
                author=cosmo,
                topics= [a_topic]
            )]
    top_posts = Topic.objects.order_by('-blog_posts__count').annotate(Count('blog_posts')).values('blog_posts__count')

    assert  top_posts[0].get('blog_posts__count')== 15
    assert  top_posts[10].get('blog_posts__count')== 5

def test_authors_included_in_context_data(client, django_user_model):
    """
    Checks that a list of unique published authors is included in the
    context and is ordered by first name.
    """
    # Make a published author called Cosmo
    cosmo = mommy.make(
        django_user_model,
        username='ckramer',
        first_name='Cosmo',
        last_name='Kramer'
    )
    mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=cosmo,
        _quantity=2
    )
    # Make a published author called Elaine
    elaine = mommy.make(
        django_user_model,
        username='ebenez',
        first_name='Elaine',
        last_name='Benez'
    )
    mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=elaine,
    )

    # Make an unpublished author
    unpublished_author = mommy.make(
        django_user_model,
        username='gcostanza'
    )
    mommy.make('blog.Post', author=unpublished_author, status=Post.DRAFT)

    # Expect Cosmo and Elaine to be returned, in this order
    expected = [cosmo, elaine]

    # Make a request to the home view
    response = client.get('/')

    # The context is available in the test response.
    result = response.context.get('authors')

    # Cast result (QuerySet) to a list to compare
    assert list(result) == expected
