# SQLAlchemy imports
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint, text, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy

# Local modules imports
from properties.properties import DataBaseProps

import datetime
import enum

# Create engine connection
engine = create_engine(
    DataBaseProps.ENGINE_ROUTE,
    # echo=True
)
# Declaring Base
Base = declarative_base()
Base.metadata.schema = 'junco_db'
# Session class which will serve as a factory for new Session objects
Session = sessionmaker(bind=engine)


# ========================================================================
# ====== DEVICES MODEL ======
# ========================================================================
class Devices(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(17), primary_key=True, unique=True)
    name = Column(String(45))
    vendor = Column(Integer, ForeignKey("device_vendors.id"))
    serial_number = Column(String(45))
    device_model = Column(String(45))
    connection_type = Column(Integer, ForeignKey('device_connection.id'))
    location = Column(String(45))
    device_type = Column(Integer, ForeignKey('device_type.id'))
    date = Column(SQLAlchemy().DateTime)
    
    # FK Relationships
    vendor_id = relationship("DeviceVendors", foreign_keys=[vendor])
    connection_type_id = relationship("DeviceConnection", foreign_keys=[connection_type])
    device_type_id = relationship("DeviceType", foreign_keys=[device_type])
    ArpTable = relationship("ArpTable", backref="devices", cascade="all, delete")
    EthernetSwitchingTable = relationship("EthernetSwitchingTable", backref="devices", cascade="all, delete")
    InterfacesTable = relationship("InterfacesTable", backref="devices", cascade="all, delete")
    NeighborsTable = relationship("NeighborsTable", backref="devices", cascade="all, delete")
    
    def __repr__(self):
        return """<Device(id='%s', ip='%s', name='%s', vendor='%s', serial_number='%s', device_model='%s', 
        connection_type='%s', location='%s', device_type='%s', date='%s')>""" % (self.id, self.ip, self.name, 
        self.vendor, self.serial_number, self.device_model, self.connection_type, self.location, self.device_type, self.date)

class VendorEnum(enum.Enum):
    cisco = 1
    juniper = 2
    dell = 3
    arista = 4

    def return_name(value):
        if isinstance(value, int):
            return value
        return value.name
class DeviceVendors(Base):
    __tablename__ = 'device_vendors'
    id = Column(Integer, primary_key=True)
    name = Column(Enum(VendorEnum), unique=True)

    def __repr__(self):
        return "<DeviceVendor(id='%s', name='%s')>" % (self.id, self.name)

class DeviceConnectionEnum(enum.Enum):
    ssh = 1
    telnet = 2
class DeviceConnection(Base):
    __tablename__ = 'device_connection'
    id = Column(Integer, primary_key=True)
    name = Column(Enum(DeviceConnectionEnum), unique=True)

    def __repr__(self):
        return "<DeviceConnection(id='%s', name='%s')>" % (self.id, self.name)

class DeviceTypeEnum(enum.Enum):
    router = 1
    switch = 2
    firewall = 3
class DeviceType(Base):
    __tablename__ = 'device_type'
    id = Column(Integer, primary_key=True)
    name = Column(Enum(DeviceTypeEnum), unique=True)

    def __repr__(self):
        return "<DeviceType(id='%s', name='%s')>" % (self.id, self.name)


# ========================================================================
# ====== ARP MODEL ======
# ========================================================================
class ArpTable(Base):
    __tablename__ = 'arp_table'

    mac_address = Column(String(17), primary_key=True)
    ip_address = Column(String(17), primary_key=True)
    interface_name = Column(String(45))
    ip_source = Column(String(17), ForeignKey('devices.ip', ondelete='CASCADE', onupdate='CASCADE'),primary_key=True)
    date = Column(SQLAlchemy().DateTime)

    def __repr__(self):
        return "<ARPTable(mac='%s', ip='%s', interface='%s', ip_source='%s')>" % (self.mac_address, self.ip_address, 
        self.interface_name, self.ip_source)

class EthernetSwitchingTable(Base):
    __tablename__ = 'ethernet_switching_table'

    mac_address = Column(String(17), primary_key=True)
    vlan = Column(String(45), primary_key=True)
    logical_interface = Column(String(45), primary_key=True)
    ip_source = Column(String(17), ForeignKey('devices.ip', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    date = Column(SQLAlchemy().DateTime)

    def __repr__(self):
        return "<EthernetSwithcingTable(mac_address='%s', vlan='%s', logical_interface='%s', ip_source='%s')>" % (self.mac_address, 
            self.vlan, self.logical_interface, self.ip_source)

class InterfacesTable(Base):
    __tablename__ = 'interfaces_table'

    interface = Column(String(45), primary_key=True)
    description = Column(String(45))
    ip_source = Column(String(17), ForeignKey('devices.ip', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    date = Column(SQLAlchemy().DateTime)

    def __repr__(self):
        return "<InterfacesTable(interface='%s', description='%s', ip_source='%s')>" % (self.interface, self.description, 
            self.ip_source)


class NeighborsTable(Base):
    __tablename__ = 'neighbors_table'

    local_interface = Column(String(45), primary_key=True)
    device_id = Column(String(90))
    port_info = Column(String(90))
    ip_source = Column(String(17), ForeignKey('devices.ip', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    date = Column(SQLAlchemy().DateTime)

    def __repr__(self):
        return "<NeighborsTable(local_interface='%s', device_id='%s', port_info='%s', ip_source='%s')>" % (self.local_interface,
            self.device_id, self.port_info, self.ip_source)


class TransitInterfaces(Base):
    __tablename__ = 'transit_interfaces_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(20), primary_key=True, nullable=False, unique=True)
    vendor = Column(Integer, ForeignKey("device_vendors.id"), primary_key=True, nullable=False)