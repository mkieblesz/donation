import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.fixture
def user(db):
    yield User.objects.create(username='user1')


def test_homepage_success(db, client):
    assert client.get(reverse('homepage')).status_code == 200


def test_homepage_content_no_pledges(db, client):
    assert client.get(reverse('homepage')).content.decode('utf-8') == """Homepage

number of pledges: 0
Impact 1: 0 of CO2 less in the athmosphere
Impact 2: 0 less water used
Impact 3: 0 less waste
"""


def test_user_pledges_success(user, client):
    assert (
        client.get(reverse('user_pledges', kwargs={'username': user.username})).status_code == 200
    )


def test_user_pledges_no_pledges_made(user, client):
    response = client.get(reverse('user_pledges', kwargs={'username': user.username}))

    assert response.content.decode('utf-8') == """User pledges

user1 user has made following pledges: """
