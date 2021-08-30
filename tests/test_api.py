import time

import pytest
import redis
from django.conf import settings
from django.urls import reverse
from freezegun import freeze_time

pytestmark = pytest.mark.django_db
VISITED_LINKS_ENDPOINT = reverse('visited-links')
VISITED_DOMAINS_ENDPOINT = reverse('visited-domains')
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=1)

LINKS = [
    ['https://realpython.com/'],
    ['https://stackoverflow.com/questions/11828270/how-do-i-exit-the-vim-editor'],
    [
        'funbox.ru',
        'https://www.geeksforgeeks.org/',
        'https://github.com/',
        'http://127.0.0.1:8000/',
        'https://ya.ru',
        'https://ya.ru?q=123',
    ]
]

INVALID_LINK_TYPES = [
    1,
    'test',
    {'foo': 'bar'},
    [1, 2, 3, 4],
    []
]


def test_redis_server_is_available():
    assert redis_instance.ping()


def test_visited_domains_endpoint_available(client):
    response = client.get(VISITED_DOMAINS_ENDPOINT)
    assert response.status_code == 200


@pytest.mark.parametrize('link', LINKS)
def test_post_valid_visited_links(client, link):
    redis_instance.flushdb()
    redis_instance.flushall()

    data = {'links': link}
    response = client.post(VISITED_LINKS_ENDPOINT, data, content_type='application/json')

    assert response.status_code == 201

    redis_instance.flushdb()
    redis_instance.flushall()


@pytest.mark.parametrize('invalid_link', INVALID_LINK_TYPES)
def test_post_invalid_visited_links(client, invalid_link):
    redis_instance.flushdb()
    redis_instance.flushall()

    data = {'links': invalid_link}
    response = client.post(VISITED_LINKS_ENDPOINT, data, content_type='application/json')

    assert response.status_code == 400

    redis_instance.flushdb()
    redis_instance.flushall()


def test_domains_are_valid(client):
    redis_instance.flushdb()
    redis_instance.flushall()

    data = {'links': [
        'https://pypi.org/project/fakeredis/',
        'https://www.youtube.com/',
        'https://stackabuse.com/',
    ]
    }
    client.post(VISITED_LINKS_ENDPOINT, data, content_type='application/json')
    response = client.get(VISITED_DOMAINS_ENDPOINT)

    assert 'pypi.org' in response.json()['domains']
    assert 'www.youtube.com' in response.json()['domains']
    assert 'stackabuse.com' in response.json()['domains']

    redis_instance.flushdb()
    redis_instance.flushall()


@freeze_time('2021-08-29 18:00:01', auto_tick_seconds=60)
def test_timestamps_return_valid_domains(client):
    redis_instance.flushdb()
    redis_instance.flushall()

    first_time = time.time()
    data = {'links': [
        'funbox.ru',
        'https://pypi.org/project/fakeredis/',
        'https://www.youtube.com/',
        'https://stackabuse.com/',
    ]}
    client.post(VISITED_LINKS_ENDPOINT, data, content_type='application/json')

    auto_incremented_time = time.time()
    new_data = {'links': ['https://github.com/']}
    client.post(VISITED_LINKS_ENDPOINT, new_data, content_type='application/json')

    response = client.get(f'{VISITED_DOMAINS_ENDPOINT}?from={first_time}&to={auto_incremented_time}')

    assert 'pypi.org' in response.json()['domains']
    assert 'www.youtube.com' in response.json()['domains']
    assert 'stackabuse.com' in response.json()['domains']
    assert 'funbox.ru' in response.json()['domains']

    assert 'github.com' not in response.json()['domains']

    redis_instance.flushdb()
    redis_instance.flushall()
