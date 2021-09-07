<template>
  <div class="devices">
    <h3> {{ $t('devices.messageDevice')}} </h3>
    <!-- Displays device list from DataBase (DB) -->
    <div class="device-table">
      <AllDeviceComp 
        :deviceList="deviceList"
        :loading="loading"
        @selectedDevice="getDevices"
        @actionController="actionController"
      ></AllDeviceComp>
    </div>
    
    <!-- Displays alert message whenever backend actions occurs -->
    <AlertComponent
      :showAlert="showAlert"
      :message="alertMessage"
      :type="alertType"
    ></AlertComponent>

    <!-- Shows selected devices's configuration -->
    <ShowConfigComponent
      :showConfig="showConfig"
      :loadingConfig="loadingConfig"
      :item="configItem"
      :title="configTitle"
      :data="configData"
      @unselectItem="showConfig=null, configData=null"
    ></ShowConfigComponent>
  </div>
</template>

<script>
import AllDeviceComp from '@/components/devices/AllDeviceComp.vue';
import ShowConfigComponent from '@/components/utilityComponents/ShowConfigComponent.vue';
import {buildJsonArray} from '@/utils/functions.js';
import {getDevicesAPI, deleteDevicesAPI, addDeviceAPI, editDeviceAPI, getDeviceConfigAPI} from '@/api/devices.js';
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'

export default{
  name: 'Devices',
  components:{
    AllDeviceComp,
    AlertComponent,
    ShowConfigComponent,
  },
  data(){
    return {
      deviceList: [],
      loading: false,
      alertMessage: '',
      alertType: 'info',
      showAlert: false,
      selectedDevice: null,
      selectedDevices: null,
      deviceConfig: '',
      
      // ShowConfigComponent props
      showConfig: false,
      loadingConfig: false,
      configTitle: '',
      configItem: null,
      configData: '',
    }
  },
  methods: {
    // ACTION CONTROLLER
    actionController(ev, devices){
      switch(ev){
        case "addDevice":
          this.addDevice(devices)
          break;
        case "deleteDevices":
          this.deleteDevices(devices)
          break;
        case "refreshDevices":
          this.loadDevices()
          break;
        case "editDevice":
          this.editDevice(devices)
          break;
        case "seeDeviceConfig":
          this.getDeviceConfig(devices)
          break;
        case "applyConfigBtn":
          this.deviceTask(devices)
          break;
        default:
          console.log("Unknow action")
      }
    },
    /** ============================
     *  Action methods
     ==============================*/
    getDevices(value){
      if(value){
        this.selectedDevices=value;
      }else{
        console.log("ALERT ERROR")
      }
    },
    loadDevices(){
      this.loading = true;
      getDevicesAPI().then(res=>{
        this.deviceList = buildJsonArray(res.data.data)
        this.loading = false
        // this.displayAlertTime(1, 'success', this.$t('alerts.successLoadingItems') )
      }).catch(e => {
        this.loading = false
        this.displayAlertTime(5, 'error', this.$t('errors.databaseError'))
        console.log("e => ", e)
      });
    },
    addDevice(device){
      addDeviceAPI(device).then( () => {
        this.loadDevices()
        this.displayAlertTime(3, 'success', this.$t('alerts.successAddingItem') )
      }).catch(e => {
        this.loading = false
        this.displayAlertTime(5, 'error', this.$t('errors.databaseError'))
        console.log("e => ", e)
      });
    },
    editDevice(device){
      editDeviceAPI(device).then( () => {
        this.loadDevices()
        this.displayAlertTime(3, 'success', this.$t('alerts.successEditingItem'))
      }).catch(e => {
        this.loading = false;
        this.displayAlertTime(5, 'error', this.$t('errors.databaseError'))
        console.log("e => ", e)
      });
    },
    deleteDevices(value){
      this.selectedDevices = value
      deleteDevicesAPI(this.selectedDevices).then( (res) => {
        console.log(1,res)
        this.loading = false
        this.loadDevices()
        this.displayAlertTime(3, 'success', this.$t('alerts.successDeletingItem'))
      }).catch(e => {
        this.loading = false;
        this.displayAlertTime(5, 'error', this.$t('errors.databaseError'))
        console.log("e => ", e)
      });
    },
    getDeviceConfig(devices){
        this.deviceConfig = null
        this.loadingConfig = true
        this.selectedDevice = devices
        this.showConfig = true
        this.configItem = this.selectedDevice,
        this.configTitle = this.selectedDevice.name,
        this.configData = ''
      getDeviceConfigAPI(devices).then( res => {
        this.configData = res.data.data
        // this.deviceConfig = res.data.data
        this.loadingConfig = false;
      }).catch( e => {
        console.log("e => ", e.response)
        this.loadingConfig = false;
        this.showConfig = false
        let msg = this.$t('errors.deviceConnectionError') + "\t(" + e.response.data.data + ")"
        this.displayAlertTime(5, 'error', msg)
      });
    },
    deviceTask(device){
      this.$router.push(this.$route.path+"/task/"+device.id)
    },
    /**
     * Configure the alert component showed
     * @param time seconds to display alert component
     * @param type the type of alert component
     * @param message string displayed by alert component
     */
    displayAlertTime(time, type, message){
      this.alertType = type
      this.showAlert = true
      this.alertMessage = message
      let seconds = time*1000
      setTimeout( () => {
        this.showAlert = false
      }, seconds)
    }
  },
  mounted(){
    this.loadDevices()
    this.showAlert = false
  },

}
</script>

<style lang="scss" scoped>
.devices{
  width: 100%;
  margin-right: 4rem;
}
.device-table{
  width: 80%;
}
</style>




