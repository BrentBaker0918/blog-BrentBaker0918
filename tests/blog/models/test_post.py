# tests/blog/test_post.py

import pytest
from model_mommy import mommy
import datetime as dt
from freezegun import freeze_time
# Mark this test module as requiring the database
pytestmark = pytest.mark.django_db


@freeze_time(dt.datetime(2030, 6, 1, 12), tz_offset=0) # replaces now()
def test_publish_sets_published_to_current_datetime():
    # Create a new post, and ensure no published datetime is set
    post = mommy.make('blog.Post', published=None)
    post.publish()

    # Set the timezone to UTC (to match tz_offset=0)
    assert post.published == dt.datetime(2030, 6, 1, 12, tzinfo=dt.timezone.utc)

def test_published_posts_only_returns_those_with_published_status():
    # Create a published Post by setting the status to "published"
    published = mommy.make('blog.Post', status=post.PUBLISHED)
    # Create a draft Post
    mommy.make('blog.Post', status=post.DRAFT)

    # We expect only the "publised" object to be returned
    expected = [published]
    # Cast the result as a list so we can compare apples with apples!
    # Lists and querysets are of different types.
    result = list(Post.objects.published())

    assert result == expected

def test_publish_sets_status_to_published():
    post = mommy.make('blog.Post', status=Post.DRAFT)
    post.publish()
    assert post.status == Post.PUBLISHED