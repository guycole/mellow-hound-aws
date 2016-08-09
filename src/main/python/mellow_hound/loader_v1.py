#! /usr/bin/python
#
# Title:loader_v1.py
# Description:load version1 messages
# Development Environment:OS X 10.10.5/Python 2.7.7
# Author:G.S. Cole (guycole at gmail dot com)
#
import datetime
import syslog

from sql_table import ApplicationLog
from sql_table import Ble
from sql_table import Cdma
from sql_table import GeoLoc
from sql_table import Gsm
from sql_table import Installation
from sql_table import Lte
from sql_table import Observation
from sql_table import Wcdma
from sql_table import WiFi

class LoaderVersion1:

    def log_writer(self, level, message, task_id, session):
        """
        logger
        """
        print message

        syslog.syslog(syslog.LOG_INFO, message)

        session.add(ApplicationLog(task_id, 'LoaderV1', level, message))
        session.commit()

    def select_installation(self, inst_uuid, phone1, task_id, session):
        selected = session.query(Installation).filter_by(uuid = inst_uuid).first()

        if selected == None:
            log_message = "new installation:%s" % (inst_uuid)
            self.log_writer(6, log_message, task_id, session)

            fresh = Installation(inst_uuid, phone1, 'android')
            session.add(fresh)
            session.commit()
            return fresh

        return selected

    def insert_geo_loc(self, observation_id, parsed_json, task_id, session):
        raw_time = parsed_json['fixTimeMs']
        fix_time = datetime.datetime.utcfromtimestamp(raw_time/1000)

        accuracy = parsed_json['accuracy']
        altitude = parsed_json['altitude']
        latitude = parsed_json['latitude']
        longitude = parsed_json['longitude']
        provider = parsed_json['provider']

        fresh = GeoLoc(observation_id, fix_time, provider, accuracy, altitude, latitude, longitude)
        session.add(fresh)
        session.commit()
        return fresh

    def insert_observation(self, installation_id, network_name, network_operator, session):
        fresh = Observation(installation_id, 0, network_name, network_operator)
        session.add(fresh)
        session.commit()
        return fresh

    def process_ble(self, observation_id, parsed_json, task_id, session):
        try:
            address = parsed_json['address']
            name = parsed_json['name']
            rssi = parsed_json['rssi']
            raw_scan = parsed_json['rawScan']

            if raw_scan.endswith(','):
                raw_scan = raw_scan[:len(raw_scan)-1]
        except:
            print 'ble parse failure'
            return

        fresh = Ble(observation_id, address, name, rssi, raw_scan)
        session.add(fresh)
        session.commit()

        self.ble_loaded += 1

        return fresh

    def process_wifi(self, observation_id, parsed_json, session):
        try:
            ssid = parsed_json['ssid']
            if len(ssid) < 1:
                ssid = 'empty ssid'
            bssid = parsed_json['bssid']
            capability = parsed_json['capability']
            frequency = parsed_json['frequency']
            level = parsed_json['level']
        except:
            print 'wifi parse failure'
            return

        fresh = WiFi(observation_id, frequency, level, ssid, bssid, capability)
        session.add(fresh)
        session.commit()

        self.wifi_loaded += 1

        return fresh

    def process_cdma(self, observation_id, parsed_json, session):
        try:
            register_flag = parsed_json['registerFlag']
            base_station = parsed_json['baseStation']
            latitude = parsed_json['latitude']
            longitude = parsed_json['longitude']
            network = parsed_json['network']
            system = parsed_json['system']
            asu_level = parsed_json['asuLevel']
            cdma_dbm = parsed_json['cdmaDbm']
            cdma_ecio = parsed_json['cdmaEcio']
            cdma_level = parsed_json['cdmaLevel']
            dbm = parsed_json['dbm']
            evdo_dbm = parsed_json['evdoDbm']
            evdo_ecio = parsed_json['evdoEcio']
            evdo_level = parsed_json['evdoLevel']
            evdo_snr = parsed_json['evdoSnr']
            level = parsed_json['level']
        except:
            print 'cdma parse failure'
            return

        fresh = Cdma(observation_id)
        fresh.observation_id = observation_id
        fresh.register_flag = register_flag
        fresh.base_station = base_station
        fresh.latitude = latitude
        fresh.longitude = longitude
        fresh.network = network
        fresh.system = system
        fresh.asu_level = asu_level
        fresh.cdma_dbm = cdma_dbm
        fresh.cdma_ecio = cdma_ecio
        fresh.cdma_level = cdma_level
        fresh.dbm = dbm
        fresh.evdo_dbm = evdo_dbm
        fresh.evdo_ecio = evdo_ecio
        fresh.evdo_level = evdo_level
        fresh.evdo_snr = evdo_snr
        fresh.level = level

        session.add(fresh)
        session.commit()

        self.cdma_loaded += 1

        return fresh

    def process_gsm(self, observation_id, parsed_json, session):
        try:
            register_flag = parsed_json['registerFlag']
            arfcn = parsed_json['arfcn']
            bsic = parsed_json['bsic']
            cid = parsed_json['cid']
            lac = parsed_json['lac']
            mcc = parsed_json['mcc']
            mnc = parsed_json['mnc']
            asu_level = parsed_json['asuLevel']
            dbm = parsed_json['dbm']
            level = parsed_json['level']
        except:
            print 'gsm parse failure'
            return

        fresh = Gsm(observation_id)
        fresh.register_flag = register_flag
        fresh.arfcn = arfcn
        fresh.bsic = bsic
        fresh.cid = cid
        fresh.lac = lac
        fresh.mcc = mcc
        fresh.mnc = mnc
        fresh.asu_level = asu_level
        fresh.dbm = dbm
        fresh.level = level

        session.add(fresh)
        session.commit()

        self.gsm_loaded += 1

        return fresh

    def process_lte(self, observation_id, parsed_json, session):
        try:
            register_flag = parsed_json['registerFlag']
            ci = parsed_json['ci']
            earfcn = parsed_json['earfcn']
            mcc = parsed_json['mcc']
            mnc = parsed_json['mnc']
            pci = parsed_json['pci']
            tac = parsed_json['tac']

            asu_level = parsed_json['asuLevel']
            dbm = parsed_json['dbm']
            level = parsed_json['level']
            timing_advance = parsed_json['timingAdvance']
        except:
            print 'lte parse failure'
            return

        fresh = Lte(observation_id)
        fresh.register_flag = register_flag
        fresh.ci = ci
        fresh.earfcn = earfcn
        fresh.mcc = mcc
        fresh.mnc = mnc
        fresh.pci = pci
        fresh.tac = tac
        fresh.asu_level = asu_level
        fresh.dbm = dbm
        fresh.level = level
        fresh.timing_advance = timing_advance

        session.add(fresh)
        session.commit()

        self.lte_loaded += 1

        return fresh

    def process_wcdma(self, observation_id, parsed_json, session):
        try:
            register_flag = parsed_json['registerFlag']
            cid = parsed_json['cid']
            lac = parsed_json['lac']
            mcc = parsed_json['mcc']
            mnc = parsed_json['mnc']
            psc = parsed_json['psc']
            uarfcn = parsed_json['uarfcn']

            asu_level = parsed_json['asuLevel']
            dbm = parsed_json['dbm']
            level = parsed_json['level']
        except:
            print 'wcdma parse failure'
            return

        fresh = Wcdma(observation_id)
        fresh.register_flag = register_flag
        fresh.cid = cid
        fresh.lac = lac
        fresh.mcc = mcc
        fresh.mnc = mnc
        fresh.psc = psc
        fresh.uarfcn = uarfcn
        fresh.asu_level = asu_level
        fresh.dbm = dbm
        fresh.level = level

        session.add(fresh)
        session.commit()

        self.wcdma_loaded += 1

        return fresh

    def process_cellular(self, observation_id, parsed_json, session):
        cell_type = parsed_json['cellType']
        print cell_type
        if cell_type == 'cdma':
            self.process_cdma(observation_id, parsed_json, session)
        elif cell_type == 'gsm':
            self.process_gsm(observation_id, parsed_json, session)
        elif cell_type == 'lte':
            self.process_lte(observation_id, parsed_json, session)
        elif cell_type == 'wcdma':
            self.process_wcdma(observation_id, parsed_json, session)

    def execute(self, parsed_json, task_id, session):
        installation = self.select_installation(parsed_json['installation'], parsed_json['phone1'], task_id, session)

        network_name = parsed_json['networkName']
        network_operator = parsed_json['networkOperator']
        observation = self.insert_observation(installation.id, network_name, network_operator, session)

        geo_loc = self.insert_geo_loc(observation.id, parsed_json['geoLoc'], task_id, session)

        self.ble_loaded = 0
        ble_list = parsed_json['ble']
        for ble in ble_list:
            self.process_ble(observation.id, ble, task_id, session)

        self.wifi_loaded = 0
        wifi_list = parsed_json['wiFi']
        for wifi in wifi_list:
            self.process_wifi(observation.id, wifi, session)

        self.cdma_loaded = 0
        self.gsm_loaded = 0
        self.lte_loaded = 0
        self.wcdma_loaded = 0
        cellular_list = parsed_json['cellular']
        for cellular in cellular_list:
            self.process_cellular(observation.id, cellular, session)

        return (observation.id, self.ble_loaded, self.wifi_loaded, self.cdma_loaded, self.gsm_loaded, self.lte_loaded, self.wcdma_loaded)

#;;; Local Variables: ***
#;;; mode:python ***
#;;; End: ***