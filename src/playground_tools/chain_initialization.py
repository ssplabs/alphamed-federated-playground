import os
import hashlib
from playground_tools.client import BackendClient
from db import db_initalization
from libs.other_utils import ExecShellUnix


class ChainInitialization(object):

    def __init__(self, config):
        self.backend_client = BackendClient()
        self.config = config
        self.cert_content_dict = dict()
        self.chain_config = self.config.get('chain')
        self.machine = None
        self.node_id = None

    def upload_file(self):

        cert_dict = self.config.get('chain').get('cert')
        assert cert_dict, "do not find any cert configs from configs.yml"
        for key, cert_path in cert_dict.items():
            assert os.path.isfile(cert_path) and os.path.exists(cert_path), f"{cert_path} does not exist"
            file_key = self.backend_client.upload_file(cert_path, host=self.config.get('backend', {}).get('host'))
            self.cert_content_dict[key] = file_key

    def import_init_certs(self):
        chain_config = self.config.get("chain")
        params = {
            "OrgId": chain_config.get("org_id"),
            "OrgName": chain_config.get("org_name"),
            "NodeName": chain_config.get("node_name"),
            "UserName": chain_config.get("user_name"),
            "CaCert": self.cert_content_dict["org_ca"],
            "SignCert": self.cert_content_dict["user_sign_cert"],
            "SignKey": self.cert_content_dict["user_sign_key"],
            "TlsCert": self.cert_content_dict["user_tls_cert"],
            "TlsKey": self.cert_content_dict["user_tls_key"],
        }
        org_params = {
            "OrgId": chain_config.get("org_id"),
            "OrgName": chain_config.get("org_name"),
            "CaCert": self.cert_content_dict["org_ca"],
            "Algorithm": 1
        }
        res_json = self.backend_client.import_org_cert(org_params)
        assert res_json.get("Status") == "OK", "import_init_certs failed"
        user_params = {
            "OrgId": chain_config.get("org_id"),
            "OrgName": chain_config.get("org_name"),
            "NodeName": chain_config.get("node_name"),
            "UserName": chain_config.get("user_name"),
            "SignCert": self.cert_content_dict["user_sign_cert"],
            "SignKey": self.cert_content_dict["user_sign_key"],
            "TlsCert": self.cert_content_dict["user_tls_cert"],
            "TlsKey": self.cert_content_dict["user_tls_key"],
            "Algorithm": 1
        }
        res_json = self.backend_client.import_user_cert(user_params)
        assert res_json.get("Status") == "OK", "import_init_certs failed"

    def subscribe_chain(self):
        params = {
            "ChainId": self.chain_config.get('chain_id'),
            "OrgId": self.chain_config.get('org_id'),
            "NodeId": self.chain_config.get('node_id'),
            "UserName": self.chain_config.get('user_name'),
            "NodeRpcAddress": "{0}:{1}".format(self.chain_config.get('node_host'),
                                               self.chain_config.get('node_rpc_port')),
            "Tls": 0 if self.chain_config.get('tls') else 1,
            "TLSHostName": self.chain_config.get('tls_host_name')
        }
        try:
            res = self.backend_client.subscribe_chain(params)
            assert res.get('Status') == "OK", f"subscribe_chain params={params} failed res={res}"
            print("successfully subscribe chain ")
            return True
        except Exception as e:
            print(f"subscribe_chain failed {e}")
            return False

    def subscribe_contract(self, params: dict):
        res = self.backend_client.subscribe_contract(params)
        assert res.get('Status') == "OK", f"subscribe_contract params={params} failed res={res}"
        print(f"successfully subscribe chain {params}")

    def init_cert(self):
        try:
            check_step = db_initalization.check_init_step()
            if not check_step.init_result:
                self.upload_file()
                self.import_init_certs()
                db_initalization.update_step(self.node_id, "chain_connector_init_cert", True, "")
                return True
        except Exception as e:
            print(str(e))
            db_initalization.update_step(self.node_id, "chain_connector_init_cert", False, e.__repr__())
            return False

    def subscribe_chain_contract(self):
        try:
            for contract in self.chain_config.get('contract'):
                self.subscribe_contract(
                    {"ChainId": self.chain_config.get('chain_id'), "ContractName": contract.get('name'),
                     "ContractVersion": contract.get('version')})
                self.subscribe_contract(
                    {"ChainId": self.chain_config.get('chain_id'), "ContractName": contract.get('name'),
                     "ContractVersion": contract.get('version')})
        except AssertionError as e:
            print(e)
            return False
        else:
            return True

    def dispatch(self):
        res = ExecShellUnix("dmidecode -s  system-serial-number")
        if not res:
            print("please insert dmidecode by yum or apt")
            exit(-1)
        self.node_id = hashlib.md5(res[0].strip().encode()).hexdigest()
        init_cert_ret = self.init_cert()
        assert init_cert_ret, "init cert failed"
        subscribe_chain_ret = self.subscribe_chain()
        assert subscribe_chain_ret, "subscribe chain failed"
        chain_contract_ret = self.subscribe_chain_contract()
        assert chain_contract_ret, "subscribe chain contract failed"
