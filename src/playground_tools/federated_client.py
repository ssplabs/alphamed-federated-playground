import base64
import requests
import logging
import os

_logger = logging.getLogger()


class FederatedClient(object):
    def __init__(self):
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.bass_host = "localhost"
        self.bass_port = 9080
        self.base_path = "/fed-service/api/"
        self.session = requests.Session()

    def send_request(self, url, params):
        try:
            resp = self.session.post(
                url=url, json=params, headers=self.headers)
            assert resp.status_code >= 200, f'requests : {url}={resp}'
            resp_json: dict = resp.json()
            assert resp_json and isinstance(
                resp_json, dict), f'requests response: {resp.text}'
            return resp_json, ""
        except AssertionError as e:
            _logger.exception(e)
            return {}, str(e)
        except requests.exceptions.RequestException as e:
            _logger.exception(e)
            return {}, ""
        except Exception as e:
            raise e

    def node_init(self, params, host=None):
        """
        params:
            chain_id     string
            node_machine_code     string
        """
        if not host:
            host = self.bass_host
        url_path = "/fed-service/api/v2/node/init"
        try:
            url = f"http://{host}:{self.bass_port}{url_path}"
            resp_json, error = self.send_request(url, params)
            print(resp_json)
            return resp_json
        except AssertionError as e:
            _logger.exception(e)
            return {}
