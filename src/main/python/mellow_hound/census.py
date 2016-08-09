#! /usr/bin/python
#
# Title:census.py
# Description:visit defined tables and record row population
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import sys
import syslog
import time
import yaml

from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_table import ApplicationLog
from sql_table import Ble
from sql_table import Cdma
from sql_table import Census
from sql_table import GeoLoc
from sql_table import Gsm
from sql_table import Installation
from sql_table import LoadLog
from sql_table import Lte
from sql_table import Observation
from sql_table import TaskLog
from sql_table import Wcdma
from sql_table import WiFi

class CensusDriver:

    def census(self, task_id, table_name, population, session):
        census = Census(task_id, table_name, population)
        session.add(census)
        session.commit()

    def execute(self, task_id, session):
        start_time = time.time()

        population = session.query(func.count(ApplicationLog.id)).scalar()
        self.census(task_id, 'application_log', population, session)

        population = session.query(func.count(Ble.id)).scalar()
        self.census(task_id, 'ble', population, session)

        population = session.query(func.count(Cdma.id)).scalar()
        self.census(task_id, 'cdma', population, session)

        population = session.query(func.count(GeoLoc.id)).scalar()
        self.census(task_id, 'geoloc', population, session)

        population = session.query(func.count(Gsm.id)).scalar()
        self.census(task_id, 'gsm', population, session)

        population = session.query(func.count(Installation.id)).scalar()
        self.census(task_id, 'installation', population, session)

        population = session.query(func.count(LoadLog.id)).scalar()
        self.census(task_id, 'load_log', population, session)

        population = session.query(func.count(Lte.id)).scalar()
        self.census(task_id, 'lte', population, session)

        population = session.query(func.count(Observation.id)).scalar()
        self.census(task_id, 'observation', population, session)

        population = session.query(func.count(TaskLog.id)).scalar()
        self.census(task_id, 'task_log', population, session)

        population = session.query(func.count(Wcdma.id)).scalar()
        self.census(task_id, 'wcdma', population, session)

        population = session.query(func.count(WiFi.id)).scalar()
        self.census(task_id, 'wifi', population, session)

        stop_time = time.time()
        return stop_time - start_time

print 'start'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL3)
    syslog.syslog(syslog.LOG_INFO, 'start mellow hound census')

    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        fileName = 'config.dev'

    configuration = yaml.load(file(fileName))

    mysql_username = configuration['mySqlUserName']
    mysql_password = configuration['mySqlPassWord']
    mysql_hostname = configuration['mySqlHostName']
    mysql_database = configuration['mySqlDataBase']

    mysql_url = "mysql://%s:%s@%s:3306/%s" % (mysql_username, mysql_password, mysql_hostname, mysql_database)

    engine = create_engine(mysql_url, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    task_log = TaskLog('CensusDriver')
    session.add(task_log)
    session.commit()

    application_log = ApplicationLog(task_log.id, 'CensusDriver', 6, 'CensusDriver Begin')
    session.add(application_log)
    session.commit()

    driver = CensusDriver()

    duration = 0
    duration = driver.execute(task_log.id, session)

    log_message = "CensusDriver End w/duration:%d" % duration
    application_log = ApplicationLog(task_log.id, 'CensusDriver', 6, log_message)
    session.add(application_log)
    session.commit()
    session.close()

    syslog.syslog(syslog.LOG_INFO, 'stop mellow hound census')
    syslog.closelog()

print 'stop'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
