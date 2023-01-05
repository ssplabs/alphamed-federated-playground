import logging
import datetime
from optparse import OptionParser

import sqlalchemy
from core.database import BaseDatabase
from db.models import mapper_registry
from core.install import app_install

_logger = logging.getLogger("app")
logging.info("Project core install start.")
app = app_install()
logging.info("Project core install completed.")


class Manager(object):
    def __init__(self):
        self.parser = OptionParser(usage="usage: % params [options] arg")
        self.default_date = datetime.date.today()
        self.params_dict = dict()

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
        import uvicorn
        _logger.info('begin run : %s' %
                     datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'))
        uvicorn.run(app="main:app", host="0.0.0.0", port=9088, log_level="info", reload=True, debug=False,
                    workers=2)
        _logger.info('end run : %s' %
                     datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'))


if __name__ == "__main__":
    import sys
    input_arg = sys.argv[1]
    if input_arg in ("-h", "--help") or input_arg not in (
            'runserver', 'syncdb'):
        print("usage: main.py runserver for start a web server")
        print("usage: main.py syncdb for create database table")
        print("usage: main.py -h/--help given the help message")
        sys.exit(2)
    else:
        if input_arg == "runserver":
            Manager().run_server()
        elif input_arg == "syncdb":
            Manager().create_tables()
        else:
            print("unknown arg !")
            sys.exit(-1)
