# tests/blog/views/test_contact_form.py

import pytest

from blog.models import Contact

pytestmark = pytest.mark.django_db


def test_post_contact_form_redirect(client):
    data = {
        'first_name': 'George',
        'last_name': 'Costanza',
        'email': 'gcostanza@vandelay.com',
        'message': 'This is a test message!'
    }
    response = client.post('/contact/', data)
    assert response.status_code == 302
    assert response.url == '/'  # Home

def test_post_contact_form_saves_data(client):
    data = {
        'first_name': 'George',
        'last_name': 'Costanza',
        'email': 'gcostanza@vandelay.com',
        'message': 'This is a test message!'
    }
    client.post('/contact/', data)

    # There should only be one object in the database
    obj = Contact.objects.get()
    assert obj.first_name == data['first_name']
    assert obj.last_name == data['last_name']
    assert obj.email == data['email']
    assert obj.message == data['message']
def test_invalid_submission(client):
    data = {'fizz': 'buzz'}
    response = client.post('/contact/', data)
    assert response.status_code != 302
    assert Contact.objects.exists() is False
