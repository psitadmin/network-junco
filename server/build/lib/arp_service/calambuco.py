# SQLAlchemy imports
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint, text, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint as pp
import socket

# Local modules imports
from model.model_db import *
from properties.properties import DataBaseProps
from devices.devices_db import get_routers, get_switches
from utilities.utils_db import check_interface, validate_ip, validate_mac

import json
import datetime
import enum


def search_calambuco(value):
    ''' Detects if value is an IP Addres or MAC Address. Raises an exception if neither '''
    # TODO: función utility que vea si es mac, address o qué. Que recorte espacios también
    v = value.split()[0]
    result = {}
    if(validate_ip(v) ):
        result = router_find_by_ip(v)
    elif(validate_mac(v) ):
        result = router_find_by_mac(v)
    else:
        result = False
    return result

def router_find_by_ip(device_ip):
    ''' Starts IP's MAC address search on routers ARP tables fetching IP on tables'''
    with Session() as session:
        # Finds IP on all router's ARP table
        result = session.query(ArpTable).filter(ArpTable.ip_address == device_ip).all()
        # print("router_find_by_ip result = ",result)
        session.close()
        if (len(result) > 0):
            result_array = switch_loop_search(result[0].mac_address)
            return build_json_calambuco(result[0], result_array)
        else:
            return False

def router_find_by_mac(mac_address):
    ''' Starts IP's MAC address search on routers ARP tables fetching MAC Address on tables'''
    with Session() as session:
        # Finds MAC on all router's ARP table
        result = session.query(ArpTable).filter(ArpTable.mac_address == mac_address).all()
        session.close()
        if (len(result) > 0):
            result_array = switch_loop_search(result[0].mac_address)
            return build_json_calambuco(result[0], result_array)
        else:
            print("NO ENCONTRADA MAC ", mac_address)
            session.close()
            return False

def switch_loop_search(mac_address):
    ''' Search MAC address on switches recursively. Returns MAC Address data from physical device that contains the direction '''
    with Session() as session:
        # print("\nBuscando con la mac", mac_address)
        # Getting switches matches with MAC address
        devices = session.query(EthernetSwitchingTable, Devices)\
            .filter(EthernetSwitchingTable.mac_address == mac_address)\
            .filter(EthernetSwitchingTable.ip_source == Devices.ip)\
            .filter(Devices.device_type == DeviceTypeEnum.switch.value)\
            .all()
        result = []
        # If only finds single device, that's the final one
        if(len(devices) == 1):
            result.append(devices[0])
        # If not, we need to discard non-final device
        else:
            # Finds final addresses on query result
            for dev in devices:
                # Check if interface is an end-point interface
                print("DISPOSITIVO ", dev.Devices.ip, dev.Devices.name, dev.EthernetSwitchingTable.logical_interface)
                if ( check_interface( dev.EthernetSwitchingTable.logical_interface ) ):
                # if ( ( dev.EthernetSwitchingTable.logical_interface ) ):
                    neighbors = session.query(EthernetSwitchingTable, NeighborsTable)\
                        .filter(EthernetSwitchingTable.ip_source == dev.Devices.ip)\
                        .filter(EthernetSwitchingTable.mac_address == mac_address)\
                        .filter(EthernetSwitchingTable.logical_interface == NeighborsTable.local_interface)\
                        .filter(NeighborsTable.ip_source == dev.Devices.ip)\
                        .first()
                    # Checks if device has any connection with others
                    if(neighbors is not None):
                        print("\n\n Neighbors = ", neighbors)
                        neighbor_result = neighbors.NeighborsTable.port_info
                        # interface_result = 

                        device_result = session.query(Devices).filter(Devices.name.like(neighbor_result.split(".", 1)[0])).all()
                        
                        
                        print("DEVICES = ",device_result)
                        if(device_result):
                            print("El resultado es OTRO DISPOSITIVO", device_result)
                        else:
                            print("El resultado es un dispositivo final" , neighbor_result, dev)
                            result.append(dev)
                    else:
                        print ("no tiene vencino todavía")
                        result.append(dev)
                else:
                    print("NO ES => ",dev.EthernetSwitchingTable.ip_source)

        session.close()
        return result


def build_json_calambuco(device_found, devices_result):
    ''' Get the device finded by IP or MAC address and devices where MAC found and return a JSON with them '''
    # print("\nDispositivo buscado: {0}\nDispositivos donde lo encuentran: {1}\n\n".format(device_found,devices_result))
    addresses = []
    nslookup = ''
    try:
        nslookup = socket.gethostbyaddr(device_found.ip_address)[0]
    except:
        nslookup = '------'
    result = {
        'device_found': [{
            'mac': device_found.mac_address,
            'ip': device_found.ip_address,
            'name': nslookup,
            'date': device_found.date.strftime('%Y-%m-%d %H:%M:%S'),
        }]
    }
    session = Session()
    for i in range( len(devices_result) ):
        inter = session.query(InterfacesTable)\
            .filter(InterfacesTable.ip_source == devices_result[i].Devices.ip)\
            .filter(InterfacesTable.interface == devices_result[i].EthernetSwitchingTable.logical_interface)\
            .first()
        
        interface = ""
        if(inter):
            interface = inter.description
        else:
            interface = "------"
            
        direction = {
            'device_name': devices_result[i].Devices.name,
            'ip': devices_result[i].Devices.ip,
            'vendor': VendorEnum(devices_result[i].Devices.vendor).name,
            'interface': devices_result[i].EthernetSwitchingTable.logical_interface,
            'interface_description': interface,
            'vlan': devices_result[i].EthernetSwitchingTable.vlan,
            'date': devices_result[i].EthernetSwitchingTable.date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        addresses.append(direction)
    
    session.close()
    result["addresses"] = addresses 
    return result
    