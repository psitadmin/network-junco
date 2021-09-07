import axios from 'axios'; 

const path = process.env.VUE_APP_BACK_URL+'/arp'

function resolveARPAPI(address) {
    return new Promise( (resolve,reject) => {
        axios.post(path, {    
            headers: {
                'Access-Control-Allow-Origin' : '*',
                'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            },
            data: {
                'address': address,
            }
        }).then ( (res) => {
            setTimeout( () => {resolve(res)}, 250 )}
        ).catch( (res) => {reject(res)})
    })
}

function getTransitInterfacesAPI() {
    return new Promise( (resolve,reject) => {
        axios.get(path+"/transitinterfaces", {    
            headers: {
                'Access-Control-Allow-Origin' : '*',
                'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            },
        }).then ( (res) => {
            setTimeout( () => {resolve(res)}, 500 )}
        ).catch( (res) => {reject(res)})
    })
}

export function postTransitInterfacesAPI(new_int, edit_int, delete_int){
    return new Promise( (resolve,reject) => {
        axios.post(path+"/transitinterfaces", {    
            headers: {
                'Access-Control-Allow-Origin' : '*',
                'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            },
            data: {
                'put': new_int,
                'post': edit_int,
                'delete': delete_int
            }
        }).then ( (res) => {
            setTimeout( () => {resolve(res)}, 500 )}
        ).catch( (res) => {reject(res)})
    })
}
export {resolveARPAPI, getTransitInterfacesAPI}