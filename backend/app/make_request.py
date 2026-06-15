import json
from urllib import request
from urllib.parse import urljoin


BASE_URL = 'http://auth:7000'

def get_public_key():
    url = urljoin(BASE_URL, 'v1/auth/public-key')
    req = request.Request(url, method='GET')

    with request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        return json.loads(result)


def make_post_request(payload):
    url = urljoin(BASE_URL, 'v1/auth/login')

    req = request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')

    with request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        return json.loads(result)


def make_register_request(payload):
    url = urljoin(BASE_URL, 'v1/auth/register')

    req = request.Request(url, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')

    with request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        return json.loads(result)