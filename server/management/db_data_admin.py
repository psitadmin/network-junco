from devices.devices_connection import CiscoDevice, JuniperDevice
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, PrimaryKeyConstraint, text, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import UnboundExecutionError, OperationalError
from jnpr.junos.exception import ConnectUnknownHostError
from pprint import pprint as pp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
import logging

import pandas as pd

from model.model_db import *
from properties.properties import DataBaseProps
from utilities.utils_db import *
from arp_service.arp_connection import *
from arp_service.arp_connection import *
from devices.devices_db import edit_device

from datetime import datetime
import sys

class OperatingDB():
    ''' Utiliy class from general operations on DB tables '''

    def delete_data_from_table(*args):
        ''' Delete all data from table '''
        with Session() as session:
            for table in args:
                try:
                    print("Deleting data from table {0}...".format(table.__tablename__, checkfirst=True))
                    print(session.query(table).delete())
                    session.commit()
                except Exception as e:
                    print(e)
                
            session.close()


class PopulateDB():
    ''' Utility class to put, update or delete data on arp related tables '''

    # Populate Enum classes
    def populate_vendors():
        with Session() as session:
            for i in VendorEnum:
                session.add( DeviceVendors( name = i.name ) )
            session.commit()
            session.close()
    def populate_connection_type():
        with Session() as session:
            for i in DeviceConnectionEnum:
                session.add( DeviceConnection( name = i.name ) )
            session.commit()
            session.close()
    def populate_device_type():
        with Session() as session:
            for i in DeviceTypeEnum:
                session.add( DeviceType( name = i.name ) )
            session.commit()
            session.close()
    def populate_enum_tables():
        PopulateDB.populate_vendors()
        PopulateDB.populate_connection_type()
        PopulateDB.populate_device_type()
    # ========================================


    def populate_devices():
        ''' Update database devices table from .csv file '''
        # Saving deafult output
        old_stdout = sys.stdout
        # Creating files
        log_file = open(datetime.now().strftime('%Y_%m_%d_%H_%M_db_devices.log'), "w")
        logging.basicConfig(filename=datetime.now().strftime('log_devices_%Y_%m_%d_%H_%M.log'), encoding='utf-8', level=logging.INFO)
        # Swapping standard output
        sys.stdout = log_file
        df = get_devices_csv()
        # print(df.columns)

        with Session() as session:
        # Creating session
            # Iterating dataframe rows to retrieve device params
            for index, row in df.iterrows():
                try:
                    # Check if IP/NAME exist in database
                    exist = session.query(Devices).filter(or_(Devices.ip == row['ip'], Devices.name == row['name'])).first()
                    # Adding items to query
                    if(exist is not None):
                        # If name or ip exist -> updating device object with new params
                        exist.ip =  row['ip'].strip()
                        exist.name = row['name'].removesuffix('.hi.inet').upper().strip()
                        exist.vendor = VendorEnum[ row['vendor'].lower().strip() ].value
                        exist.device_type = DeviceTypeEnum[ row['device_type'].lower().strip() ].value
                        exist.connection_type = DeviceConnectionEnum[ row['connection'].lower().strip() ].value
                        if (row['vendor'].lower() == "juniper"):
                            exist.serial_number = JuniperDevice.get_serial_number(row['ip'].strip())
                            exist.device_model = JuniperDevice.get_device_model(row['ip'].strip())
                        elif (row['vendor'].lower() == "cisco"):
                            exist.serial_number = CiscoDevice.get_serial_number(row['ip'].strip())
                            exist.device_model = CiscoDevice.get_device_model(row['ip'].strip())
                        exist.location = resolve_location(row['name'].removesuffix('.hi.inet')).strip()
                        exist.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        print("{0} Existe: {1}\n".format(exist.id, exist))
                        session.merge(exist)

                    else:
                        # Adding new device to DB
                        dev = Devices(
                            ip = row['ip'].strip(),
                            name = row['name'].removesuffix('.hi.inet').upper().strip(),
                            vendor = VendorEnum[ row['vendor'].lower().strip() ].value,
                            serial_number = '',
                            device_model = '',
                            connection_type = DeviceConnectionEnum[ row['connection'].lower().strip() ].value,
                            device_type = DeviceTypeEnum[ row['device_type'].lower().strip() ].value,
                            location = resolve_location(row['name'].removesuffix('.hi.inet')).strip(),
                            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        )
                        session.merge(dev)
                        session.commit()
                        new_dev = session.query(Devices).filter(or_(Devices.ip == row['ip'], Devices.name == row['name'])).first()
                        if (row['vendor'].lower() == "juniper"):
                            new_dev.serial_number = JuniperDevice.get_serial_number(row['ip'].strip())
                            new_dev.device_model = JuniperDevice.get_device_model(row['ip'].strip())
                        elif (row['vendor'].lower() == "cisco"):
                            new_dev.serial_number = CiscoDevice.get_serial_number(row['ip'].strip())
                            new_dev.device_model = CiscoDevice.get_device_model(row['ip'].strip())
                        print("{0} Añadiendo nuevo: {1}\n".format(index+1, dev))

                    # UPDATE on database
                    session.commit()
                
                except Exception as e:
                    print (e)

            session.close()

        sys.stdout = old_stdout
        log_file.close()

    def populate_arp_tables():
        # Saving deafult output
        old_stdout = sys.stdout
        # Creating files
        log_file = open(datetime.now().strftime('%Y_%m_%d_%H_%M_log_db_arp.log'), "w")
        logging.basicConfig(filename=datetime.now().strftime('log_arp_%Y_%m_%d_%H_%M.log'), encoding='utf-8', level=logging.INFO)
        # Swapping standard output
        sys.stdout = log_file

        with Session() as session:
            try:
                # Get all devices
                devices = get_all_devices()
                print("Se han encontrado {0} dispositivos".format(devices.count()))
                logging.info("Se han encontrado {0} dispositivos".format(devices.count()))
                
                for d in devices:
                    logging.info("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    print("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    arp_table = pd.DataFrame()
                    if (d.vendor.name == 'juniper'):
                        arp_table = JuniperARP.get_arp_table(d.ip)
                    elif(d.vendor.name == 'cisco'):
                        arp_table = CiscoARP.get_arp_table(d.ip)
                    elif(d.vendor.name == 'dell'):
                        arp_table = DellARP.get_arp_table(d.ip)
                    elif(d.vendor.name == 'arista'):
                        arp_table = AristaARP.get_arp_table(d.ip)
                    else:
                        print("\nUNKNOW DEVICE VENDOR\n")
                        logging.info("\nUNKNOW DEVICE VENDOR\n")

                    if(arp_table is not None):
                        save_arp_table(d.ip, arp_table)
                    print(arp_table, "\n============================ >\n\n")
                    # logging.info(arp_table, "\n============================ >\n\n")

                # print( devices.all() )
            except ConnectionError as e:
                logging.error("Cannot connect to device: {0}\n".format(e))
                # sys.exit(1)
            except Exception as ex:
                logging.error("\nException raised: {0}\n".format(ex) )
                # sys.exit(1)
            session.close()

        sys.stdout = old_stdout
        log_file.close()


    def populate_ethernet_switching ():
        # Saving deafult output
        old_stdout = sys.stdout
        # Creating files
        log_file = open(datetime.now().strftime('%Y_%m_%d_%H_%M_log_db_est.log'), "w")
        logging.basicConfig(filename=datetime.now().strftime('log_est_%Y_%m_%d_%H_%M.log'), encoding='utf-8', level=logging.INFO)
        # Swapping standard output
        sys.stdout = log_file

        with Session() as session:
            try:
                # Get all devices
                devices = get_all_devices()
                print("Se han encontrado {0} dispositivos".format(devices.count()))
                logging.info("Se han encontrado {0} dispositivos".format(devices.count()))

                for d in devices:
                    logging.info("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    print("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    ethernet_switching_table = pd.DataFrame()
                    if (d.vendor.name == 'juniper'):
                        ethernet_switching_table = JuniperARP.get_ethernet_switching_table(d.ip)
                    elif(d.vendor.name == 'cisco'):
                        ethernet_switching_table = CiscoARP.get_ethernet_switching_table(d.ip)
                    elif(d.vendor.name == 'dell'):
                        ethernet_switching_table = DellARP.get_ethernet_switching_table(d.ip)
                    elif(d.vendor.name == 'arista'):
                        ethernet_switching_table = AristaARP.get_ethernet_switching_table(d.ip)
                    else:
                        print("\nUNKNOW DEVICE VENDOR\n")
                        logging.info("\nUNKNOW DEVICE VENDOR\n")

                    if(ethernet_switching_table is not None):
                        save_ethernet_switching_table(d.ip, ethernet_switching_table)
                    print(ethernet_switching_table, "\n============================ >\n\n")
            except ConnectionError as e:
                logging.error("Cannot connect to device: {0}\n".format(e))
                # sys.exit(1)
            except Exception as ex:
                logging.error("\nException raised: {0}\n".format(ex) )
                # sys.exit(1)

            session.close()
        
        sys.stdout = old_stdout
        log_file.close()


    def populate_interfaces():
        # Saving deafult output
        old_stdout = sys.stdout
        # Creating files
        log_file = open(datetime.now().strftime('%Y_%m_%d_%H_%M_log_db_int.log'), "w")
        logging.basicConfig(filename=datetime.now().strftime('log_int_%Y_%m_%d_%H_%M.log'), encoding='utf-8', level=logging.INFO)
        # Swapping standard output
        sys.stdout = log_file

        with Session() as session:
            try:
                # Get all devices
                devices = get_all_devices()
                logging.info("Se han encontrado {0} dispositivos".format(devices.count()))
                for d in devices:
                    print("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    logging.info("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    interfaces_table = pd.DataFrame()
                    if (d.vendor.name == 'juniper'):
                        interfaces_table = JuniperARP.get_interfaces_table(d.ip)
                    elif(d.vendor.name == 'cisco'):
                        interfaces_table = CiscoARP.get_interfaces_table(d.ip)
                    elif(d.vendor.name == 'dell'):
                        interfaces_table = DellARP.get_interfaces_table(d.ip)
                    elif(d.vendor.name == 'arista'):
                        interfaces_table = AristaARP.get_interfaces_table(d.ip)
                    else:
                        logging.info("\nUNKNOW DEVICE VENDOR\n")

                    if(interfaces_table is not None):
                        save_interfaces_table(d.ip, interfaces_table)
                    print(interfaces_table, "\n============================ >\n\n")
            except ConnectionError as e:
                logging.error("Cannot connect to device: {0}\n".format(e))
                # sys.exit(1)
            except Exception as ex:
                logging.error("\nException raised: {0}\n".format(ex) )
                # sys.exit(1)

            session.close()

        sys.stdout = old_stdout
        log_file.close()


    def populate_neighbors():
        # Saving deafult output
        old_stdout = sys.stdout
        # Creating files
        log_file = open(datetime.now().strftime('%Y_%m_%d_%H_%M_log_db_nei.log'), "w")
        logging.basicConfig(filename=datetime.now().strftime('log_nei_%Y_%m_%d_%H_%M.log'), encoding='utf-8', level=logging.INFO)
        # Swapping standard output
        sys.stdout = log_file

        with Session() as session:
            try:
                # Get all devices
                devices = get_all_devices()
                logging.info("Se han encontrado {0} dispositivos".format(devices.count()))
                for d in devices:
                    print("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    logging.info("\n<================================ ({0}) DEVICE TODO ({1}): {2} - {3}".format(d.id, d.vendor.name, d.ip, d.name) )
                    neighbors_table = pd.DataFrame()
                    if (d.vendor.name == 'juniper'):
                        neighbors_table = JuniperARP.get_neighbors_table(d.ip)
                    if(d.vendor.name == 'cisco'):
                        neighbors_table = CiscoARP.get_neighbors_table(d.ip)
                    elif(d.vendor.name == 'dell'):
                        neighbors_table = DellARP.get_neighbors_table(d.ip)
                    elif(d.vendor.name == 'arista'):
                        neighbors_table = AristaARP.get_neighbors_table(d.ip)
                    else:
                        logging.info("\nUNKNOW DEVICE VENDOR\n")

                    if(neighbors_table is not None):
                        save_neighbors_table(d.ip, neighbors_table)
                    print(neighbors_table, "\n============================ >\n\n")
            except ConnectionError as e:
                logging.error("Cannot connect to device: {0}\n".format(e))
                # sys.exit(1)
            except Exception as ex:
                logging.error("\nException raised: {0}\n".format(ex) )
                # sys.exit(1)

            session.close()
    
        sys.stdout = old_stdout
        log_file.close()