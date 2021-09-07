# ARP utils
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.exception import ConnectError
from jnpr.junos.op.arp import ArpTable as JunosARP
from jnpr.junos.op.elsethernetswitchingtable import ElsEthernetSwitchingTable
from jnpr.junos.op.phyport import PhyPortTable
from jnpr.junos.op.lldp import LLDPNeighborTable
from netmiko import ConnectHandler, ssh_exception, Netmiko
# Local modules
from properties.properties import DataBaseProps
from model.model_db import *
from devices.devices_db import *
from arp_service.arp_db import *

from pprint import pprint as pp
import pandas as pd
import re
import json
import sys


class JuniperARP():
    ''' JUNIPER CONNECTION UTILITY '''

    def get_arp_table(device_ip):
        ''' Connects with the device and retrieves ARP table information '''
        try:
            with Device(host=device_ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_PASSWORD) as dev:
                dev.timeout = 100
                arp_table = JunosARP(dev)
                arp_table.get(no_resolve = False)
                result_array= []
                # Filling array with arp rows
                for item in arp_table:
                    serie = [ item.mac_address, item.ip_address, item.interface_name ]
                    if(validate_mac(item.mac_address)):
                        result_array.append(serie)
                df = pd.DataFrame(result_array)
                df.columns = ['mac_address',"ip_address","interface_name"]
                dev.close()
                return df

        except ConnectionError as e:
            print ("Cannot connect to device: {0}\n".format(e))
            # sys.exit(1)
        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )
            # sys.exit(1)

    def get_ethernet_switching_table(device_ip):
        ''' Connects with device and retrieves ETHERNET-SWITCHING table information '''
        try:
            with Device(host=device_ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_PASSWORD) as dev:
                dev.timeout = 100
                es_table = ElsEthernetSwitchingTable(dev)
                es_table.get()
                result_array= []
                # Filling array with ethernet-switching rows
                for item in es_table:
                    # if (check_interface(item.logical_interface) ):
                    item.logical_interface = item.logical_interface.split(".")[0]
                    serie = [ item.mac_address, item.vlan_name, item.logical_interface ]
                    if(validate_mac(item.mac_address)):
                        result_array.append(serie)
                df = pd.DataFrame(result_array)
                df.columns = ['mac_address', "vlan_name", "logical_interface"]
                print(df.to_string())
                dev.close()
                return df

        except ConnectionError as e:
            print ("Cannot connect to device: {0}\n".format(e))
            # sys.exit(1)
        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )
            # sys.exit(1)

    def get_interfaces_table(device_ip):
        ''' Connects with device and retrieves interfaces table information '''
        try: 
            with Device(host=device_ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_PASSWORD) as dev:
                dev.timeout = 100
                in_table = PhyPortTable(dev)
                in_table.get(interface_name='*')
                result_array = []
                for item in in_table:
                    result_array.append( [item.name, item.description] )
                df = pd.DataFrame(result_array)
                df.columns = ['interface', 'description']
                dev.close()
                return df

        except ConnectionError as e:
            print ("Cannot connect to device: {0}\n".format(e))
            # sys.exit(1)
        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )
            # sys.exit(1)

    def get_neighbors_table(device_ip):
        ''' Connects with device and retrieves neighbors table information '''
        try: 
            with Device(host=device_ip, user=DataBaseProps.TEST_USER, password=DataBaseProps.TEST_PASSWORD) as dev:
                dev.timeout = 100
                ne_table = LLDPNeighborTable(dev)
                ne_table.get()
                result_array = []
                for item in ne_table:
                    result_array.append( [item.local_int, item.remote_chassis_id, item.remote_sysname] )
                df = pd.DataFrame(result_array)
                df.columns = ['local_interface', 'device_id', 'port_info']
                dev.close()
                # print(df.to_string())
                return df

        except ConnectionError as e:
            print ("Cannot connect to device: {0}\n".format(e))
            # sys.exit(1)
        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )
            # sys.exit(1)


class CiscoARP():
    ''' CISCO CONNECTION UTILITY '''

    def get_arp_table(device_ip):
        # Get device props
        protocol = get_device_protocol(device_ip)
        typeof = get_device_type(device_ip)
        device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
        Device = {}
        print(typeof, device_type, device_ip)
        if (typeof == "firewall"):
            Device = {
                "host": device_ip,
                "username": DataBaseProps.TEST_USER,
                "password": DataBaseProps.TEST_PASSWORD,
                "secret": DataBaseProps.TEST_PASSWORD,
                "device_type": "cisco_asa",
            }
        else:
            device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
            Device = {
                "host": device_ip,
                "username": DataBaseProps.TEST_USER,
                "password": DataBaseProps.TEST_PASSWORD,
                "device_type": device_type,
            }
        result_array = []
            
        try:
            connect = ConnectHandler(**Device)
            connect.enable()
            arp_table = connect.send_command("show arp")
            # Executing command on remote device
            connect = ConnectHandler(**Device)
            connect.enable()
            if(device_ip == "10.95.245.91"):
                connect.send_command("changeto context DCO2-C02-FWC1")
            arp_table = connect.send_command("show arp")
            connect.disconnect()
            # FIREWALL CASE
            if (typeof == "firewall"):
                for line in arp_table.split("\n"):
                    serie = line.split()
                    if (len(serie) == 4):
                        new_serie = [ format_mac_address(serie[2]), serie[1], serie[0] ]
                        result_array.append(new_serie)
                    else:
                        print("FALLO", line)
            # ROUTER AND SWITCH CASE
            else:
                # Parsing text to make a dataframe
                for line in arp_table.split("\n")[1:]:
                    serie = line.split()
                    if( (len(serie) > 1) and (serie[3] != 'Incomplete') ):
                        serie.pop(0)
                        serie.pop(1)
                        serie.pop(2)
                        # If there are more unnecesary fields...
                        if( len(serie) > 3 ):
                            if( ('Vl' in serie) and ( serie.index('Vl') == 2 ) ):
                                serie.pop(2)
                                if (validate_mac(serie[1])):
                                    new_serie = [ serie[1], serie[0], "Vlan"+serie[2] ]
                                    result_array.append(new_serie)
                                elif(validate_mac( format_mac_address(serie[1]) )):
                                    new_serie = [ format_mac_address(serie[1]), serie[0], "Vlan"+serie[2] ]
                                    result_array.append(new_serie)
                            elif( ('Vl' in serie) and ( serie.index('Vl') == 3 ) ):
                                serie.pop(2)
                                serie.pop(2)
                                if (validate_mac(serie[1])):
                                    new_serie = [ serie[1], serie[0], "Vlan"+serie[2] ]
                                    result_array.append(new_serie)
                                elif(validate_mac( format_mac_address(serie[1]) )):
                                    new_serie = [ format_mac_address(serie[1]), serie[0], "Vlan"+serie[2] ]
                                    result_array.append(new_serie)
                            # serie.pop(3)
                        else:
                            if (validate_mac(serie[1])):
                                new_serie = [ serie[1], serie[0], serie[2] ]
                                result_array.append(new_serie)
                            elif(validate_mac( format_mac_address(serie[1]) )):
                                new_serie = [ format_mac_address(serie[1]), serie[0], serie[2] ]
                                result_array.append(new_serie)
                            else:
                                print( "ERROR EN LA MAC ", serie[1])
                    else:
                        print("SERIE QUE ROMPE => ", serie)
                        
            df = pd.DataFrame(result_array)
            df.columns = ['mac_address',"ip_address","interface_name"]
            return df

        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )

    def get_ethernet_switching_table(device_ip):
        # Get Device props
        protocol = get_device_protocol(device_ip)

        device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
        print(device_type, device_ip)
        Device = {
            "host": device_ip,
            "username": DataBaseProps.TEST_USER,
            "password": DataBaseProps.TEST_PASSWORD,
            "device_type": device_type,
        }
        result_array = []
        
        try:    
            # Executing command on remote device
            connect = ConnectHandler(**Device)
            connect.enable()
            es_table = connect.send_command("show mac-address-table")
            if ('Invalid input detected') in es_table:
                es_table = connect.send_command("show mac address-table")
            connect.disconnect()

            # Parsing text to make a dataframe
            for line in es_table.split("\n")[3:]:
                serie = line.split()
                # print(serie)
                if (len(serie) == 4):
                    # print( ( serie ) )
                    new_serie = [ format_mac_address(serie[1]), serie[0], serie[3]]
                    if(validate_mac( format_mac_address(serie[1]) )):
                        result_array.append(new_serie)
                    else:
                        print( "ERROR EN LA MAC ", serie[1])
                elif (len(serie) == 5):
                    # print( ( serie ) )
                    new_serie = [ format_mac_address(serie[1]), serie[0], serie[4]]
                    if(validate_mac( format_mac_address(serie[1]) )):
                        result_array.append(new_serie)
                    else:
                        print( "ERROR EN LA MAC ", serie[1])
                elif (len(serie) == 6):
                    # print( ( serie ) )
                    # Special case with formatted mac address
                    if( validate_mac(serie[1]) ):
                        new_serie = [ serie[1], serie[0], serie[3]+serie[4] ]
                    else:
                        new_serie = [ format_mac_address(serie[2]), serie[1], serie[5]]
                    result_array.append(new_serie)
                else:
                    print("SERIE QUE ROMPE => ", serie)

            df = pd.DataFrame(result_array)
            df.columns = ['mac_address', "vlan_name", "logical_interface"]
            
            return df

        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )

    def get_interfaces_table(device_ip):
        ''' Connects with device and retrieves interfaces table information '''
        # Get Device props
        protocol = get_device_protocol(device_ip)
        device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
        print(device_type, device_ip)
        Device = {
            "host": device_ip,
            "username": DataBaseProps.TEST_USER,
            "password": DataBaseProps.TEST_PASSWORD,
            "device_type": device_type,
        }
        result_array = []
        
        try:    
            # Executing command on remote device
            connect = ConnectHandler(**Device)
            connect.enable()
            in_table = connect.send_command("show interfaces description")
            connect.disconnect()

            # Parsing text to make a dataframe
            for line in in_table.split("\n")[1:]:
                serie = line.split()
                inter = serie[0]
                if(len(serie) == 3):
                    result_array.append( [inter, ""] )
                elif(len(serie) == 4):
                    result_array.append( [inter, serie[3] ] )
                elif(len(serie) > 4):
                    # print("\nSERIE CON LONG = ", len(serie))
                    name = ""
                    if(serie[1] == "admin"):
                        serie.pop(1)
                    for x in range(3, (len(serie))):
                        name = name + " " + (serie[x])
                    result_array.append( [inter, name])
                else:
                    print("SERIE QUE ROMPE => ", serie)
            
            df = pd.DataFrame(result_array)
            df.columns = ['interface', 'description']
            return df

        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )

    def get_neighbors_table(device_ip):
        ''' Connects with device and retrieves neighbors table information '''
        # Get Device props
        protocol = get_device_protocol(device_ip)
        device_type = "cisco_ios" if (protocol == "ssh") else "cisco_ios_telnet"
        print(device_type, device_ip)
        Device = {
            "host": device_ip,
            "username": DataBaseProps.TEST_USER,
            "password": DataBaseProps.TEST_PASSWORD,
            "device_type": device_type,
        }
        result_array = []
        
        try:
            # Executing command on remote device
            connect = ConnectHandler(**Device)
            connect.enable()

            error = "invalid input detected at '^' marker"
            # LLDP NEIGHBORS
            lldp_table = connect.send_command("show lldp neighbors")
            if (error not in lldp_table.lower()):
                # Parsing text to make a dataframe
                # print("LONGITUD = ",lldp_table.split("\n")[len(lldp_table.split("\n"))-2])
                for line in lldp_table.split("\n")[5:(len(lldp_table.split("\n"))-3)]:
                    serie = line.split()
                    if(serie[0] == 'Device' or len(serie) == 0):
                        continue
                    result_array.append([serie[1], serie[len(serie)-1], serie[0]])

            # LLDP NEIGHBORS
            cdp_table = connect.send_command("show cdp neighbors")
            try:
                if (error not in cdp_table.lower()):
                    # Parsing text to make a dataframe
                    table = cdp_table.split("\n")[4:]
                    # print("LONGITUD = ",len(table))
                    
                    for line in range ( len(table) ):
                        # print("LINEA = ", table[line], len(table[line]))
                        if line is not None:
                            serie = table[line].split()
                            # print("(",line,") serie ", serie, " con long ", len(serie))
                            if( len(serie) < 1 or ('cdp entries' in table[line]) or serie[0] == 'Device' ):
                                # print("cabecera")
                                continue
                            if(len(serie) == 1):
                                # print("solo nombre")
                                # print("long de la linea = 1", table[line].split())
                                continue
                            else:
                                if(line > 0 and len(table[line-1].split()) == 1):
                                    # print("siguiente al nombre",[serie[0]+serie[1], serie[len(serie)-2]+serie[len(serie)-1], table[line-1]])
                                    result_array.append([serie[0]+serie[1], serie[len(serie)-2]+serie[len(serie)-1], table[line-1]])
                                else:
                                    # print("linea normal", [serie[1]+serie[2], serie[len(serie)-2]+serie[len(serie)-1], serie[0]])
                                    result_array.append([serie[1]+serie[2], serie[len(serie)-2]+serie[len(serie)-1], serie[0]])
            except Exception:
                print("EXC = ", Exception)

            connect.disconnect()
            if(result_array):
                df = pd.DataFrame(result_array)
                df.columns = ['local_interface', 'device_id', 'port_info']
                # pp(df.to_string())
                return df

        except ConnectionError as e:
            print ("Cannot connect to device: {0}\n".format(e))
            # sys.exit(1)
        except Exception as ex:
            print ("\nException raised: {0}\n".format(ex) )
            # sys.exit(1)