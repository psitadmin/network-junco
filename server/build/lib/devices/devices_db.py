from utilities.utils_db import *
from model.model_db import *
from properties.properties import DataBaseProps
from jnpr.junos.utils.start_shell import StartShell
from datetime import datetime   
import json


def get_all_devices():
    ''' Returns query object with all devices '''
    with Session() as session:
        devices = session.query(Devices.id.label("id"), Devices.ip.label("ip"), Devices.name.label("name"), DeviceVendors.name.label("vendor"),\
                    DeviceType.name.label("device_type")).join(DeviceVendors).join(DeviceType)\
                    .filter(DeviceVendors.id == Devices.vendor)\
                    .filter(Devices.device_type == DeviceType.id).order_by(Devices.id)
        session.close()
        return devices

def get_routers():
    ''' Returns an array with only router devices '''
    with Session() as session:
        # Get all routers from database
        routers = session.query(Devices.id.label("id"), Devices.ip.label("ip"), Devices.name.label("name"),
            DeviceVendors.name.label('vendor'), DeviceType.name.label("device_type")).join(DeviceVendors).join(DeviceType)\
            .filter(Devices.device_type == DeviceType.id).filter(DeviceType.name == 'router')\
            .filter(DeviceVendors.id == Devices.vendor).all()
        session.close()
        # Find IP on all router's ARP table  
        return routers


def get_switches():
    ''' Returns an array with only switches devices '''
    with Session() as session:
        # Get all switches from database
        switches = session.query(Devices.id.label("id"), Devices.ip.label("ip"), Devices.name.label("name"),
            DeviceVendors.name.label('vendor'), DeviceType.name.label("device_type")).join(DeviceVendors).join(DeviceType)\
            .filter(Devices.device_type == DeviceType.id).filter(DeviceType.name == 'switch')\
            .filter(DeviceVendors.id == Devices.vendor).all()    
        session.close()
        # Find IP on all router's ARP table  
        return switches


def get_device_by_ip(device_ip):
    ''' Returns device that matchs ip param '''
    with Session() as session:
        return session.query(Devices).filter(Devices.ip == device_ip).first()


def get_device_protocol(device_ip):
    ''' Returns device protocol connection '''
    with Session() as session:
        dev =  session.query(Devices, DeviceConnection.name.label("protocol")).filter(Devices.connection_type == DeviceConnection.id)\
            .filter(Devices.ip == device_ip).first()
        session.close()
        return dev.protocol.name

def get_device_type(device_ip):
    ''' Returns device type that matchs ip param '''
    with Session() as session:
        dev = session.query(Devices, DeviceType.name.label("typeof")).filter(Devices.device_type == DeviceType.id)\
            .filter(Devices.ip == device_ip).first()
        session.close()
        return dev.typeof.name

# ===============================================
#   CRUD OPERATIONS TO DEVICES
# ===============================================
def get_devices_json():
    '''Return JSON with all avaliable devices from database'''

    session = Session()
    json_result = []
    # Executing query and iter devices
    for dev, vend, dev_type, proto in session.query(Devices, DeviceVendors, DeviceType, DeviceConnection).\
        filter(Devices.vendor == DeviceVendors.id).\
        filter(Devices.device_type == DeviceType.id).\
        filter(Devices.connection_type == DeviceConnection.id).\
        order_by(Devices.id):

        # Creating JSON item
        data = {
            'id' : dev.id,
            'ip' : dev.ip,
            'name' : dev.name,
            'vendor' : vend.name.name,
            'serial_number' : dev.serial_number,
            'device_model' : dev.device_model,
            'protocol' : proto.name.name,
            'location' : dev.location,
            'device_type' : dev_type.name.name,
            'date' : dev.date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        # Appends JSON item on JSON object
        json_result.append( json.dumps(data) )
    session.close()
    
    # Returns JSON with all devices
    return json_result


def get_devices_array():
    '''Return array with all avaliable devices from database'''

    session = Session()
    array_result = []

    # Executing query and iter devices
    for dev, vend, dev_type, proto in session.query(Devices, DeviceVendors, DeviceType, DeviceConnection).\
        filter(Devices.vendor == DeviceVendors.id).\
        filter(Devices.device_type == DeviceType.id).\
        filter(Devices.connection_type == DeviceConnection.id).\
        order_by(Devices.id):

        # Creating array item
        device_row = []
        # Write every device row
        device_row.append(dev.id)
        device_row.append(dev.ip)
        device_row.append(dev.name)
        device_row.append(vend.name.name)
        device_row.append(dev.serial_number)
        device_row.append(dev.device_model)
        device_row.append(proto.name.name)
        device_row.append(dev.location)
        device_row.append(dev_type.name.name)
        device_row.append(dev.date.strftime('%Y-%m-%d %H:%M:%S'))
        # Builds the device row
        array_result.append( device_row )
    session.close()

    # Returns array with all devices
    return array_result

def get_devices_args(*argv):
    ''' Get an array with argv device params only '''


def delete_devices(device_ids):
    '''Delete devices which IDs are on "device_ids" '''
    
    session = Session()
    # Executing loop for every id
    for i in device_ids:
        session.query(Devices).filter(Devices.id == i).delete()
        
    session.commit()
    session.close()


def add_device(device):
    '''Add received device to database'''
    
    with Session() as session:    
        dev = get_device_object(device)
        # Executing query
        session.add(dev)
        session.commit()
        session.close()


def edit_device(device):
    '''Edit received device and update database'''
    print("DEVICE = ", device)
    with Session() as session:
        # Retrieves device
        dev = session.query(Devices).filter(Devices.id == device['id']).first()
        # Updating device object with new params
        dev.ip = device['ip']
        dev.name = device['name']
        dev.vendor = VendorEnum[ device['vendor'] ].value
        dev.device_type = DeviceTypeEnum[ device['device_type'] ].value
        dev.connection_type = DeviceConnectionEnum[ device['protocol'] ].value
        dev.location = resolve_location(device['name'])
        
        # Apply changes on device params
        session.commit()
        session.close()


# ===============================================
#   OTHER TABLES (ENUM)
# ===============================================
def get_vendors():
    '''Returns an array with all vendors'''
    with Session() as session:
        # Executing query to fetch all vendors
        result = []
        for vendor in VendorEnum:
            result.append(vendor.name)
    # Returns all vendor list   
    return result
    session.close()


def get_protocols():
    ''' Returns an array with all protocols'''
    with Session() as session:
        # Executing query to fetch all vendors
        result = []
        for connection in DeviceConnectionEnum:
            result.append(connection.name)
    # Returns all vendor list   
    return result
    session.close()


def get_device_types():
    ''' Returns an array with all device types '''
    with Session() as session:
        # Executing query to fetch all vendors
        result = []
        for dev_type in DeviceTypeEnum:
            result.append(dev_type.name)
    # Returns all vendor list   
    return result
    session.close()

