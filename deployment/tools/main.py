import datetime
import yaml
from pathlib import Path
from optparse import OptionParser
from cert import CertificateInitiator
from subscribe import Subscribe


class Manager(object):
    def __init__(self):
        self.parser = OptionParser(usage="usage: % params [options] arg")
        self.default_date = datetime.date.today()
        self.params_dict = dict()
        self.config =  yaml.safe_load(Path("../config/config.yml").read_text())

    def init_cert(self):
        """
        :return:
        """
        CertificateInitiator(config=self.config).dispatch()

    def subscribe(self):
        """
        :return:
        """
        Subscribe(config=self.config).dispatch()

    def subscribe_contract(self):
        """
        :return:
        """
        Subscribe(config=self.config).dispatch_contract()

        


if __name__ == "__main__":
    import sys

    input_arg = sys.argv[1]
    if input_arg in ("-h", "--help") or input_arg not in ('init_cert', "subscribe_chain", "subscribe_contract"):
        print("usage: main.py init_cert init the chain user and org cert")
        print("usage: main.py subscribe_chain subscribe a chain node")
        print("usage: main.py subscribe_contract subscribe chain contract invoke")
        print("usage: main.py -h/--help given the help ")
        sys.exit(2)
    else:
        if input_arg == "init_cert":
            flag = Manager().init_cert()
            print(f"init_cert {flag}")
        elif input_arg == "subscribe_chain":
            flag = Manager().subscribe()
            print(f"subscribe chain {flag}")
        else:
            flag = Manager().subscribe_contract()
            print(f"subscribe contract {flag}")
