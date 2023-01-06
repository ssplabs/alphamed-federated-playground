import hashlib
from hashlib import sha256
from playground_tools.client import BackendClient
from libs.other_utils import ExecShellUnix


class PlaygroundInitialization(object):

    def __init__(self, config):
        self.backend_client = BackendClient()
        self.config = config
        self.cert_content_dict = dict()
        self.chain_config = self.config.get('chain')
        self.machine_code = None
        self.node_id = None

    def save_machine_code(self):
        self.machine_code = sha256(self.node_id.encode()).hexdigest()
        with open("./configs/register_code.txt", "w") as f:
            f.write(self.machine_code)

    # def sync_chain_subscribe(self):
    #     pass

    def dispatch(self):
        res = ExecShellUnix("dmidecode -s  system-serial-number")
        if not res:
            print("please insert dmidecode by yum or apt")
            exit(-1)
        self.node_id = hashlib.md5(res[0].strip().encode()).hexdigest()
        self.save_machine_code()
