import axios from 'axios'; 

const path = process.env.VUE_APP_BACK_URL+'/devices'

function getDevicesAPI () {
  return new Promise( (resolve,reject) => {

    axios.get(path, {} ,{
      headers: {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
      },
    }).then( (res) => {
      setTimeout( () => {resolve(res)},500 )}
    ).catch( (res) => {reject(res)})
  })
}

export function getDeviceByIDAPI(ids) {
  return new Promise( (resolve,reject) => {
    if(ids.length === 1){
      axios.get(path, { params: {device: ids[0]} } ,{
        headers: {
          'Access-Control-Allow-Origin' : '*',
          'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        },
      }).then( (res) => {
        setTimeout( () => {resolve(res)},500 )}
      ).catch( (res) => {reject(res)})
    }else{
      console.log("TODO: construir query param con >1 device")
      
    }
  })
}

function deleteDevicesAPI(devices) {
  return axios.delete(path ,{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
    data: {
      'devices' : devices,
    },
  })
}

function addDeviceAPI(device) {
  return axios.post(path ,{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
    data: {
      'device' : device,
    },
  })
}

function editDeviceAPI(device) {
  return axios.put(path ,{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
    data: {
      'device' : device,
    },
  })
}

function getDeviceConfigAPI(device){
  return axios.post(path+'/config',{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
    data: {
      'device': device,
    }
  })

}

export function getVendorsAPI(){
  return axios.get(path.concat('/vendors') ,{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
  })
}

export function getProtocolsAPI(){
  return axios.get(path.concat('/protocol') ,{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
  })
}

export function getDeviceTypeAPI(){
  return axios.get(path.concat('/device_types') ,{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
  })
}

export {getDevicesAPI, deleteDevicesAPI, addDeviceAPI, editDeviceAPI, getDeviceConfigAPI};