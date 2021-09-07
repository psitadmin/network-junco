from management.db_data_admin import *
from management.db_tables_admin import *

def main(argv):
    if(len(argv) > 1 ):
        if(argv[1] == '0'):
            # Deleting database
            delete_db()
            print("deleting...")   
        elif(argv[1] == '1'):
            # Creating database
            print("creating database tables...")
            create_db()
        elif(argv[1] == '2'):
            # Populating enum tables
            print("populating enum previous tables...")
            PopulateDB.populate_enum_tables()
        elif(argv[1] == '3'):
            print("pushing devices from .csv")
            # Populate devices
            PopulateDB.populate_devices()
        elif(argv[1] == '4'):
            print("populating arp tables")
            PopulateDB.populate_arp_tables()
        elif(argv[1] == '5'):
            print("populating ethernet-switching tables")
            PopulateDB.populate_ethernet_switching()
        elif(argv[1] == '6'):
            print("populating interfaces tables")
            PopulateDB.populate_interfaces()
        elif(argv[1] == '7'):
            print("populating neighbors tables")
            PopulateDB.populate_neighbors()
        elif(argv[1] == 'populate_all'):
            PopulateDB.populate_enum_tables()
            PopulateDB.populate_devices()
            PopulateDB.populate_arp_tables()
            PopulateDB.populate_interfaces()
            PopulateDB.populate_ethernet_switching()
            PopulateDB.populate_neighbors()
        elif(argv[1] == 'populate_tables'):
            print("populating arp tables")
            PopulateDB.populate_arp_tables()
            print("populating ethernet-switching tables")
            PopulateDB.populate_ethernet_switching()
            print("populating interfaces tables")
            PopulateDB.populate_interfaces()
            print("populating neighbors tables")
            PopulateDB.populate_neighbors()
        else:
            print("No action selected")
    else:
        print("NO ACTION SELECTED")
    

if __name__ == "__main__":
    main(sys.argv)