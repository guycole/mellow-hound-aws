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
from sql_table import Census
from sql_table import FileStat
from sql_table import Fundamental
from sql_table import LoadLog
from sql_table import LoadLogSummary
from sql_table import Market
from sql_table import MarketDate
from sql_table import Name
from sql_table import NameChange
from sql_table import Price
from sql_table import RawFileLog
from sql_table import RawFileSummary
from sql_table import Split
from sql_table import TaskLog
from sql_table import Technical

class CensusDriver:

    def census(self, task_id, table_name, population, session):
        census = Census(task_id, table_name, population)
        session.add(census)
        session.commit()

    def execute(self, task_id, session):
        start_time = time.time()

        population = session.query(func.count(ApplicationLog.id)).scalar()
        self.census(task_id, 'application_log', population, session)

        population = session.query(func.count(FileStat.id)).scalar()
        self.census(task_id, 'file_stat', population, session)

        population = session.query(func.count(Fundamental.id)).scalar()
        self.census(task_id, 'fundamental', population, session)

        population = session.query(func.count(LoadLog.id)).scalar()
        self.census(task_id, 'load_log', population, session)

        population = session.query(func.count(LoadLogSummary.id)).scalar()
        self.census(task_id, 'load_log_summary', population, session)

        population = session.query(func.count(Market.id)).scalar()
        self.census(task_id, 'market', population, session)

        population = session.query(func.count(MarketDate.id)).scalar()
        self.census(task_id, 'market_date', population, session)

        population = session.query(func.count(Name.id)).scalar()
        self.census(task_id, 'name', population, session)

        population = session.query(func.count(NameChange.id)).scalar()
        self.census(task_id, 'name_change', population, session)

        population = session.query(func.count(Price.id)).scalar()
        self.census(task_id, 'price', population, session)

        population = session.query(func.count(RawFileLog.id)).scalar()
        self.census(task_id, 'raw_file_log', population, session)

        population = session.query(func.count(RawFileSummary.id)).scalar()
        self.census(task_id, 'raw_file_summary', population, session)

        population = session.query(func.count(Split.id)).scalar()
        self.census(task_id, 'split', population, session)

        population = session.query(func.count(TaskLog.id)).scalar()
        self.census(task_id, 'task_log', population, session)

        population = session.query(func.count(Technical.id)).scalar()
        self.census(task_id, 'technical', population, session)

        stop_time = time.time()
        return stop_time - start_time

print 'start'

#
# argv[1] = configuration filename
#
if __name__ == '__main__':
    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL3)
    syslog.syslog(syslog.LOG_INFO, 'start mythic eoddata census')

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

    syslog.syslog(syslog.LOG_INFO, 'stop mythic eoddata census')
    syslog.closelog()

print 'stop'

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***
