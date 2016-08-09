#
# Title:sql_table.py
# Description: RDBMS wrapper
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

class Ble(Base):
    __tablename__ = 'ble'

    id = Column(BigInteger, primary_key=True)
    observation_id = Column(BigInteger)
    address = Column(String)
    name = Column(String)
    rssi = Column(Integer)
    raw_scan = Column(String)

    def __init__(self, observation_id, address, name, rssi, raw_scan):
        self.observation_id = observation_id
        self.address = address
        self.name = name
        self.rssi = rssi
        self.raw_scan = raw_scan

    def __repr__(self):
        return "<ble(%d, %s, %s)>" % (self.id, self.name, self.address)

class Cdma(Base):
    __tablename__ = 'cdma'

    id = Column(BigInteger, primary_key=True)
    observation_id = Column(BigInteger)
    register_flag = Column(Boolean)
    base_station = Column(Integer)
    latitude = Column(Integer)
    longitude = Column(Integer)
    network = Column(Integer)
    system = Column(Integer)
    asu_level = Column(Integer)
    cdma_dbm = Column(Integer)
    cdma_ecio = Column(Integer)
    cdma_level = Column(Integer)
    dbm = Column(Integer)
    evdo_dbm = Column(Integer)
    evdo_ecio = Column(Integer)
    evdo_level = Column(Integer)
    evdo_snr = Column(Integer)
    level = Column(Integer)

    def __init__(self, observation_id):
        self.observation_id = observation_id
        self.register_flag = False
        self.base_station = 0
        self.latitude = 0
        self.longitude = 0
        self.network = 0
        self.system = 0
        self.asu_level = 0
        self.cdma_dbm = 0
        self.cdma_ecio = 0
        self.cdma_level = 0
        self.dbm = 0
        self.evdo_dbm = 0
        self.evdo_ecio = 0
        self.evdo_level = 0
        self.evdo_snr = 0
        self.level = 0

    def __repr__(self):
        return "<cdma(%d, %d)>" % (self.id, self.observation_id)

class Census(Base):
    __tablename__ = 'census'

    id = Column(BigInteger, primary_key=True)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    task_id = Column(BigInteger)
    table = Column(String)
    population = Column(BigInteger)

    def __init__(self, task, table_name, population):
        self.task_id = task
        self.table = table_name
        self.population = population

    def __repr__(self):
        return "<census(%d, %s, %d)>" % (self.id, self.table, self.population)

class GeoLoc(Base):
    __tablename__ = 'geo_loc'

    id = Column(BigInteger, primary_key=True)
    observation_id = Column(BigInteger)
    time_stamp = Column(DateTime, default=datetime.datetime.utcnow)
    provider = Column(String)
    accuracy = Column(Float)
    altitude = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)

    def __init__(self, observation_id, time_stamp, provider, accuracy, altitude, latitude, longitude):
        self.observation_id = observation_id
        self.time_stamp = time_stamp
        self.provider = provider
        self.accuracy = accuracy
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "<geoloc(%d, %f, %f)>" % (self.id, self.latitude, self.longitude)

class Gsm(Base):
    __tablename__ = 'gsm'

    id = Column(BigInteger, primary_key=True)
    observation_id = Column(BigInteger)
    register_flag = Column(Boolean)
    arfcn = Column(Integer)
    bsic = Column(Integer)
    cid = Column(Integer)
    lac = Column(Integer)
    mcc = Column(Integer)
    mnc = Column(Integer)
    psc = Column(Integer)
    asu_level = Column(Integer)
    dbm = Column(Integer)
    level = Column(Integer)

    def __init__(self, observation_id):
        self.observation_id = observation_id
        self.register_flag = False
        self.arfcn = 0
        self.bsic = 0
        self.cid = 0
        self.lac = 0
        self.mcc = 0
        self.mnc = 0
        self.psc = 0
        self.asu_level = 0
        self.dbm = 0
        self.level = 0

    def __repr__(self):
        return "<gsm(%d, %d)>" % (self.id, self.observation_id)

class Installation(Base):
    __tablename__ = "installation"

    id = Column(BigInteger, primary_key=True)
    uuid = Column(String)
    phone_line = Column(String)
    platform = Column(String)
    device = Column(String)
    note = Column(String)

    def __init__(self, uuid, phone_line, platform):
        self.uuid = uuid
        self.phone_line = phone_line
        self.platform = platform
        self.device = 'unknown'
        self.note = 'no note'

    def __repr__(self):
        return "<installation(%d, %s, %s)>" % (self.id, self.phone_line, self.uuid)

class LoadLog(Base):
    __tablename__ = 'load_log'

    id = Column(BigInteger, primary_key=True)
    task_id = Column(BigInteger)
    observation_id = Column(BigInteger)
    version = Column(Integer)
    file_name = Column(String)
    ble_pop = Column(Integer)
    cell_cdma_pop = Column(Integer)
    cell_gsm_pop = Column(Integer)
    cell_lte_pop = Column(Integer)
    cell_wcdma_pop = Column(Integer)
    wifi_pop = Column(Integer)

    def __init__(self, task_id, observation_id, version, file_name):
        self.task_id = task_id
        self.observation_id = observation_id
        self.version = version
        self.file_name = file_name
        self.ble_pop = 0
        self.cell_cdma_pop = 0
        self.cell_gsm_pop = 0
        self.cell_lte_pop = 0
        self.cell_wcdma_pop = 0
        self.wifi_pop = 0

    def __repr__(self):
        return "<load_log(%d, %s)>" % (self.id, self.file_name)

class Lte(Base):
    __tablename__ = 'lte'

    id = Column(BigInteger, primary_key=True)
    observation_id = Column(BigInteger)
    register_flag = Column(Boolean)
    ci = Column(Integer)
    earfcn = Column(Integer)
    mcc = Column(Integer)
    mnc = Column(Integer)
    pci = Column(Integer)
    tac = Column(Integer)
    asu_level = Column(Integer)
    dbm = Column(Integer)
    level = Column(Integer)
    timing_advance = Column(Integer)

    def __init__(self, observation_id):
        self.observation_id = observation_id
        self.register_flag = False
        self.ci = 0
        self.earfcn = 0
        self.mcc = 0
        self.mnc = 0
        self.pci = 0
        self.tac = 0
        self.asu_level = 0
        self.dbm = 0
        self.level = 0
        self.timing_advance = 0

    def __repr__(self):
        return "<lte(%d, %d)>" % (self.id, self.observation_id)

class Observation(Base):
    __tablename__ = "observation"

    id = Column(BigInteger, primary_key=True)
    installation_id = Column(BigInteger)
    sortie_id = Column(BigInteger)
    network_name = Column(String)
    network_operator = Column(String)

    def __init__(self, installation_id, sortie_id, network_name, network_operator):
        self.installation_id = installation_id
        self.sortie_id = sortie_id
        self.network_name = network_name
        self.network_operator = network_operator

class TaskLog(Base):
    __tablename__ = 'task_log'

    id = Column(BigInteger, primary_key=True)
    command = Column(String)

    def __init__(self, command):
        self.command = command

    def __repr__(self):
        return "<task_log(%d, %s)>" % (self.id, self.command)

class Wcdma(Base):
    __tablename__ = 'wcdma'

    id = Column(BigInteger, primary_key=True)
    observation_id = Column(BigInteger)
    register_flag = Column(Boolean)
    cid = Column(Integer)
    lac = Column(Integer)
    mcc = Column(Integer)
    mnc = Column(Integer)
    psc = Column(Integer)
    uarfcn = Column(Integer)
    asu_level = Column(Integer)
    dbm = Column(Integer)
    level = Column(Integer)

    def __init__(self, observation_id):
        self.observation_id = observation_id
        self.register_flag = False
        self.cid = 0
        self.lac = 0
        self.mcc = 0
        self.mnc = 0
        self.psc = 0
        self.uarfcn = 0
        self.asu_level = 0
        self.dbm = 0
        self.level = 0

    def __repr__(self):
        return "<wcdma(%d, %d)>" % (self.id, self.observation_id)

class WiFi(Base):
    __tablename__ = 'wifi'

    id = Column(BigInteger, primary_key=True)
    observation_id = Column(BigInteger)
    frequency = Column(Integer)
    level = Column(Integer)
    ssid = Column(String)
    bssid = Column(String)
    capability = Column(String)
    passpoint_name = Column(String)
    passpoint_venue = Column(String)

    def __init__(self, observation_id, frequency, level, ssid, bssid, capability):
        self.observation_id = observation_id
        self.frequency = frequency
        self.level = level
        self.ssid = ssid
        self.bssid = bssid
        self.capability = capability
        self.passpoint_name = 'unknown'
        self.passpoint_venue = 'unknown'

    def __repr__(self):
        return "<wifi(%d, %s, %s)>" % (self.id, self.ssid, self.bssid)
