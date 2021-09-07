# Connection imports
from arp_service.arp_connection import CiscoARP
from jnpr.junos.utils.config import Config
from jnpr.junos.op.phyport import PhyPortTable
from jnpr.junos import Device
from netmiko import ConnectHandler

from utilities.utils_db import resolve_vendor
from devices.devices_db import get_device_by_id, get_device_protocol, get_device_type
from properties.properties import DataBaseProps

from pprint import pprint as pp

def get_device_interfaces(device_id):
    dev = get_device_by_id(device_id)
    vendor = resolve_vendor(dev.vendor)
    int_array = []
    try:
        if(vendor == "juniper"):
            with Device(host=dev.ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_PASSWORD) as dev:
                dev.timeout = 100
                in_table = PhyPortTable(dev)
                in_table.get(interface_name='[aefgx][et]*')
                # in_table.get(interface_name='*')
                for item in in_table:
                    int_array.append( {
                        'name': item.name,
                        'status': item.admin,
                        'link': item.oper,
                        'description': str(item.description)
                    })
                dev.close()
        elif(vendor == "cisco"):
            df = CiscoARP.get_interfaces_table(dev.ip)
            for item in df.itertuples():
                int_array.append({
                    'name': item.interface,
                    'status': item.status,
                    'link': item.link,
                    'description': str(item.description)  
                })
            
        elif(vendor == "dell"):
            print(vendor)
        elif(vendor == "arista"):
            print(vendor)
            
        return int_array

    except Exception as ex:
        print ("\nException raised: {0}\n".format(ex) ) 

def post_interface_config(device_id, configs):
    device_id = get_device_by_id(device_id)
    vendor = resolve_vendor(device_id.vendor)
    device_ip = device_id.ip
    output_result = ""

    try:
        if(vendor == "juniper"):
            with Device(host=device_ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_PASSWORD) as dev:
                dev.timeout = 100
                with Config(dev, mode='private') as cu:
                    for conf in configs:
                        if('action' in conf):
                            if(conf['action'] == True):
                                act = "delete interfaces "+conf['name']+" disable"
                                cu.load(act)
                            elif(conf['action'] == False):
                                act = "set interfaces "+conf['name']+" disable"
                                cu.load(act)
                        if('description' in conf):
                            act = "set interfaces "+conf['name']+" description "+conf['description']
                            cu.load(act)
                        output_result = output_result + cu.diff()
                        cu.commit()
                dev.close()    

        elif(vendor == "cisco"):
            protocol = get_device_protocol(device_id.ip)
            typeof = get_device_type(device_id.ip)
            device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
            if (typeof == "firewall"):
                DeviceCisco = {
                    "host": device_id.ip,
                    "username": DataBaseProps.TEST_USER,
                    "password": DataBaseProps.TEST_PASSWORD,
                    "secret": DataBaseProps.TEST_PASSWORD,
                    "device_type": "cisco_asa",
                }
            else:
                device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
                DeviceCisco = {
                    "host": device_id.ip,
                    "username": DataBaseProps.TEST_USER,
                    "password": DataBaseProps.TEST_PASSWORD,
                    "device_type": device_type,
                }
            print(device_type, protocol, typeof)
        
            connect = ConnectHandler(**DeviceCisco)
            connect.enable()
            connect.config_mode()
            for conf in configs:
                connect.send_config_set("interface "+conf['name'])
                if('action' in conf):
                    output=""
                    if(conf['action'] == True):
                        command = ["interface "+conf['name'], "no shutdown"]
                        output = connect.send_config_set(command)
                    elif(conf['action'] == False):
                        command = ["interface "+conf['name'], "shutdown"]
                        output = connect.send_config_set(command)
                    output_result = output_result + output
                if('description' in conf):
                    command = ""
                    if(conf['description']==""):
                        command = ["interface "+conf['name'],"no description"]
                    else:
                        command = ["interface "+conf['name'],"description "+conf['description']]
                    output = connect.send_config_set(command)
                    output_result = output_result + output
            print(output_result)
        elif(vendor == "dell"):
            print(vendor)
        elif(vendor == "arista"):
            print(vendor)
        print("output result is ", output_result)
        return output_result
    except Exception as ex:
        print ("\nException raised: {0}\n".format(ex) )    