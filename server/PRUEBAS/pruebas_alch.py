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

# import socket

import json

from datetime import datetime
import logging
import sys


if __name__ == "__main__":
    
    logging.basicConfig(filename=datetime.now().strftime('log_est_%Y_%m_%d_%H_%M.log'), level=logging.INFO)
    logging.info(datetime.now().strftime('log_est_%Y_%m_%d_%H_%M.log'))