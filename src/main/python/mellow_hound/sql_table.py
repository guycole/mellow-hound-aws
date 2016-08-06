#
# Title:sql_table.py
# Description:
# Development Environment:OS X 10.9.3/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime

from sqlalchemy import Column
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ApplicationLog(Base):
    __tablename__ = 'application_log'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    task_id = Column(BigInteger)
    facility = Column(String)
    level = Column(Integer)
    event = Column(String)

    def __init__(self, task, facility, level, event):
        self.task_id = task
        self.facility = facility
        self.level = level
        self.event = event

    def __repr__(self):
        return "<application_log(%d, %d, %s, %d, %s)>" % (self.id, self.task_id, self.facility, self.level, self.event)

class Census(Base):
    __tablename__ = 'census'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    census_task_id = Column(BigInteger)
    table_name = Column(String)
    population = Column(BigInteger)

    def __init__(self, task, table_name, population):
        self.census_task_id = task
        self.table_name = table_name
        self.population = population

    def __repr__(self):
        return "<census(%d, %s, %d)>" % (self.id, self.table_name, self.population)

class FileStat(Base):
    __tablename__ = "file_stat"

    id = Column(BigInteger, primary_key=True)
    creation_task = Column(BigInteger)
    update_task = Column(BigInteger)
    size = Column(BigInteger)
    full_name = Column(String)
    sha1_hash = Column(String)

    def __init__(self, task, size, full_name, sha1_hash):
        self.creation_task = task
        self.update_task = 0
        self.size = size
        self.full_name = full_name
        self.sha1_hash = sha1_hash

class Fundamental(Base):
    __tablename__ = "fundamental"

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    creation_task_id = Column(BigInteger)
    scorer_task_id = Column(BigInteger)
    market_date_id = Column(BigInteger)
    name_id = Column(BigInteger)
    sector = Column(String)
    industry = Column(String)
    pe = Column(Float)
    eps = Column(Float)
    div_yield = Column(Float)
    shares = Column(BigInteger)
    dps = Column(Float)
    peg = Column(Float)
    pts = Column(Float)
    ptb = Column(Float)

    def __init__(self, task):
        self.creation_task_id = task

class LoadLog(Base):
    __tablename__ = 'load_log'

    id = Column(BigInteger, primary_key=True)
    creation_task = Column(BigInteger)
    update_task = Column(BigInteger)
    market = Column(String)
    directory = Column(String)
    file_name = Column(String)
    full_name = Column(String)
    duplicate_row = Column(Integer)
    fail_row = Column(Integer)
    success_row = Column(Integer)
    fresh_name_row = Column(Integer)
    duration = Column(Integer)

    def __init__(self, task, market, directory, file_name, full_name):
        self.creation_task = task
        self.update_task = 0
        self.market = market
        self.directory = directory
        self.file_name = file_name
        self.full_name = full_name
        self.duplicate_row = 0
        self.fail_row = 0
        self.success_row = 0
        self.fresh_name_row = 0
        self.duration = 0

    def __repr__(self):
        return "<load_log(%d, %s)>" % (self.id, self.file_name)

class LoadLogSummary(Base):
    __tablename__ = 'load_log_summary'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger)

    def __init__(self, task):
        self.creation_task_id = task

class Market(Base):
    __tablename__ = 'market'

    id = Column(BigInteger, primary_key=True)
    creation_task = Column(BigInteger)
    update_task = Column(BigInteger)
    scorer_task = Column(BigInteger)
    symbol = Column(String)
    name = Column(String)

    def __init__(self, task, symbol, name):
        self.creation_task = task
        self.update_task = 0
        self.scorer_task = 0
        self.symbol = symbol
        self.name = name

    def __repr__(self):
        return "<market(%d, %s, %s)>" % (self.id, self.symbol, self.name)

class MarketDate(Base):
    __tablename__ = 'market_date'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger)

    def __init__(self, task):
        self.creation_task_id = task

class Name(Base):
    __tablename__ = 'name'

    id = Column(BigInteger, primary_key=True)
    creation_task = Column(BigInteger)
    update_task = Column(BigInteger)
    market = Column(BigInteger)
    symbol = Column(String)
    name = Column(String)
    active = Column(Boolean)
    equity = Column(Boolean)
    mkt_ndx = Column(Boolean)
    equity_option = Column(Boolean)
    future = Column(Boolean)
    forex = Column(Boolean)
    put_call = Column(Boolean)
    root_symbol = Column(String)
    expiration = Column(Date)
    strike = Column(BigInteger)

    def __init__(self, task, market, symbol, name):
        self.creation_task = task
        self.update_task = 0
        self.market = market
        self.symbol = symbol
        self.name = name
        self.active = True
        self.equity = True
        self.mkt_ndx = False
        self.equity_option = False
        self.future = False
        self.forex = False
        self.put_call = False
        self.root_symbol = 'None'
        self.expiration = datetime.datetime.utcfromtimestamp(0)
        self.strike = 0

    def __repr__(self):
        return "<name(%d, %s, %s)>" % (self.id, self.symbol, self.name)

class NameChange(Base):
    __tablename__ = 'name_change'

    id = Column(BigInteger, primary_key=True)
    creation_task = Column(BigInteger)
    update_task = Column(BigInteger)
    scorer_task = Column(BigInteger)
    change_date = Column(Date)
    old_market = Column(String)
    old_symbol = Column(String)
    new_market = Column(String)
    new_symbol = Column(String)

    def __init__(self, task, change_date, old_market, old_symbol, new_market, new_symbol):
        self.creation_task = task
        self.update_task = 0
        self.scorer_task = 0
        self.change_date = change_date
        self.old_market = old_market
        self.old_symbol = old_symbol
        self.new_market = new_market
        self.new_symbol = new_symbol

    def __repr__(self):
        return "<name_change(%d, %s, %s)>" % (self.id, self.old_symbol, self.old_market)

class Price(Base):
    __tablename__ = 'price'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger)

    def __init__(self, task):
        self.creation_task_id = task

class RawFileLog(Base):
    __tablename__ = 'raw_file_log'

    id = Column(BigInteger, primary_key=True)
    creation_task_id = Column(BigInteger)
    normalized_name = Column(String)
    update_flag = Column(Boolean)
    file_size = Column(BigInteger)
    access_time = Column(BigInteger)
    create_time = Column(BigInteger)
    modify_time = Column(BigInteger)
    sha1_hash = Column(String)

    def __init__(self, task, name, update, size, access, create, modify, sha1):
        self.creation_task_id = task
        self.normalized_name = name
        self.update_flag = update
        self.file_size = size
        self.access_time = access
        self.create_time = create
        self.modify_time = modify
        self.sha1_hash = sha1

    def __repr__(self):
        return "<rawfilelog(%d, %s, %d, %s)>" % (self.id, self.normalized_name, self.file_size, self.sha1_hash)

class RawFileSummary(Base):
    __tablename__ = 'raw_file_summary'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    creation_task_id = Column(BigInteger)
    duration = Column(Integer)
    total_pop = Column(Integer)
    update_pop = Column(Integer)

    def __init__(self, task, duration, total, update):
        self.creation_task_id = task
        self.duration = duration
        self.total_pop = total
        self.update_pop = update

    def __repr__(self):
        return "<rawfilesum(%d, %d, %d, %d)>" % (self.id, self.creation_task_id, self.duration, self.update_pop)

class Split(Base):
    __tablename__ = 'split'

    id = Column(BigInteger, primary_key=True)
    creation_task = Column(BigInteger)
    scorer_task = Column(BigInteger)
    market = Column(String)
    symbol = Column(String)
    split_date = Column(Date)
    split_ratio = Column(String)

    def __init__(self, task, split_date, market, symbol, ratio):
        self.creation_task = task
        self.scorer_task = 0
        self.market = market
        self.symbol = symbol
        self.split_date = split_date
        self.split_ratio = ratio

    def __repr__(self):
        return "<split(%d, %s, %s)>" % (self.id, self.symbol, self.split_ratio)

class TaskLog(Base):
    __tablename__ = 'task_log'

    id = Column(BigInteger, primary_key=True)
    command = Column(String)

    def __init__(self, command):
        self.command = command

    def __repr__(self):
        return "<task_log(%d, %s)>" % (self.id, self.command)

class Technical(Base):
    __tablename__ = 'technical'

    id = Column(BigInteger, primary_key=True)
    command = Column(String)

    def __init__(self, command):
        self.command = command

    def __repr__(self):
        return "<technical(%d, %s)>" % (self.id, self.command)

