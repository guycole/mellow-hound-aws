#! /usr/bin/python
#
# Title:loader.py
# Description:poll directory for fresh file and process file when available
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import json
import os
import sys
import syslog
import time
import yaml

from loader_v1 import LoaderVersion1

from sql_table import ApplicationLog
from sql_table import LoadLog
from sql_table import TaskLog

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class FileLoader:

    def log_writer(self, level, message, task_id, session):
        """
        logger
        """
        print message

        syslog.syslog(syslog.LOG_INFO, message)

        session.add(ApplicationLog(task_id, 'Loader', level, message))
        session.commit()

    def file_handler(self, candidate, task_id, session):
        infile = open(candidate, 'r')
        raw_buffer = infile.readlines()
        infile.close()

        for raw_line in raw_buffer:
            print raw_line
            parsed_json = json.loads(raw_line)
#            print parsed_json
#            print parsed_json['networkName']

            try:
                version = parsed_json['version']
            except:
                version = 'missing_version'

            if version == 'missing_version':
                log_message = "missing version:%s" % candidate
                self.log_writer(6, log_message, task_id, session)
            elif version == 1:
                loader_v1 = LoaderVersion1()
                retval = loader_v1.execute(parsed_json, task_id, session)

                load_log = LoadLog(task_id, retval[0], 1, candidate)
                load_log.ble_pop = retval[1]
                load_log.wifi_pop = retval[2]
                load_log.cell_cdma_pop = retval[3]
                load_log.cell_gsm_pop = retval[4]
                load_log.cell_lte_pop = retval[5]
                load_log.cell_wcdma_pop = retval[6]

                session.add(load_log)
                session.commit()

                return True
        else:
                log_message = "bad version:%d:%s" % (version, candidate)
                self.log_writer(6, log_message, task_id, session)

        return False

    def execute(self):
        start_time = time.time()

        mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)
        engine = create_engine(mysql_url, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        task_log = TaskLog('Loader')
        session.add(task_log)
        session.commit()

        self.log_writer(6, 'start', task_log.id, session)

        success = 0
        failure = 0

        os.chdir(import_dir)
        targets = os.listdir('.')
        for target in targets:
            print "target:%s" % target
#            self.file_handler(target, task_log.id, session)
            try:
                if self.file_handler(target, task_log.id, session):
                    success =+ 1
                else:
                    failure =+ 1
            except:
                log_message = "failure:%s" % target
                self.log_writer(6, log_message, task_id, session, False)
                failure =+ 1

            os.unlink(target)

        duration = time.time() - start_time
        log_message = "stop w/population %d and duration %d" % (len(targets), duration)
        self.log_writer(6, log_message, task_log.id, session)

print 'loader start'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL3)

    if len(sys.argv) > 1:
        yaml_filename = sys.argv[1]
    else:
        yaml_filename = 'config.dev'

    configuration = yaml.load(file(yaml_filename))

    import_dir = configuration['importDir']

    s3_name = configuration['s3Name']
    sqs_name = configuration['sqsName']

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_hostname = configuration['mySqlHostName']
    mysql_database = configuration['mySqlDataBase']

    driver = FileLoader()
    driver.execute()

    syslog.closelog()

print 'loader stop'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
