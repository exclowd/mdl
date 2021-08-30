import json

import numpy as np
import requests

API_ENDPOINT = 'http://10.4.21.156'
MAX_DEG = 11
SECRET_KEY = 'KbWaA65AkqYq1F73dsUTAQQTCqLTVqYcxYkk7CgzfvHuB0NAFv'


def get_overfit_vector():
    return json.loads(send_request(SECRET_KEY, [0], 'getoverfit'))


def urljoin(root, path=''):
    if path: root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root


def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id': id, 'vector': vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response


def get_errors(key, vector):
    for i in vector:
        assert 0 <= abs(i) <= 10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(key, vector, 'geterrors'))


# Replace 'SECRET_KEY' with your team's secret key (Will be sent over email)
def do_request(vector):
    errors = get_errors(SECRET_KEY, list(vector))
    return np.array(errors, dtype=np.longdouble)


def submit(vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector:
        assert 0 <= abs(i) <= 10
    assert len(vector) == MAX_DEG
    return send_request(SECRET_KEY, list(vector), 'submit')


def refresh():
    get_overfit_vector()
