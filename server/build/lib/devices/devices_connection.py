# ARP utils
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.exception import ConnectError
from jnpr.junos.op.arp import ArpTable as JunosARP
from jnpr.junos.op.elsethernetswitchingtable import ElsEthernetSwitchingTable
from jnpr.junos.op.phyport import PhyPortTable
from netmiko import ConnectHandler, ssh_exception, Netmiko
# Local modules
from properties.properties import DataBaseProps
from model.model_db import *
from utilities.utils_db import TableJSONEncoder
from devices.devices_db import *
from arp_service.arp_db import *

from pprint import pprint as pp
from lxml import etree
import pandas as pd
import re
import json
import sys


def get_device_config(device):
    ip = device["ip"]
    vend = device["vendor"]
    try:
        if(vend == VendorEnum.juniper.name):
            return get_juniper_config(ip)
        elif(vend == VendorEnum.cisco.name):
            return get_cisco_config(ip)
        else:
            return "device not found"
    
    except ConnectionError as e:
        print ("Cannot connect to device: {0}\n".format(e))
        return e
        # sys.exit(1)
    except Exception as ex:
        print ("\nException raised: {0}\n".format(ex) )
        return ex
        # sys.exit(1)

def get_juniper_config(ip):
    with Device(host=ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_PASSWORD) as dev:
        dev.open()
        dev.timeout = 150
        data = dev.rpc.get_config(options={'format':'text'})
        dev.close()
        return etree.tostring(data, encoding='unicode', pretty_print=True)

def get_cisco_config(ip):
        protocol = get_device_protocol(ip)
        device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
        Device = {
            "host": ip,
            "username": DataBaseProps.TEST_USER,
            "password": DataBaseProps.TEST_PASSWORD,
            "device_type": device_type,
        }
        connect = ConnectHandler(**Device)
        connect.enable()
        data = connect.send_command("show configuration")
        connect.disconnect()
        return data

def get_device_config_cisco(device):
    print("CIS")

def device_cli_juniper(device_ip, commands):
    result = []
    try:
        with Device(host=device_ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_USER) as dev:
            dev.timeout = 15
            ss = Startshell(Device)
            dev.close()
            return df

    except ConnectionError as e:
        print ("Cannot connect to device: {0}\n".format(e))
        # sys.exit(1)
    except Exception as ex:
        print ("\nException raised: {0}\n".format(ex) )
        # sys.exit(1)