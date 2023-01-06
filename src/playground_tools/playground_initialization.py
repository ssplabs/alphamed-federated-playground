import hashlib
from hashlib import sha256
from playground_tools.chain_connector_client import ChainConnectorClient
from libs.other_utils import ExecShellUnix
from playground_tools.federated_client import FederatedClient


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
        self.machine_code = sha256(self.node_id.encode()).hexdigest().upper()
        with open("./configs/register_code.txt", "w") as f:
            f.write(self.machine_code)

    def init_federate_playground(self):
        ret = self.fed_client.node_init(
            {"chain_id": self.chain_config.get("chain_id"), "node_machine_code": self.machine_code,
             "node_ip": self.config.get("local_ip")})
        assert ret.get("ok") == "", "sync chain subscribe failed by request res str(ret)"

    def dispatch(self):
        res = ExecShellUnix("dmidecode -s  system-serial-number")
        if not res:
            print("please insert dmidecode by yum or apt")
            exit(-1)
        self.machine_code = res[0].strip()
        self.node_id = hashlib.md5(self.machine_code.encode()).hexdigest().upper()
        print("生成机器码。。。")
        self.save_machine_code()
        print("初始化系统。。。")
        self.init_federate_playground()
