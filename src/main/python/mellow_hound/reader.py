#! /usr/bin/python
#
# Title:reader.py
# Description:poll SQS for fresh file alerts and process file when available
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import json
import os
import sys
import syslog
import time
import yaml

from sql_table import ApplicationLog
from sql_table import TaskLog

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from boto.s3.connection import S3Connection
from boto.sqs.connection import SQSConnection

class SqsReader:

    def log_writer(self, level, message, task_id, session):
        """
        logger
        """
        print message

        syslog.syslog(syslog.LOG_INFO, message)

        session.add(ApplicationLog(task_id, 'Reader', level, message))
        session.commit()

    def s3read(self, s3filename, s3bucket, task_id, session):
        print s3filename
        os.chdir(import_dir)

        temp = s3filename.split('/')
        fresh_filename = temp[len(temp)-1]

        try:
            s3key = s3bucket.get_key(s3filename)
            s3key.get_contents_to_filename(fresh_filename)
            log_message = "S3 read success %s" % s3filename
            self.log_writer(6, log_message, task_id, session)
            return True
        except:
            log_message = "S3 read failure %s" % s3filename
            self.log_writer(6, log_message, task_id, session)

        return False

    def parser(self, message, s3bucket, task_id, session):
        flag = False
        print message.get_body()
        parsed_json = json.loads(message.get_body())
        event_name = parsed_json['Records'][0]['eventName']
        if event_name == 'ObjectCreated:Put':
            s3_file_object = parsed_json['Records'][0]['s3']['object']
            key = s3_file_object['key']
            if key.startswith('hound') is True:
                flag = self.s3read(key, s3bucket, task_id, session)
            else:
                print "bad key:%s" % key

        return flag

    def queue_poller(self, task_id, session):
        counter = 0

        s3connection = S3Connection()
        s3bucket = s3connection.get_bucket(s3_name)

        qconnection = SQSConnection()
        queue = qconnection.create_queue(sqs_name)
        results = queue.get_messages(3)
        while (len(results) > 0):
            print "length:%d" % len(results)
            for message in results:
                flag = self.parser(message, s3bucket, task_id, session)
                if flag is True:
                    counter += 1
                    queue.delete_message(message)

            results = queue.get_messages(10)

        return counter

    def execute(self):
        start_time = time.time()

        mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)
        engine = create_engine(mysql_url, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        task_log = TaskLog('Reader')
        session.add(task_log)
        session.commit()

        self.log_writer(6, 'start', task_log.id, session)

        population = self.queue_poller(task_log.id, session)

        duration = time.time() - start_time
        log_message = "stop w/population %d and duration %d" % (population, duration)
        self.log_writer(6, log_message, task_log.id, session)

print 'sqs_reader start'

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

    driver = SqsReader()
    driver.execute()

    syslog.closelog()

print 'sqs_reader stop'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
