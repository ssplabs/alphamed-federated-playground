import base64
import requests
import logging
import os

_logger = logging.getLogger()


class ChainConnectorClient(object):
    def __init__(self):
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.bass_host = "localhost"
        self.bass_port = 9070
        self.base_path = "/chain/connector?cmb="
        self.session = requests.Session()

    def login(self, host=None) -> bool:
        """Login to BASS system."""
        data = {
            'UserName': 'admin',
            'Password': 'dc483e80a7a0bd9ef71d8cf973673924',
            'Captcha': 'aes2'
        }
        if not host:
            host = self.bass_host
        base_url = f"http://{host}:{self.bass_port}{self.base_path}"
        url = f"{base_url}Login"

        try:
            resp = self.session.post(url=url, json=data, headers=self.headers)
            assert resp.status_code >= 200, f'requests : {url}={resp}'
            resp_json: dict = resp.json()
            _Response: dict = resp_json.get('Response')
            assert _Response and isinstance(
                _Response, dict), f'返回 Response 错误: {_Response}'
            _Data: dict = _Response.get('Data')
            token = _Data.get('Token')
            assert token and isinstance(token, str), f'invalid token: {_Data}'
            self.session.cookies.update(resp.cookies)
            self.headers['token'] = token
            self.headers['cookie'] = ';'.join(
                f'{name}={value}' for name, value in self.session.cookies.items())
        except AssertionError as e:
            return False
        else:
            return True

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

    def import_org_cert(self, params, host=None):
        """
        params:
            OrgId     string
            OrgName   string
            CaCert    string
            CaKey     string
            Algorithm int
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}InitOrgCaCert"
            resp_json, error = self.send_request(url, params)
            print(resp_json)
            _Response: dict = resp_json.get('Response')
            _Data: dict = _Response.get('Data')
            assert _Data, f'get_cert host={host} params={params} 返回 Data 错误: {_Data}'
            return _Data
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def import_user_cert(self, params, host=None):
        """
        params:
            OrgId     string
            OrgName   string
            NodeName  string
            UserName  string
            SignCert  string
            SignKey   string
            TlsCert   string
            TlsKey    string
            Algorithm int
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}InitUserCert"
            resp_json, error = self.send_request(url, params)
            print(resp_json)
            _Response: dict = resp_json.get('Response')
            _Data: dict = _Response.get('Data')
            assert _Data, f'get_cert host={host} params={params} 返回 Data 错误: {_Data}'
            return _Data
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def import_start_cert(self, params, host=None):
        """
        params:
            Role      int
            OrgId     string
            OrgName   string
            NodeName  string
            UserName  string
            CaCert    string
            SignCert  string
            SignKey   string
            TlsCert   string
            TlsKey    string
            Algorithm int
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}ImportStartCert"
            resp_json, error = self.send_request(url, params)
            print(resp_json)
            _Response: dict = resp_json.get('Response')
            _Data: dict = _Response.get('Data')
            assert _Data, f'get_cert host={host} params={params} 返回 Data 错误: {_Data}'
            return _Data
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def get_org_list(self, params, host=None):
        """
        params:
            'ChainId': 'sspchain1'

        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}GetOrgListByChainId"
            resp_json, error = self.send_request(url, params)
            print(resp_json)
            _Response: dict = resp_json.get('Response')
            return _Response["GroupList"]
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def get_org_ca_list(self, params, host=None):
        """
        params:
            {
                "CertType": 1,
                "OrgId": ""
            }
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}GetOrgCertList"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            return _Response["GroupList"]
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def get_cert_list(self, params, host=None):
        """
        params:
            {
                "Type": 1,
                "NodeName": "",
                "PageNum": 0,
                "PageSize": 10,
                "ChainMode": "permissionedWithCert"
            }
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}GetCertList"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            return _Response["GroupList"]
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def get_node_list(self, params, host=None):
        """
        params:
            {
                ChainId  string
                NodeName string
                PageNum  int
                PageSize int
            }
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}GetNodeList"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            return _Response["GroupList"]
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def get_chain_org_node_list(self, params, host=None):
        """
        params:
            {
                ChainId  string
            }
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}GetChainOrgNodeList"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            return _Response["GroupList"]
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def get_cert(self, params, host=None):
        """
        params:
            {
                "CertId": 47,
                "CertUse": 2
            }
        """

        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}GetCert"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            _Data: dict = _Response.get('Data')
            assert _Data, f'get_cert host={host} params={params} 返回 Data 错误: {_Data}'
            return _Data
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def subscribe_chain(self, params: dict, host=None):
        """
            params: {
            "ChainId": "sspchain1",
            "OrgId": "wx-org4.chainmaker.org",
            "NodeId": "QmRj3kV7uQeCndrJvYYFHwfDoQmFdxNkCqpiL7m7VanKfw",
            "UserName": "sspchain1org4node1admin1",
            "NodeRpcAddress": "159.75.210.122:12301",
            "Tls": 0,
            "TLSHostName": "chainmaker.org"
            }

        """
        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}SubscribeChain"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            _Data: dict = _Response.get('Data')
            assert _Data, f'get_cert host={host} params={params} 返回 Data 错误: {_Data}'
            return _Data
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def subscribe_contract(self, params: dict, host=None):
        """
            params: {
                "ChainId": "sspchain1",
                "ContractName": "task",
                "ContractVersion": "2.0"
            }
        """
        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}SubscribeChainContract"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            _Data: dict = _Response.get('Data')
            assert _Data, f'get_cert host={host} params={params} 返回 Data 错误: {_Data}'
            return _Data
        except AssertionError as e:
            _logger.exception(e)
            return {}

    def get_full_chain_subscribe(self, params: dict, host=None):
        """
            params: {
            "ChainId": "string",
            "Algorithm": 0 // 0 sm2 1 ecdsa
            }
        """
        if not host:
            host = self.bass_host
            self.login()
        else:
            self.login(host=host)

        try:
            url = f"http://{host}:{self.bass_port}{self.base_path}GetFullSubscribeConfig"
            resp_json, error = self.send_request(url, params)
            _Response: dict = resp_json.get('Response')
            _Data: dict = _Response.get('Data')
            assert _Data, f'get full chain subscribe host={host} params={params} 返回 Data 错误: {_Data}'
            return _Data
        except AssertionError as e:
            _logger.exception(e)
            return {}

    @staticmethod
    def get_filename_from_header(resp_header):
        content_disposition = resp_header.get("Content-Disposition")
        for item in content_disposition.split(";"):
            if "filename" in item:
                return base64.b64decode(item.split("filename=")[1]).decode()
        return ""

    @classmethod
    def download_file(cls, params, host=None):
        """
        params:
            "FileKey": "3.1.3a1dcc6dc2487a189ccfdb44881010eba421075fa4be0e6520f433277a95df1b"
        """
        if not host:
            host = cls.bass_host
        base_url = f"http://{host}:{cls.bass_port}{cls.base_path}"
        url = f"{base_url}DownloadFile"
        resp = requests.post(url=url, json=params,
                             headers=cls.headers, stream=True)
        assert resp.status_code >= 200, f'requests : {url}={resp}'
        assert resp.headers.get(
            "Content-Type") == "application/octet-stream", "文件下载失败"
        file_name = cls.get_filename_from_header(resp.headers)
        return {
            "file_name": file_name,
            "rw_content": resp.content,
            "file_key": params["FileKey"],
            "file_hash": params["FileKey"].split(".")[-1]
        }

    def upload_file(self, file_path, host=None):
        self.login(host=host)

        assert file_path, 'nothing to upload'
        assert (
                isinstance(file_path, str)
                and os.path.exists(file_path)
                and os.path.isfile(file_path)
        ), f'{file_path} does not exist or is not a file'
        file_name = os.path.split(file_path)[-1]
        if not host:
            host = self.bass_host
        url = f"http://{host}:{self.bass_port}{self.base_path}UploadFile"
        headers = self.headers.copy()
        headers.pop('content-type')
        files = {'File': (file_name, open(file_path, 'rb'))}
        resp = self.session.post(url, headers=headers, files=files)
        resp_json: dict = resp.json()
        _Response: dict = resp_json.get('Response')
        assert _Response and isinstance(
            _Response, dict), f'返回 Response 错误: {_Response}'
        _Data: dict = _Response.get('Data')
        file_key = _Data.get('FileKey')
        assert file_key and isinstance(
            file_key, str), f'invalid file key: {file_key}'
        return file_key
