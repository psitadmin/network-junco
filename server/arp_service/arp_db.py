import pandas as pd
from model.model_db import *
from datetime import datetime 
from pprint import pprint as pp  
import json

        
def save_arp_table(device_ip, df_table):
    ''' Push received device arp table to database'''
    with Session() as session:
        # arp_objects = []
        try:
            for index, row in df_table.iterrows():
                arp_row = ArpTable(
                    mac_address = row['mac_address'],
                    ip_address = row['ip_address'],
                    interface_name = row['interface_name'],
                    ip_source = device_ip,
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                session.merge(arp_row)
                # print(arp_row)
                session.commit()
        except Exception as e:
            print("EXCEPTION on save_arp_table => ", e)
                
        session.close()

def save_ethernet_switching_table(device_ip, df_table):
    ''' Push received device ethernet-switching table to database'''
    with Session() as session:
        try:
            es_objects = []
            for index, row in df_table.iterrows():
                es_row = EthernetSwitchingTable(
                    mac_address = row['mac_address'],
                    vlan = row['vlan_name'],
                    logical_interface = row['logical_interface'],
                    ip_source = device_ip,
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                session.merge(es_row)
                # print(es_row)
                session.commit()
            
        except Exception as e:
            print("EXCEPTION on save_ethernet_switching_table => ", e)
                
        session.close()


def save_interfaces_table(device_ip, in_table):
    ''' Push received device interfaces table to database'''
    with Session() as session:
        try:
            for index, row in in_table.iterrows():
                in_row = InterfacesTable(
                    interface = row['interface'],
                    description = row['description'],
                    ip_source = device_ip,
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                session.merge(in_row)
                # print(in_row)
                session.commit()

        except Exception as e:
            print("EXCEPTION on save_interfaces_table => ", e)

        session.close()

def save_neighbors_table(device_ip, ne_table):
    ''' Push received device neighbors table to database'''
    with Session() as session:
        try:
            for index, row in ne_table.iterrows():
                in_row = NeighborsTable(
                    local_interface = row['local_interface'],
                    device_id = row['device_id'],
                    port_info = row['port_info'],
                    ip_source = device_ip,
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                session.merge(in_row)
                # print(in_row)
                session.commit()

        except Exception as e:
            print("EXCEPTION on save_interfaces_table => ", e)

        session.close()

def get_transit_interfaces():
    ''' Returns transit interfaces table '''
    result = []
    with Session() as session:
        for id, int, vend in session.query(TransitInterfaces.id, TransitInterfaces.description, DeviceVendors.name)\
            .join(DeviceVendors).filter(DeviceVendors.id == TransitInterfaces.vendor).all():
            data = {
                'id': id,
                'transit_interface': int,
                'vendor': vend.name,
            }
            result.append(data)
        return result

def transit_interfaces_controller(new_int, delete_int, edit_int):
    response = ""
    with Session() as session:
        if(new_int):
            response += "Added: "
            for i in new_int:
                int_to_add = TransitInterfaces(
                    description = i['transit_interface'].lower(),
                    vendor = VendorEnum[ i['vendor'] ].value
                )
                session.merge(int_to_add)
                response += str(i) + ";"
            session.commit()
        if(delete_int):
            response += "Deleted: "
            for i in delete_int:
                session.query(TransitInterfaces).filter(TransitInterfaces.id == i['id']).delete()
                response += str(i) + ";"
            session.commit()
        if(edit_int):
            response += "Modified: "
            for i in edit_int:
                int = session.query(TransitInterfaces).filter(TransitInterfaces.id == i['id']).first()
                int.description = i['transit_interface'].lower()
                int.vendor = VendorEnum[i['vendor']].value
                response += str(i) + ";"
            session.commit()
        session.close()
    return response