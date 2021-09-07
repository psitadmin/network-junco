import {axiosinstance} from '@/utils/axiosinstance';

const path = 'https://pr-junspace-vip.hi.inet/api/space/'

// ============================================
// DEVICES
// ============================================
function getDevicesJUNOS() {
  return axiosinstance.get(path+'device-management/devices',{
    headers: {
      'Accept': 'application/vnd.net.juniper.space.device-management.devices+json;version=2'
    }
  })
}
export function getDeviceDataJUNOS(device_id) {
  let new_path = path+'device-management/devices/'+device_id
  return axiosinstance.get(new_path+"",{
    headers: {
      'Accept': 'application/vnd.net.juniper.space.device-management.device+json;version=1',
    },
  })
}
export function getDeviceConfigJUNOS(device_id) {
    let new_path = path+'device-management/devices/'+device_id+'/configurations/expanded'
  return axiosinstance.get(new_path+"",{
    headers: {
      'Accept': 'application/vnd.net.juniper.space.device-management.expanded-xml-configuration+json;version=5',
    },
  })
}

// ============================================
// CONFIGLETS
// ============================================
function getConfigletsJUNOS() {
  return axiosinstance.get(path+'configuration-management/cli-configlets',{
    headers: {
      'Accept': 'application/vnd.net.juniper.space.configuration-management.cli-configlets+json;version=3'
    }
  })
}

export function getConfigletsDataJUNOS(configlet_id) {
  return axiosinstance.get(path+'configuration-management/cli-configlets/'+configlet_id,{
    headers: {
      'Accept': 'application/vnd.net.juniper.space.configuration-management.cli-configlet+json;version=3'
    }
  })
}

export function getApplicableDevicesJUNOS(configlet_id){
  return axiosinstance.get(path+'configuration-management/cli-configlets/'+configlet_id+'/applicable-devices',{
    headers: {
      'Accept': 'application/vnd.net.juniper.space.configuration-management.applicable-devices+json;version=1'
    }
  })
}

export function getApplicableConfigletsJUNOS(device_id){
  return axiosinstance.get(path+'device-management/devices/'+device_id+'/applicable-configlets',{
    headers: {
      'Accept': 'application/vnd.net.juniper.space.device-management.applicable-configlets+json;version=5'
    }
  })
}

export function validateConfigletJUNOS(configlet_id, input){
  return axiosinstance.post(path+'configuration-management/cli-configlets/'+configlet_id+'/validate-cli-configlet', input, {
    headers: {
      'Content-Type': 'application/vnd.net.juniper.space.configuration-management.validate-cli-configlet+json;version=1;charset=UTF-8',
      'Accept': 'application/vnd.net.juniper.space.job-management.task+json;version=1'
    }
  })
}

export function getValidateResultJUNOS(job_id){
  return axiosinstance.get(path+'configuration-management/job-instances/'+job_id+'/validate-cli-configlet-job-results', {
    headers: {
      'Accept': 'application/vnd.net.juniper.space.configuration-management.validate-cli-configlet-job-results+json;version=1'
    }
  })
}

export function applyConfigletJUNOS(configlet_id, input){
  return axiosinstance.post(path+'configuration-management/cli-configlets/'+configlet_id+'/apply-cli-configlet', input, {
    headers: {
      'Content-Type': 'application/vnd.net.juniper.space.configuration-management.apply-cli-configlet-request+json;version=3;charset=UTF-8',
      'Accept': 'application/vnd.net.juniper.space.job-management.task+json;version=1'
    }
  })
}


// ============================================
//  ALL DEVICES
// ============================================
function addDeviceAPI(device) {
  return axiosinstance.post(path ,{
    headers: {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    },
    data: {
      'device' : device,
    },
  })
}

export function deleteConfigletJUNOS(configlet_id){
  return axiosinstance.delete(path+'configuration-management/cli-configlets/'+configlet_id,{
  })
}

export {getDevicesJUNOS, getConfigletsJUNOS, addDeviceAPI};