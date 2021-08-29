import time
from urllib.parse import urlparse

import redis
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Assume persistence
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


# Assume if submitted link exists - only update its timestamp

@api_view(['POST'])
def visited_links(request, *args, **kwargs) -> Response:
    data = request.data.get('links')
    if not data or not isinstance(data, list):
        return Response(
            {'status': 'Error',
             'message': 'Links array missing or incorrect data type'
             },
            status=status.HTTP_400_BAD_REQUEST,
        )

    links = dict()
    domains = dict()
    timestamp = round(time.time())

    for link in data:
        if not isinstance(link, str):
            return Response(
                {'status': 'Error',
                 'message': 'Link instances must be strings',
                 },
                status=status.HTTP_400_BAD_REQUEST
            )

        domain = urlparse(link).netloc
        if domain == '':
            domain = link
        links[link] = timestamp
        domains[domain] = timestamp
    with redis_instance.pipeline() as pipe:
        pipe.multi()
        pipe.zadd('visited_links', {**links})
        pipe.zadd('domains', {**domains})
        pipe.execute()
    response = {
        'status': 'Ok'
    }
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def visited_domains(request, *args, **kwargs) -> Response:
    from_timestamp = request.query_params.get('from')
    to_timestamp = request.query_params.get('to')

    if from_timestamp is None or to_timestamp is None:
        key = redis_instance.zrange('domains', 0, -1)
        response = {
            'status': 'Ok',
            'domains': key
        }
        return Response(response, status=status.HTTP_200_OK)

    try:
        from_timestamp = float(from_timestamp)
        to_timestamp = float(to_timestamp)
    except ValueError:
        return Response({
            'status': 'Error',
            'message': 'Invalid type for timestamps',
        },
            status=status.HTTP_400_BAD_REQUEST
        )

    keys = redis_instance.zrangebyscore(
        'domains',
        from_timestamp,
        to_timestamp
    )
    response = {'status': 'Ok', 'domains': keys}
    return Response(response, status=status.HTTP_200_OK)
