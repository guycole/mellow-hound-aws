#! /usr/bin/python
#
# Title:reloader.py
# Description: sequentially pull S3 files, unpack and load (takes months)
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import os
import subprocess
import sys
import syslog
import time
import yaml

from sql_table import ApplicationLog
from sql_table import TaskLog

import boto

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class EodReloader:

    def log_writer(self, level, message, task_id, session):
        """
        logger
        """
        print message

        syslog.syslog(syslog.LOG_INFO, message)

        session.add(ApplicationLog(task_id, 'Reloader', level, message))
        session.commit()

    def s3key_to_name(self, s3key):
        temp = s3key.name.encode('ascii', 'ignore')
        tokens = temp.split('/')
        return tokens[len(tokens)-1]

    def s3read(self, s3key, task_id, session):
        log_message = "working file:%s" % s3key.name
        self.log_writer(6, log_message, task_id, session)

        file_name = self.s3key_to_name(s3key)

        s3key.get_contents_to_filename(file_name)

        command = "%s -xvzf %s" % (tar_command, file_name)
        print command
        os.system(command)

        return subprocess.check_output([find_command, '/mnt/raid/mythic_reload', '-name', 'ftp.eoddata.com']).strip('\n')

    def eod_load(self, s3key, directory):
        file_name = self.s3key_to_name(s3key)

        command = "%s -jar /home/gsc/github/mythic-crux-aws/mythic-eoddata/target/mythic-eoddata-jar-with-dependencies.jar loader %s %s" % (java_command, file_name, directory)
        print command
#        os.system(command)

    def execute(self):
        start_time = time.time()

        mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)
        engine = create_engine(mysql_url, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        task_log = TaskLog('Reloader')
        session.add(task_log)
        session.commit()

        os.chdir('/mnt/raid/mythic_reload')
        population = 0

        self.log_writer(6, 'start', task_log.id, session)

        s3 = boto.connect_s3()
        s3bucket = s3.get_bucket(s3_name)
        for s3key in s3bucket.list():
            ndx = s3key.name.find('eoddata')
            if ndx >= 0:
                print s3key.name
                ndx = s3key.name.find('tgz')
                if ndx > 0:
                    directory = self.s3read(s3key, task_log.id, session)
                    self.eod_load(s3key, directory)
                    population = population+1;

                    command = "%s -rf /mnt/raid/mythic_reload/*" % rm_command
                    print command
                    os.system(command)

        duration = time.time() - start_time
        log_message = "stop w/population %d and duration %d" % (population, duration)
        self.log_writer(6, log_message, task_log.id, session)

print 'reloader start'

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

    find_command = configuration['findCommand']
    java_command = configuration['javaCommand']
    rm_command = configuration['rmCommand']
    tar_command = configuration['tarCommand']

    s3_name = configuration['s3Name']
    sqs_name = configuration['sqsName']

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_hostname = configuration['mySqlHostName']
    mysql_database = configuration['mySqlDataBase']

    driver = EodReloader()
    driver.execute()

    syslog.closelog()

print 'reloader stop'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
