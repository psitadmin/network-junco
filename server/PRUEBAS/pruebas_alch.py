from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, PrimaryKeyConstraint, text, literal
from pprint import pprint as pp
from sqlalchemy.sql.expression import false, null
from utilities.utils_db import *
from tasks.interfacesTask import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy.exc import UnboundExecutionError, OperationalError
from jnpr.junos.utils.start_shell import StartShell
from devices.devices_connection import *
from devices.devices_db import *
from jnpr.junos import Device
from flask_sqlalchemy import SQLAlchemy
from arp_service.arp_db import *
from arp_service.calambuco import *
from arp_service.arp_connection import *
from model.model_db import *
from jnpr.junos.op.elsethernetswitchingtable import ElsEthernetSwitchingTable
from properties.properties import DataBaseProps
from arp_service.arp_connection import JuniperARP
from jnpr.junos.op.arp import ArpTable as JunosARP
from management.facade_db_admin import *
from netmiko import ConnectHandler, ssh_exception, Netmiko, dell
from netmiko.dell import dell_powerconnect
import paramiko
import dracclient.client
from cryptography.fernet import Fernet
from os import path
# import socket

import json

from datetime import datetime
import logging
import sys


if __name__ == "__main__":
    PATH = 'logs/'
    DIR = os.path.dirname(__file__)
    logging.basicConfig(filename=os.path.join(DIR, PATH)+'p1', filemode='a', level=logging.INFO, force=True)
    logging.info("hola 1")
    logging.basicConfig(filename=os.path.join(DIR, PATH)+'p2', filemode='a', level=logging.INFO, force=True)
    logging.info("hola 2")
    logging.basicConfig(filename=os.path.join(DIR, PATH)+'p3', filemode='a', level=logging.INFO, force=True)
    logging.info("hola 3")
    # log_1 = logging.getLogger('logger_1')
    # log_2 = logging.getLogger('logger_2')
    # log_3 = logging.getLogger('logger_3')
    # log_2.info("hola 2")
    # log_3.info("hola 3")

