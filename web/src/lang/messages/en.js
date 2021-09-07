export default{
  global: {
    helloMessage: 'Welcome to Junco',
    loadingText: 'Loading... Please wait',
    selectAnOption: 'Select an option',
    seeConfig: 'See configuration',
    add: 'Add',
    applyConfig: 'Apply configuration',
    apply: 'Apply',
    searchLabel: 'Search',
    searchMessage: 'Input text to filter:',
    refresh: 'Refresh',
    confirm: 'Confirm',
    cancel: 'Cancel',
    parameter: 'Parameter',
    value: 'Value',
    requiredField: 'Required Field',
    invalidIP: 'Invalid IP',
    clear: 'Clear',
    delete: 'Delete',
  },
  about: {
    juncoInfo1: "Junco is a network devices connection, remote configurations push and net utilities application",
    juncoInfo2_1: "This application was developed with",
    juncoInfo2_2: "to Network team.",
    juncoInfo3: "For more information please contact ",
    juncoInfo4: "Proyect repository code available in: ",
  },
  alerts: {
    successApply: 'Configuration has been applied successfully.',
    successLoadingItems: 'Success! Items have been loaded successfully.',
    successAddingItem: 'Success! Device has been added successfully.',
    successDeletingItem: 'Success! Device/s have been deleted successfully.',
    successEditingItem: 'Success! Device has been edited successfully.',
  },
  errors: {
    invalidForm: 'Invalid form. Check errors and try again.',
    databaseError: 'Error: can\'t connect with DataBase',
    deviceConnectionError: 'Error: can\'t connect with device',
    applyError: 'Error applying configurations',
    noChangesError: 'Error: no changes detected',
  },
  headers: {
    about: 'About this page',
    logout: 'Logout',
    languageSelector: 'Select language'
  },
  menuBar: {
    configlets: 'Configlets',
    junosDevices: 'Junos devices',
    arpTables: 'ARP Search',
    allDevices: 'All devices',
  },
  login: {
    userLabel: 'User',
    passwordLabel: 'Password',
    userMessage: 'Enter your username',
    passwordMessage: 'Enter your password',
    loginError: 'User name or password is incorrect',
    loginEmpty: 'User name and password must not be empty',
    loginMessage: 'Login',
  },
  tasks: {
    selectTask: 'Please, select one available task from the list',
    interfacesTask: {
      info: 'Those are the device\'s interfaces. Please, click on a field to change it. To finish, press ',
      name: 'Name',
      status: 'Status',
      link: 'Link',
      signal: 'Signal',
      action: 'Action',
      description: 'Description',
      headerText: 'Applying changes...',
      hint: 'Change desired parameters and press ',
      bodyText: 'Are you sure to apply changes on these interfaces?',
    },
  },
  configlet: {
    messageConfiglet: 'Select an available configlet to apply on a device',
    applicableDevices: 'Select device/s to apply configlet',
    validateConfiglet: 'Validate configlets',
    confirmApply: "Are you sure to apply these configurations?",
    validatingConfigletError: 'Validate configlet error',
    applySuccess: "Configlet apply success!",
    applyError: "Error applying configlet to device/s",
    configletComp: {
      messageButton: 'Apply configlets',
      showDefault: 'Show default configlets',
      headers: {
        nameHeader: "Name",
        idHeader: "ID",
        osVersion: "OS Version",  
        platform: "Platform",
        domainHeader: "Domain",
        deviceTypeHeader: "Device type",
        descriptionHeader: "Description",
        execTypeHeader: "Execution type",
        creationHeader: "Creation date",
        updateHeader: "Last update",
        modifiedHeader: "Modified by",
      },
    }
  },
  devices: {
    messageDevice: 'Select an available device from list',
    applicableConfiglets: 'Select applicable configlet/s from list',
    deviceComp: {
      addDevice: 'Add device',
      editDevice: 'Edit device',
      deleteDevice: 'Delete device/s',
      headers: {
        statusHeader: "Status",
        nameHeader: "Name",
        ipHeader: "IP",
        vendorHeader: "Vendor",
        serialNumberHeader: "Serial number",
        platformHeader: "Platform",
        idHeader: "ID",
        osVersionHeader: "OS version",
        protocol: "Protocol",
        location: "Location",
        deviceType: "Device type",
        date: "Date",
        net: "Net",
        interface: 'Interface',
        interfaceDescription: 'Interface description',
      },
      cards: {
        deleteTitle: "Confirm action:",
        deleteText: "Are you sure you want to delete this items?",
        addTitle: 'Add device:',
        addText: 'Write device parameters and press "Confirm"',
        nameHint: 'location-site-function-vendor',
        nameRule: 'Max 25 characters',
        applyTitle: "Confirm application",
        applyText: "Do you want to apply configlet on these devices?",
      }
    },
  },
  alldevices: {

  },
  arpTables: {
    messageARP: 'ARP tables',
    arpSearch: 'Please, input an IP or MAC in order to get MAC address',
    arpInput: 'IP, MAC or device',
    arpNotFound: 'Can\'t found IP or MAC address with this params. Please, try again.',
    arpInvalid: 'Invalid IP or MAC address format.',
    arpEmpty1: 'ARP register found',
    arpEmpty2: ' but valid result not exist',
    arpComp: {
      findData: 'Finding by: ',
      result: 'Found on following devices:',
      headers: {
        ip: 'IP',
        vlan: 'VLAN',
        mac: 'MAC',
        name: 'Name',
        network: 'Network',
        date: 'Date',
        vendor: 'Vendor',
        device: 'Device',
        interface: 'Interfaz',
        interfaceDescription: 'Descripción Interfaz',
      }
    },
    arpConf: {
      transitInterfacesConf: {
        headerMessage: 'Edit transit interfaces',
        transitInterface: 'Transit interface',
        transitInterfaces: 'Transit interfaces',
        error: 'Error: unable to get transit interfaces.',
      }
    }
  }
}
