import datetime
import sys
import yaml
from optparse import OptionParser
from pathlib import Path

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())

from chain_initialization import ChainInitialization
from playground_initialization import PlaygroundInitialization


class Manager(object):
    def __init__(self):
        self.parser = OptionParser(usage="usage: % params [options] arg")
        self.default_date = datetime.date.today()
        self.params_dict = dict()
        self.config = yaml.safe_load(Path("../configs/config.yml").read_text())

    def init_chain_connector(self):
        """
        1. 记录证书初始化的阶段
        2.
        """
        try:
            print("start init chain connector...")
            ChainInitialization(config=self.config).dispatch()
            print("success init chain connector ...")
        except AssertionError as e:
            print(f"init chain connector failed: {e}")
            exit(-1)

    def init_playground(self):
        """
        1. 如果已经初始化区块链 需要拷贝 federated_db.cmb_chain_subscribe -> federated_service_db.cmb_chain_subscribe
        2. 初始化 federated_service_db.federated_node
        3. 生成机器码license 【】
        4. 提供接口验证机器码 【转调用service接口】
        5. 提供接口获取节点监控数据
        6. 提供接口获取节点各个服务的状态 
        """
        try:
            print("start init playground...")
            PlaygroundInitialization(config=self.config).dispatch()
            print("success init playground ...")
        except AssertionError as e:
            print(f"init playground failed: {e}")
            exit(-1)


if __name__ == "__main__":

    input_arg = sys.argv[1]
    if input_arg in ("-h", "--help") or input_arg not in ('init_chain', "init_playground"):
        print("usage: main.py init_chain to start the chain connector !")
        print("usage: main.py init_playground try to start init the playground platform")
        print("usage: main.py -h/--help given the help ")
        sys.exit(2)
    else:
        if input_arg == "init_chain":
            Manager().init_chain_connector()
            print(f"init_chain successfully")
        elif input_arg == "init_playground":
            Manager().init_chain_connector()
            print(f"init_playground  successfully")
        else:
            print("unknown the input arg ")
            print("usage: main.py init_chain to start the chain connector !")
            print("usage: main.py init_playground try to start init the playground platform")
            print("usage: main.py -h/--help given the help ")
