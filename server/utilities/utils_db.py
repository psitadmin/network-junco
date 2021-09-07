from jnpr.junos.factory.table import Table
from jnpr.junos.factory.view import View
from datetime import datetime
from properties.properties import DataBaseProps
from model.model_db import *
from datetime import datetime
import pandas as pd
import json
import re

REGEX_MAC_ADDRESS = re.compile(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$', re.I)
REGEX_INTERFACE = re.compile(r'(^(gi|te|ge|et|xe|efgx))-?[0-9]+(\/[0-9]{1,2}){1,2}(\.[0-9])?', re.I)
REGEX_GIGABIT_INTERFACE = re.compile(r'(gigabitethernet[0-9]\/[0-9]{1,2})',re.I)
REGEX_IP_ADDRESS = re.compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')


def check_interface(interface):
    result = False
    with Session() as session:
        result = (bool(REGEX_INTERFACE.match(interface))) or (bool(REGEX_GIGABIT_INTERFACE.match(interface)))\
            or (bool(not(session.query(TransitInterfaces).filter(TransitInterfaces.description == interface.lower()).first())))
        session.close()
    
    return result

def get_device_object(device):
    ''' Get a device array and returns Devices model object'''
    result = Devices(
        ip = device['ip'],
        name = device['name'],
        vendor = VendorEnum[ device['vendor'] ].value,
        serial_number = '',
        device_model = '',
        connection_type = DeviceConnectionEnum[device['protocol']].value,
        device_type = DeviceTypeEnum[device['device_type']].value,
        location = resolve_location(device['name']),
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    )
    return result

def resolve_location(name):
    ''' Resolve name location from name characters '''
    name_upper = name.upper()
    location = ''
    if ('ALM' in name_upper):
        location = "Almagro"
    elif ('BOE' in name_upper):
        location = "Boecillo"
    elif ('DC' in name_upper):
        location = "Madrid Distrito"
    elif ('GRA' in name_upper):
        location = "Granada"
    elif ("JC" in name_upper):
        location = "Julián Camarillo"
    elif ('WAL' in name_upper) or ('HUE' in name_upper):
        location = "Huesca"
    elif ('BCN' in name_upper):
        location = "Barcelona"
    else:
        location = "Sin sede"

    return location

def resolve_vendor(vendor):
    if(type(vendor) == int):
        return VendorEnum(vendor).name
    else:
        return VendorEnum[vendor.lower()].value
        


def get_devices_csv():
    ''' Returns dataframe that contains devicelist from csv '''
    try:
        df = pd.read_csv('../data/lista-switches.csv', sep=";")
        return df
    except FileNotFoundError:
        return FileNotFoundError


def format_mac_address(mac):
    ''' Transforms a mac address in AAAA.BBBB.CCCC on AA:BB:CC:DD:EE:FF format '''
    result = ""
    for text in mac.split("."):
        result += text[0:2] + ":"
        result += text[2:4] + ":"
    if ( validate_mac( result[:-1] ) ):
        return result[:-1]
    else: 
        return Exception

def validate_mac(mac):
    ''' True if valid mac address. False if not '''
    return bool(REGEX_MAC_ADDRESS.match(str(mac)))


def validate_ip(ip):
    ''' True if valid ip address. False if not '''
    return bool(REGEX_IP_ADDRESS.match(str(ip)))

class TableJSONEncoder(json.JSONEncoder):
    ''' Class to encode Juniper Views and table to return JSON object '''
    def default(self, obj):
        if isinstance(obj, View):
            obj = dict(obj.items())
        elif isinstance(obj, Table):
            obj = {item.name: item for item in obj}
        elif isinstance(obj, lxml.etree._Element):
            def recursive_dict(element):
                return element.tag, dict(map(recursive_dict, element)) \
                       or element.text
            _, obj = recursive_dict(obj)
        else:
            obj = super(TableJSONEncoder, self).default(obj)
        return obj
