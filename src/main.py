import datetime
import yaml
from pathlib import Path
from optparse import OptionParser
from cert_init import CertificateInitiator


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

    def chain_sub(self):
        """
        :return:
        """
        pass
    
    def contract_sub(self):
        pass


if __name__ == "__main__":
    import sys

    input_arg = sys.argv[1]
    if input_arg in ("-h", "--help") or input_arg not in ('init_cert', 'chain_sub', "contract_sub"):
        print("usage: main.py init_cert init the chain user and org cert")
        print("usage: main.py chain_sub subscribe a chain node ")
        print("usage: main.py contract_sub subscribe a contract involke")
        print("usage: main.py -h/--help given the help ")
        sys.exit(2)
    else:
        if input_arg == "init_cert":
            Manager().init_cert()
        elif input_arg == "chain_sub":
            Manager().chain_sub()
        else:
            Manager().contract_sub()
