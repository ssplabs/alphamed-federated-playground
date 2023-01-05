import datetime
import sys
import yaml
from optparse import OptionParser
from pathlib import Path

sys.path.append(Path(__file__).resolve().parent.parent.as_posix())

from cert import CertificateInitiator
from subscribe import Subscribe


class Manager(object):
    def __init__(self):
        self.parser = OptionParser(usage="usage: % params [options] arg")
        self.default_date = datetime.date.today()
        self.params_dict = dict()
        self.config = yaml.safe_load(Path("../configs/config.yml").read_text())

    def init_chain_connector(self):
        """
        :return:
        """
        print("start init cert...")
        CertificateInitiator(config=self.config).dispatch()
        print("start init subscribe node ...")
        Subscribe(config=self.config).dispatch()
        print("start init subscribe contact ...")
        Subscribe(config=self.config).dispatch_contract()


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
