export default {
  global: {
    helloMessage: 'Bienvenido a Junco',
    loadingText: 'Cargando... Espere, por favor',
    selectAnOption: 'Seleccione una opción',
    seeConfig: 'Ver configuración',
    add: 'Añadir',
    applyConfig: 'Aplicar configuración',
    apply: 'Aplicar',
    searchLabel: 'Buscar',
    searchMessage: 'Introduzca texto para filtrar',
    refresh: 'Recargar',
    confirm: 'Confirmar',
    cancel: 'Cancelar',
    parameter: 'Parámetro',
    value: 'Valor',
    requiredField: 'Campo requerido',
    invalidIP: 'IP no válida',
    clear: 'Limpiar',
    delete: 'Borrar',
  },
  about: {
    juncoInfo1: "Junco es una herramienta web para la conexión, aplicación de configuraciones remotas y otras utilidaes sobre los equipos de red de Network.",
    juncoInfo2_1: "Esta aplicación ha sido desarrollada con el framework ",
    juncoInfo2_2: "para el equipo de Network.",
    juncoInfo3: "Para más información, contactar con ",
    juncoInfo4: "El repositorio del código se puede encontrar en: ",
  },
  alerts: {
    successApply: 'Configuración/es aplicada con éxito',
    successLoadingItems: 'Elementos cargados con éxito.',
    successAddingItem: 'Elemento añadido con éxito.',
    successDeletingItem: 'Elementos/s eliminado/s con éxito.',
    successEditingItem: 'Elemento editado con éxito.',
  },
  errors: {
    invalidForm: 'Campos incorrectos. Compruebe e inténtelo de nuevo.',
    databaseError: 'Error al conectar con la base de datos',
    deviceConnectionError: 'Error al conectar con el dispositivo',
    applyError: 'Error al aplicar configuraciones',
    noChangesError: 'Error: no se han detectado cambios',
  },
  headers: {
    about: 'Sobre esta página',
    logout: 'Cerrar sesión',
    languageSelector: "Seleccionar idioma"
  },
  menuBar: {
    configlets: 'Configlets',
    junosDevices: 'Dispositivos Juniper',
    arpTables: 'Búsqueda ARP',
    allDevices: 'Todos los dispositivos',
  },
  login: {
    userLabel: 'Usuario',
    passwordLabel: 'Contraseña',
    userMessage: 'Introduzca su usuario',
    passwordMessage: 'Introduzca su contraseña',
    loginError: 'Nombre de usuario o contraseña incorrectos',
    loginEmpty: 'El nombre de usuario y la contraseña no deben estar vacíos',
    loginMessage: 'Iniciar sesión',
  },
  tasks: {
    selectTask: 'Por favor, seleccione una de las tareas disponibles',
    interfacesTask: {
      info: 'Aquí se muestran las interfaces del dispositivo. Haga click sobre un campo para editarlo y haga click en ',
      name: 'Nombre',
      status: 'Estado',
      link: 'Enlace',
      signal: 'Señal',
      action: 'Acción',
      description: 'Descripción',
      headerText: 'Aplicar cambios en interfaces',
      hint: 'Edite los parámetros deseados y pulse ',
      bodyText: '¿Desea aplicar los cambios mostrados en las siguientes interfaces?',
    },
  },
  configlet: {
    messageConfiglet: 'Seleccione el configlet que desee aplicar',
    applicableDevices: 'Seleccione uno o varios dispositivos para aplicar el configlet',
    validateConfiglet: 'Validar configlets',
    confirmApply: "¿Está seguro que desea aplicar estos configlets?",
    validatingConfigletError: 'Error al validar configlet',
    applySuccess: "¡Configlet aplicados correctamente!",
    applyError: "Error al aplicar configlet",
    configletComp: {
      showDefault: 'Mostrar configlets por defecto',
      messageButton: 'Aplicar configlets',
      headers: {
        nameHeader: "Nombre",
        idHeader: "ID",
        osVersion: "Version OS",  
        platform: "Plataforma",
        domainHeader: "Dominio",
        deviceTypeHeader: "Tipos de dispositivos",
        descriptionHeader: "Descripción",
        execTypeHeader: "Tipo de ejecución",
        creationHeader: "Fecha de creación",
        updateHeader: "Última actualización",
        modifiedHeader: "Modificado por",
      },
    },
  },
  devices: {
    messageDevice: 'Seleccione un dispositivo de la lista',
    applicableConfiglets: 'Seleccione uno o más configlets de la lista',
    deviceComp: {
      addDevice: 'Añadir dispositivo',
      editDevice: 'Editar dispositivo',
      deleteDevice: 'Eliminar disposivo/s',
      headers: {
        statusHeader: "Estado",
        nameHeader: "Nombre",
        ipHeader: "IP",
        vendorHeader: "Fabricante",
        serialNumberHeader: "Nº de serie",
        platformHeader: "Plataforma",
        idHeader: "ID",
        osVersionHeader: "Versión de SO",
        protocol: "Protocolo",
        location: "Sede",
        deviceType: "Tipo de dispositivo",
        date: "Fecha",
        net: "Red",
        interface: 'Interfaz',
        interfaceDescription: 'Descripción Interfaz',
      },
      cards: {
        deleteTitle: "Confirmar acción:",
        deleteText: "¿Seguro que desea eliminar los siguientes elementos?",
        addTitle: 'Añadir dispositivo:',
        addText: 'Escriba los parámetros del dispositivo y pulse "Confirmar"',
        nameHint: 'sede-ubicacion-funcion-marca',
        nameRule: 'Máximo 25 caracteres',
        applyTitle: "Confirmar aplicación",
        applyText: "Desea aplicar la configuración a los siguientes dispositivos",
      }
    }
  },
  arpTables: {
    messageARP: 'Tablas ARP',
    arpSearch: 'Por favor, introduzca una IP o dirección MAC para obtener la dirección MAC',
    arpInput: 'IP, máquina o MAC',
    arpNotFound: 'No se ha encontrado una dirección con estos parámetros.',
    arpEmpty1: 'Se ha encontrado un registro ARP',
    arpEmpty2: ' pero no se ha encontrado un resultado final',
    arpInvalid: 'Dirección IP o MAC incorrectas.',
    arpComp: {
      findData: 'Buscando por: ',
      result: 'Encontrado en los dispositivos:',
      headers: {
        ip: 'IP',
        vlan: 'VLAN',
        mac: 'MAC',
        name: 'Nombre',
        network: 'Red',
        date: 'Fecha',
        vendor: 'Fabricante',
        device: 'Dispositivo',
        interface: 'Interfaz',
        interfaceDescription: 'Descripción Interfaz',
      },
    },
    arpConf: {
      transitInterfacesConf: {
        headerMessage: 'Editar interfaces de tránsito',
        transitInterface: 'Interfaz de tránsito',
        transitInterfaces: 'Interfaces de tránsito',
        error: 'Error al obtener las interfaces de tránsito.',
      }
    }
  }
}