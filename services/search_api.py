import json
import logging
import requests

from requests.exceptions import (
    HTTPError,
    ConnectionError
)

from flask import abort
from introductions import app

SEARCH_API = app.config['SEARCH_API']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

def get_or_log_error(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        app.logger.error("HTTP Error %s", e)
        abort(response.status_code)
    except requests.exceptions.ConnectionError as e:
        app.logger.error("Error %s", e)
        abort(500)


def get_property_by_title_number(title_number):
    title_url = "%s/%s/%s" % (SEARCH_API, 'titles', title_number)
    logger.info("Requesting title url : %s" % title_url)

    response = get_or_log_error(title_url)
    response_json = response.json()
    logger.info("Found the following title: %s" % json)
    return response_json