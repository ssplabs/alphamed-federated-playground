import hashlib
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
        self.node_id = None

    def save_machine_code(self):
        with open("./configs/register_code.txt", "w") as f:
            f.write(self.machine_code)

    def gather_system_info(self):
        from .system_info import SystemInfo
        return SystemInfo().dispatch()

    def init_federate_playground(self):
        ret = self.fed_client.node_init(
            {"chain_id": self.chain_config.get("chain_id"), "node_machine_code": self.machine_code,
             "node_ip": self.config.get("local_ip")})
        assert ret.get("ok") == "", "sync chain subscribe failed by request res str(ret)"

    def dispatch(self):
        self.gather_system_info()
        res = ExecShellUnix("dmidecode -s  system-serial-number")
        if not res:
            print("please insert dmidecode by yum or apt")
            exit(-1)
        self.machine_code = res[0].strip()

        node_config = {
            "network_status": NodeNetworkStatus.Disable,
            "cpu": "",
            "gpu": "",
            "memory": "",
            "disk": "",
            "registry_date": None,
            "machine_code": self.machine_code,
            "license_code": "",
            "license_status": NodeLicenseStatus.Disable,
        }
        if self.config.get("local_chain") == True:
            self.node_id = self.chain_config.get("node_id")
            node_config.update({
                "node_id": self.node_id,
                "node_ip": self.chain_config.get("node_host"),
                "org_name": self.chain_config.get("org_name"),
                "org_id": self.chain_config.get("org_id")
            })
        else:
            self.node_id = hashlib.md5(self.machine_code.encode()).hexdigest().upper()
            node_config.update({
                "node_id": self.node_id,
                "node_ip": self.config.get("fed_node").get("node_host"),
                "org_name": self.config.get("fed_node").get("org_name"),
                "org_id": self.config.get("fed_node").get("org_id")
            })

        self.machine_code = sha256(self.node_id.encode()).hexdigest().upper()
        print("生成机器码。。。")
        self.save_machine_code()
        print("初始化系统。。。")
        self.init_federate_playground()
