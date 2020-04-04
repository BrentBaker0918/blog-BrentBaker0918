# tests/blog/views/test_post_list.py
from model_mommy import mommy
import pytest
from blog.models import Post
pytestmark = pytest.mark.django_db


def test_post_list_url_returns_200(client):
    response = client.get('/posts/')
    assert response.status_code
def test_post_list_only_returns_published_articles(client):
    published = mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        title='Published post'
    )
    mommy.make(
        'blog.Post',
        status=Post.DRAFT,
        title='Draft post'
    )

    response = client.get('/posts/')
    # Get the posts object_list
    result = response.context.get('posts')

    assert list(result) == [published]
