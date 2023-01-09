import hashlib
import json
from hashlib import sha256
from playground_tools.chain_connector_client import ChainConnectorClient
from libs.other_utils import ExecShellUnix
from playground_tools.federated_client import FederatedClient
from db.models import NodeNetworkStatus, NodeLicenseStatus


class PlaygroundInitialization(object):

    def __init__(self, config):
        self.backend_client = ChainConnectorClient()
        self.fed_client = FederatedClient()
        self.config = config
        self.cert_content_dict = dict()
        self.chain_config = self.config.get('chain')
        self.machine_code = None
        self.license_code = None
        self.node_id = None

    def save_machine_code(self):
        with open("../configs/register_code.txt", "w") as f:
            f.write(self.license_code)

    def gather_system_info(self):
        from .system_info import SystemInfo
        return SystemInfo().dispatch()

    def init_federate_playground(self, params: dict):
        """
            {
                "machine_code": "FVFDN0SCP3XY",
                "chain_id": "alphamed_federated_network",
                "disk": "181GB/233GB",
                "cpu": "4核8线程",
                "memory": "8.0GB",
                "gpu": "",
                "node_id": "QmYX5KatFyFve3xVjadX2h7fEt1SzpdA8wnQsQ4v9muCyR",
                "node_ip": "172.16.0.2",
                "org_name": "alphamedSSPLabs",
                "org_id": "alphamed-ssplabs"
            }
        """
        ret = self.fed_client.node_init(params)
        assert ret.get("code") == 0, "sync chain subscribe failed by request res str(ret)"

    def dispatch(self):
        system_info = self.gather_system_info()
        res = ExecShellUnix("dmidecode -s  system-serial-number")
        if not res:
            print("please insert dmidecode by yum or apt")
            exit(-1)
        self.machine_code = res[0].strip()

        node_config = {
            "node_machine_code": self.machine_code,
            "chain_id": self.chain_config.get("chain_id"),
        }
        node_config.update(system_info)
        if self.config.get("local_chain") == True:
            self.node_id = self.chain_config.get("node_id")
            node_config.update({
                "node_id": self.node_id,
                "node_name": self.chain_config.get("node_name"),
                "node_ip": self.chain_config.get("node_host"),
                "org_name": self.chain_config.get("org_name"),
                "org_id": self.chain_config.get("org_id")
            })
        else:
            self.node_id = hashlib.md5(self.machine_code.encode()).hexdigest().upper()
            node_config.update({
                "node_id": self.node_id,
                "node_name": self.config.get("fed_node").get("node_name"),
                "node_ip": self.config.get("fed_node").get("node_host"),
                "org_name": self.config.get("fed_node").get("org_name"),
                "org_id": self.config.get("fed_node").get("org_id")
            })
        self.license_code = sha256(self.machine_code.encode()).hexdigest().upper()
        print("生成机器码。。。")
        self.save_machine_code()
        print("初始化系统。。。")
        self.init_federate_playground(node_config)
