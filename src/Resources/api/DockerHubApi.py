import logging

import requests

from ..exceptions import HTTPConnectionError

DOCKER_HUB_IMAGE_URL = "https://hub.docker.com/v2/repositories/%s/tags/latest/"
DOCKER_HUB_KATHARA_URL = "https://hub.docker.com/v2/repositories/kathara/?page_size=-1"


class DockerHubApi(object):
    @staticmethod
    def get_image_information(image_name):
        try:
            result = requests.get(DOCKER_HUB_IMAGE_URL % image_name)
        except requests.exceptions.ConnectionError as e:
            raise HTTPConnectionError(str(e))

        if result.status_code != 200:
            logging.debug("DockerHub replied with status code %s while looking for image %s.",
                          result.status_code,
                          image_name
                          )
            raise HTTPConnectionError("DockerHub replied with status code %s." % result.status_code)

        return result.json()

    @staticmethod
    def get_images():
        try:
            result = requests.get(DOCKER_HUB_KATHARA_URL)
        except requests.exceptions.ConnectionError as e:
            raise HTTPConnectionError(str(e))

        if result.status_code != 200:
            logging.debug("DockerHub replied with status code %s.", result.status_code)
            raise HTTPConnectionError("DockerHub replied with status code %s." % result.status_code)

        return filter(lambda x: not x['is_private'], result.json()['results'])