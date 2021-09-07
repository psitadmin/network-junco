import axios from 'axios'; 

const path = process.env.VUE_APP_BACK_URL+'/task'

export function getDeviceInterfacesAPI (device_ip) {
  return new Promise( (resolve,reject) => {
    axios.get(path+"/interfaces", {params: {device: device_ip}} ,{
      headers: {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
      },
    }).then( (res) => {
      setTimeout( () => {resolve(res)},500 )}
    ).catch( (res) => {reject(res)})
  })
}
export function postDeviceInterfacesAPI (device_id, changes) {
  return new Promise( (resolve,reject) => {
    axios.post(path+"/interfaces" ,
      {
        headers: {
          'Access-Control-Allow-Origin' : '*',
          'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        },
        data: {
          'changes': changes
        },
      },
      { params: {device: device_id} }
      ).then( (res) => {
      setTimeout( () => {resolve(res)},500 )}
    ).catch( (res) => {reject(res)})
  })
}
