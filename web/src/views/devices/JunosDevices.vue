<template>
  <div class="devices">
    <h3> {{ $t('devices.messageDevice')}} </h3>
    <!-- Displays device list from API -->
    <JunosDeviceComp 
      :deviceList="deviceList"
      :loading="loading"
      @selectedDevice="getDevices"
      @selectedItems="getDevices"
    ></JunosDeviceComp>
    <div class="device-actions">   
      <div class="device-actions-left">
        <v-btn
          data-test="show-config-button"
          margin=10px
          color="#003245"
          class="device-button"
          :disabled="!selectedLenght"
          :title="$t('global.seeConfig')"
          @click="seeConfig"
        > {{$t('global.seeConfig')}} </v-btn>
        <v-btn
          data-test="apply-config-button"
          margin=10px
          color="#003245"
          class="device-button"
          :disabled="!selectedLenght"
          :title="$t('global.applyConfig')"
          @click="applyConfig"
        > {{$t('global.applyConfig')}} </v-btn>
      </div>
      <div class="device-actions-right">
        <!-- <v-btn
          margin=10px
          color="#003245"
          class="device-button"
          :title="$t('devices.deviceComp.addDevice')"
          @click="addDevice"
        > <v-icon>mdi-plus</v-icon> </v-btn>  
        <v-btn
          margin=10px
          color="red"
          class="device-button"
          :title="$t('devices.deviceComp.deleteDevice')"
          @click="deleteDevice"
        > <v-icon>mdi-delete</v-icon> </v-btn>   -->
      </div>
    </div> 
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
import JunosDeviceComp from '@/components/devices/JunosDeviceComp.vue';
import ShowConfigComponent from '@/components/utilityComponents/ShowConfigComponent.vue';
import {getDevicesJUNOS, getDeviceConfigJUNOS} from '@/api/junos.js'
import toJson from 'xml-js'

export default{
  name: 'Devices',
  components:{
    JunosDeviceComp,
    ShowConfigComponent,
  },
  data(){
    return {
      deviceList: [],
      loading: false,
      selectedDevice: [],
      scrolled: false,
      // ShowConfigComponent props
      showConfig: false,
      loadingConfig: false,
      configTitle: '',
      configItem: null,
      configData: '',
    }
  },
  methods: {
    getDevices(value){
      if(value){
        this.selectedDevice=value;
      }
    },
    
    seeConfig(){
      this.showConfig = true
      this.loadingConfig = true
      this.configItem = this.selectedDevice[0]
      this.configTitle = this.selectedDevice[0]["name"]
      this.configData = ""
      getDeviceConfigJUNOS(this.selectedDevice[0]["device-id"]).then(res=>{
        this.configData = this.xml2string(res.data["expanded-xml-configuration"].configuration)
        this.loadingConfig = false
      }).catch(e => {
        this.showConfig = false
        this.loadingConfig = false
        console.log(e)
      });
    },
    applyConfig() {
      this.$router.push({
        path: `/junosdevices/${this.selectedDevice[0]["device-id"]}`
      });
    },
    xml2string(value){
      // var result = toJson.xml2js(value["expanded-xml-configuration"].configuration, {ignoreCdata: false})
      // var result2 = toJson.xml2js(result.elements[0].cdata)
      var result = toJson.xml2js(value, {ignoreCdata: false})
      return result.elements[0].cdata;
    }
  },
  mounted(){
    this.loading = true;
    getDevicesJUNOS().then(res=>{
      this.deviceList = res.data.devices.device
      this.loading = false;
    }).catch(e => {
      this.loading = false;
      console.log(e)
    });
  },
  computed: {
    someSelected(){
      return this.selectedConfiglets.length >= 1
    },
    selectedLenght() {
      return this.selectedDevice.length === 1;
    },
  },
  watch: {
    // deviceList: {
    //   handler(value) {
    //     console.log("HANDLER", value)
    //   }, deep: true
    // },
  }
}
</script>

<style lang="scss" scoped>
.devices{
  width: 100%;
  margin-right: 4rem;
}

.device-actions {
  display: flex;
  justify-content: space-between;
  &-left {
    justify-content: flex-start;
  }
  &-right {
    justify-content: flex-end;
  }
}
.device-button {
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
</style>




