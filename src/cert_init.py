
import os
from backend_client import BackendClient

class CertificateInitiator(object):
    def __init__(self, config):
        self.bakend_client = BackendClient()
        self.config = config
        self.cert_content_dict = dict()

    def upload_file(self):
        cert_dict = self.config.get('chain').get('cert')
        assert cert_dict, "do not find any cert config from config.yml"
        for key, cert_path in cert_dict.items():
            assert os.path.isfile(cert_path) and os.path.exists(cert_path), f"{cert_path=} does not exist"
            file_key = self.bakend_client.upload_file(cert_path, host=self.config.get('backend', {}).get('host'))
            self.cert_content_dict[key] = file_key
    def import_init_certs(self):
        chian_config = self.config.get("chain")
        params = {
                "OrgId": chian_config.get("org_id"),
                "OrgName": chian_config.get("org_name"),
                "NodeName": chian_config.get("node_name"),
                "UserName": chian_config.get("user_name"),
                "CaCert": self.cert_content_dict["org_ca"],
                "SignCert": self.cert_content_dict["user_sign_cert"],
                "SignKey": self.cert_content_dict["user_sign_key"],
                "TlsCert": self.cert_content_dict["user_tls_cert"],
                "TlsKey": self.cert_content_dict["user_tls_key"],
        }
        res_json = self.bakend_client.import_start_cert(params)
        assert res_json.get("Status") == "OK", "import_init_certs failed"

    def dispatch(self):
        self.upload_file()
        self.import_init_certs()

