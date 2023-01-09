import logging
import datetime
import yaml
import uvicorn
from pathlib import Path
from optparse import OptionParser

import sqlalchemy
from core.database import BaseDatabase
from db.models import mapper_registry
from core.install import app_install
from playground_tools.playground_initialization import PlaygroundInitialization
from playground_tools.chain_initialization import ChainInitialization

_logger = logging.getLogger("app")
logging.info("Project core install start.")
app = app_install()
logging.info("Project core install completed.")


class Manager(object):
    def __init__(self):
        self.parser = OptionParser(usage="usage: % params [options] arg")
        self.default_date = datetime.date.today()
        self.params_dict = dict()
        self.config = yaml.safe_load(Path("./configs/config.yml").read_text())
        self.create_tables()

    @staticmethod
    def create_tables():
        print("create_tables")
        from core.database import engine
        mapper_registry.metadata.create_all(engine)
        metadata = sqlalchemy.MetaData(BaseDatabase)
        metadata.create_all(engine)

    def run_server(self):
        """
        :return:
        """
        _logger.info('begin run : %s' %
                     datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'))
        uvicorn.run(app="main:app", host="0.0.0.0", port=9088, log_level="info", reload=True, debug=False,
                    workers=2)
        _logger.info('end run : %s' %
                     datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'))

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

    def monitor(self):
        """
        1. 如果已经初始化区块链 需要拷贝 federated_db.cmb_chain_subscribe -> federated_service_db.cmb_chain_subscribe
        2. 初始化 federated_service_db.federated_node
        3. 生成机器码license 【】
        4. 提供接口验证机器码 【转调用service接口】
        5. 提供接口获取节点监控数据
        6. 提供接口获取节点各个服务的状态
        """
        try:
            print("start monitor platform...")
            from monitor.monitor import monitor
            monitor()
            print("success monitor platform ...")
        except AssertionError as e:
            print(f"init playground failed: {e}")
            exit(-1)


if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1 or sys.argv[1] in ("-h", "--help") or sys.argv[1] not in (
            'runserver', 'syncdb', 'init_chain', "init_playground", "monitor"):
        print("usage: main.py runserver for start a web server")
        print("usage: main.py syncdb for create database table")
        print("usage: main.py init_chain to start the chain connector !")
        print("usage: main.py init_playground try to start init the playground platform")
        print("usage: main.py monitor start the platform monitor")
        print("usage: main.py -h/--help given the help message")
        sys.exit(2)
    else:
        input_arg = sys.argv[1]
        if input_arg == "runserver":
            Manager().run_server()
        elif input_arg == "syncdb":
            Manager().create_tables()
        elif input_arg == "init_chain":
            Manager().init_chain_connector()
        elif input_arg == "init_playground":
            Manager().init_playground()
        elif input_arg == "monitor":
            Manager().monitor()
        else:
            print("unknown arg !")
            print("usage: main.py runserver for start a web server")
            print("usage: main.py syncdb for create database table")
            print("usage: main.py init_chain to start the chain connector !")
            print("usage: main.py init_playground try to start init the playground platform")
            print("usage: main.py monitor start the platform monitor")
            print("usage: main.py -h/--help given the help message")
            sys.exit(-1)
