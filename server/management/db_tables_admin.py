from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, PrimaryKeyConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import UnboundExecutionError, OperationalError
from jnpr.junos.exception import ConnectUnknownHostError
from pprint import pprint as pp
from flask_sqlalchemy import SQLAlchemy

import pandas as pd

from model.model_db import *
from properties.properties import DataBaseProps
from utilities.utils_db import *
from arp_service.arp_connection import *
from arp_service.arp_connection import *

from datetime import datetime
import enum
import sys

def create_db():
    ''' Create database tables previously defined '''
    try: 
        Base.metadata.create_all(engine, checkfirst=True)
    except Exception as ex:
        print(ex)


def delete_db():
    ''' Drops all tables from database'''
    try:
        print("Deleting")
        NeighborsTable.__table__.drop(checkfirst=True)
        InterfacesTable.__table__.drop(checkfirst=True)
        EthernetSwitchingTable.__table__.drop(checkfirst=True)
        ArpTable.__table__.drop(checkfirst=True)
        Devices.__table__.drop(checkfirst=True)
        DeviceVendors.__table__.drop(checkfirst=True)
        DeviceType.__table__.drop(checkfirst=True)
        DeviceConnection.__table__.drop(checkfirst=True)
    except UnboundExecutionError as e:
        try:
            print(e, "\nProceding to delete with Engine")
            NeighborsTable.__table__.drop(engine, checkfirst=True)
            InterfacesTable.__table__.drop(engine, checkfirst=True)
            EthernetSwitchingTable.__table__.drop(engine, checkfirst=True)
            ArpTable.__table__.drop(engine, checkfirst=True)
            Devices.__table__.drop(engine, checkfirst=True)
            DeviceVendors.__table__.drop(engine, checkfirst=True)
            DeviceType.__table__.drop(engine, checkfirst=True)
            DeviceConnection.__table__.drop(engine, checkfirst=True)
        except OperationalError as e:
            print("ERROR DELETING TABLES FROM DATABASE:\nError info => ",e)
        except UnboundExecutionError as e:
            print("ERROR DELETING TABLES FROM DATABASE:\nError info => ",e)


def delete_table(*args):
    ''' Drop selected table/s from DB '''
    for table in args:
        try:
            print("Dropping {0} from database...".format(table.__tablename__))
            table.__table__.drop(checkfirst=True)
        except UnboundExecutionError as e:
            try:
                print(e, "\nProceding to delete with Engine")
                table.__table__.drop(engine, checkfirst=True)
            except OperationalError as e:
                print("ERROR DELETING TABLES FROM DATABASE:\nError info => ",e)
            except UnboundExecutionError as e:
                print("ERROR DELETING TABLES FROM DATABASE:\nError info => ",e)