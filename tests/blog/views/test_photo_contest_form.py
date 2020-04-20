# tests/blog/views/test_contact_form.py
from io import BytesIO
from PIL import Image
import pytest
from blog.models import PhotoContest

pytestmark = pytest.mark.django_db

def test_valid_form_submission(client, settings, tmpdir):
    # Set media root to a pytest temporary dir
    settings.MEDIA_ROOT = tmpdir
    # Create an image in memory and save to a file buffer
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = BytesIO()
    image.save(file, 'png')
    file.name = 'pytest.png'
    file.seek(0)
    data = {
        'first_name': 'George',
        'last_name': 'Costanza',
        'email': 'gcostanza@vandelay.com',
        'photo': file
    }
    print(file.read(0))
    client.post('/PhotoContest/', data)

    # There should only be one object in the database
    obj = PhotoContest.objects.get()
    assert obj.first_name == data['first_name']
    assert obj.last_name == data['last_name']
    assert obj.email == data['email']
    assert obj.photo == data['photo']
