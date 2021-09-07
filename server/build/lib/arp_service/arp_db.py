import pandas as pd
from model.model_db import *
from properties.properties import DataBaseProps
from datetime import datetime 
from pprint import pprint as pp  

        
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