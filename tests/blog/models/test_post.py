# tests/blog/models/test_post.py

from model_bakery import bakery
import pytest
import datetime as dt
from freezegun import freeze_time
from blog.models import Post
from django.utils import timezone

# Mark this test module as requiring the database
pytestmark = pytest.mark.django_db
@freeze_time(dt.datetime(2030, 6, 1, 12), tz_offset=0)  # Replaces now()
def test_publish_sets_published_to_current_datetime():
    # Create a new post, and ensure no published datetime is set
    post = bakery.make('blog.Post', published=None)
    post.publish()

    # Set the timezone to UTC (to match tz_offset=0)
    assert post.published == dt.datetime(2030, 6, 1, 12, tzinfo=dt.timezone.utc)

def test_publish_sets_status_to_published():
    post = bakery.make('blog.Post', status=Post.DRAFT)
    post.publish()
    assert post.status == Post.PUBLISHED

def test_published_posts_only_returns_those_with_published_status():
    # Create a published Post by setting the status to "published"
    published = bakery.make('blog.Post', status=Post.PUBLISHED)
    # Create a draft Post
    bakery.make('blog.Post', status=Post.DRAFT)

    # We expect only the "publised" object to be returned
    expected = [published]
    # Cast the result as a list so we can compare apples with apples!
    # Lists and querysets are of different types.
    result = list(Post.objects.published())

    assert result == expected
