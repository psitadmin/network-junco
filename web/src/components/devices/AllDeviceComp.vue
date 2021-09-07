<template>
  <div class="deviceTable">
    <div class="searchBar">
      <v-data-table
        data-test="device-table"
        width=100%
        v-model="selected"
        :headers="items.headers"
        :items="deviceList"
        :loading="loading"
        :loading-text="$t('global.loadingText')"
        item-key="id"
        show-select
        :search="searchText"
        fixed-header
        dense
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon
            small
            @click="editDevice(item.id)"
          > mdi-pencil </v-icon>
        </template>
        <template v-slot:top>
          <v-text-field
            data-test="device-search-bar"
            v-model="searchText"
            :label="items.searchLabel"
          ></v-text-field>
        </template>
        
      </v-data-table>
      <div class="device-actions">   
        <div class="device-actions-left">
          <v-btn
            data-test="show-config-button"
            margin=10px
            color="#003245"
            class="device-button"
            :disabled="!selectedLenght"
            :title="$t('global.seeConfig')"
            @click="actionButtonController('seeDeviceConfig')"
          > {{$t('global.seeConfig')}} </v-btn>
          <v-btn
            data-test="apply-config-button"
            margin=10px
            color="#003245"
            class="device-button"
            :disabled="(!selectedLenght)"
            :title="$t('global.applyConfig')"
            @click="actionButtonController('applyConfigBtn')"
          > {{$t('global.applyConfig')}} </v-btn>
        </div>
        <div class="device-actions-right">
          <v-btn
            margin=10px
            color="#003245"
            class="device-button-icon"
            :title="$t('devices.deviceComp.addDevice')"
            @click="actionButtonController('addBtn')"
          > <v-icon>mdi-plus</v-icon> </v-btn>
          <v-btn
            margin=10px
            color="red"
            class="device-button-icon"
            :disabled="!someSelected"
            :title="$t('devices.deviceComp.deleteDevice')"
            @click="actionButtonController('deleteBtn')"
          > <v-icon>mdi-delete</v-icon> </v-btn>
          <v-btn
            margin=10px
            color="green"
            class="device-button-icon"
            :title="$t('global.refresh')"
            @click="actionButtonController('refreshBtn')"
          > <v-icon>mdi-refresh</v-icon> </v-btn>  
          <DialogComp
            :dialogObj="dialogCompObj"
            @closeDialog="closeDialogComp"
            @acceptDialog="acceptDialogComp"
          ></DialogComp>
        </div>
      </div> 
    </div>
  </div>
  
</template>

<script>
import DialogComp from '@/components/utilityComponents/DialogComp.vue';
import {getDeviceTypeAPI, getProtocolsAPI, getVendorsAPI} from '@/api/devices.js';

export default {
  name: 'AllDeviceComp',
  props: {
    deviceList: Array,
    loading: Boolean,
  },
  components: {
    DialogComp,
  },
  data() {
    return {
      addDeviceDialog: false,
      deleteDialog: false,
      searchText: '',
      selected: [],
      dialogCompObj: {
        headerText: String,
        bodyText: String,
        buttons: Array,
        showComponent: false,
        vendorList: [],
        protocolList: [],
        deviceTypeList: [],
      },
      activeObj: true,
    }
  },
  computed: {
    items() {
      return {
        headers: [
          { text: this.$t("devices.deviceComp.headers.idHeader"), value: "id" },
          { text: this.$t("devices.deviceComp.headers.ipHeader"), value: "ip" },
          { text: this.$t("devices.deviceComp.headers.nameHeader"), value: "name" },
          { text: this.$t("devices.deviceComp.headers.vendorHeader"), value: "vendor" },
          // { text: this.$t("devices.deviceComp.headers.serialNumberHeader"), value: "serial_number" },
          // { text: this.$t("devices.deviceComp.headers.platformHeader"), value: "platform" },
          { text: this.$t("devices.deviceComp.headers.protocol"), value: "protocol" },  
          { text: this.$t("devices.deviceComp.headers.location"), value: "location" },
          { text: this.$t("devices.deviceComp.headers.deviceType"), value: "device_type" },
          { text: this.$t("devices.deviceComp.headers.date"), value: "date" },
          { text: '', value: 'actions', sortable: false },
        ],
        searchLabel: this.$t("global.searchMessage"),
      }
    },
    someSelected(){
      return this.selected.length >= 1
    },
    selectedLenght() {
      return this.selected.length === 1;
    },
  },
  methods: {
    // BUTTON CONTROLLER: Watches all button type and selects appropriate task
    actionButtonController(ev){
      switch(ev){
        case "addBtn":
          this.addDevice()
          break;
        case "deleteBtn":
          this.deleteDevice()
          break;
        case "refreshBtn":
          this.refreshDevices()
          break;
        case "seeDeviceConfig":
          this.seeConfig()
          break;
        case "applyConfigBtn":
          this.applyConfig()
          break;
      }
    },
    // Flush all dialogCompObj attributes and delete component
    closeDialogComp(){
      this.dialogCompObj.showComponent = false
      this.dialogCompObj.action = ''
      this.dialogCompObj.headerText = ''
      this.dialogCompObj.bodyText = ''
      this.dialogCompObj.headers = []
      this.dialogCompObj.params = []
      this.dialogCompObj.buttons = []
      this.dialogCompObj.vendorList = []
      this.dialogCompObj.protocolList = []
      this.dialogCompObj.deviceTypeList = []
    },
    // Catch the event emitted by component and calls appropiate method
    acceptDialogComp(ev, device){
      switch (ev) {
        case "add":
          this.$emit('actionController','addDevice', device)
          break;
        case "delete":  
          this.$emit('actionController','deleteDevices', this.selected)
          this.selected = []
          this.refreshDevices()
          break;
        case "edit":
          this.$emit('actionController','editDevice', device)
          break;
        default:
          console.log("UNKNOW ACTION DIALOG ACCEPT")
      }
      this.closeDialogComp()
    },
    /** ============================
     *  CRUD device methods
     ==============================*/
    editDevice(deviceID){
      this.dialogCompObj.action = "edit"
      this.dialogCompObj.headerText = this.$t("devices.deviceComp.editDevice")
      this.dialogCompObj.bodyText = this.$t("devices.deviceComp.cards.addText")
      this.dialogCompObj.headers = [
        {text: this.$t("global.parameter"), value: "parameter"},
        {text: this.$t("global.value"), value: "value"},
      ]
      this.dialogCompObj.params = [
        { parameter: this.$t("devices.deviceComp.headers.ipHeader"), value: "", placeholder: "XXX.XXX.XXX.XXX" },
        { parameter: this.$t("devices.deviceComp.headers.nameHeader"), value: "", placeholder: this.$t("devices.deviceComp.cards.nameHint") },
        { parameter: this.$t("devices.deviceComp.headers.vendorHeader"), value: "", placeholder: "[Cisco/Juniper]", selectOptions: this.dialogCompObj.vendorList },
        { parameter: this.$t("devices.deviceComp.headers.protocol"), value: "", placeholder: "[SSH/Telnet]", selectOptions: this.dialogCompObj.protocolList },
        { parameter: this.$t("devices.deviceComp.headers.deviceType"), value: "", placeholder: "[Router/Switch]", selectOptions: this.dialogCompObj.deviceTypeList },
      ]
      this.getVendorsList()
      this.getProtocolsList()
      this.getDeviceTypeList()
      this.dialogCompObj.buttons = [
        {
          // Clear dialog button
          color: "red",
          action: "clear",
          class: "device-button",
          text: this.$t('global.clear')
        },
        {
          // Accept dialog button
          color: "#003245",
          action: "edit",
          class: "device-button",
          text: this.$t('global.confirm')
        },
      ]
      this.dialogCompObj.editableDevice = this.deviceList.find(item => item.id === deviceID )
      this.dialogCompObj.showComponent = true
    },
    addDevice() {
      // Create addComponent
      this.dialogCompObj.action = "add"
      this.dialogCompObj.headerText = this.$t("devices.deviceComp.cards.addTitle")
      this.dialogCompObj.bodyText = this.$t("devices.deviceComp.cards.addText")
      this.dialogCompObj.showComponent = true
      this.dialogCompObj.headers = [
        {text: this.$t("global.parameter"), value: "parameter"},
        {text: this.$t("global.value"), value: "value"},
      ]
      
      this.dialogCompObj.params = [
        { parameter: this.$t("devices.deviceComp.headers.ipHeader"), value: "", placeholder: "XXX.XXX.XXX.XXX" },
        { parameter: this.$t("devices.deviceComp.headers.nameHeader"), value: "", placeholder: this.$t("devices.deviceComp.cards.nameHint") },
        { parameter: this.$t("devices.deviceComp.headers.vendorHeader"), value: "", placeholder: "[Cisco/Juniper]", selectOptions: this.dialogCompObj.vendorList },
        { parameter: this.$t("devices.deviceComp.headers.protocol"), value: "", placeholder: "[SSH/Telnet]", selectOptions: this.dialogCompObj.protocolList },
        { parameter: this.$t("devices.deviceComp.headers.deviceType"), value: "", placeholder: "[Router/Switch]", selectOptions: this.dialogCompObj.deviceTypeList },
      ]
      this.getVendorsList()
      this.getProtocolsList()
      this.getDeviceTypeList()
      this.dialogCompObj.buttons = [
        {
          // Dialog Clear button
          color: "red",
          action: "clear",
          class: "device-button",
          text: this.$t('global.clear')
        },
        {
          // Dialog Accept button
          color: "#003245",
          action: "add",
          class: "device-button",
          text: this.$t('global.confirm')
        },
      ]
    },
    deleteDevice() {
      // Create deleteComponent
      this.dialogCompObj.action = "delete"
      this.dialogCompObj.headerText = this.$t("devices.deviceComp.cards.deleteTitle")
      this.dialogCompObj.bodyText = this.$t("devices.deviceComp.cards.deleteText")
      this.dialogCompObj.showComponent = true
      this.dialogCompObj.items = this.selected
      this.dialogCompObj.headers = [
        { text: this.$t("devices.deviceComp.headers.idHeader"), value: "id" },
        { text: this.$t("devices.deviceComp.headers.ipHeader"), value: "ip" },
        { text: this.$t("devices.deviceComp.headers.nameHeader"), value: "name" },
      ]
      this.dialogCompObj.buttons = [
        {
          // Accept dialog button
          color: "#003245",
          action: "delete",
          class: "device-button",
          text: this.$t('global.confirm'),
        },
      ]
    },
    refreshDevices(){
      this.$emit('actionController','refreshDevices')
    },
    applyConfig() {
      this.$emit('actionController', 'applyConfigBtn', this.selected[0])
    },
    seeConfig() {
      this.$emit('actionController', 'seeDeviceConfig', this.selected[0])
    },

    // Retrieves vendor list data from database
    getVendorsList(){
      getVendorsAPI().then(res=>{
        for (let i in res.data.data) {
          this.dialogCompObj.vendorList.push(res.data.data[i])
        }
      }).catch(e => {
        console.log("e => ", e)
      });
    },
    getProtocolsList(){
      getProtocolsAPI().then(res=>{
        for (let i in res.data.data) {
          this.dialogCompObj.protocolList.push(res.data.data[i])
        }
      }).catch(e => {
        console.log("e => ", e)
      });
    },
    getDeviceTypeList(){
      getDeviceTypeAPI().then(res=>{
        for (let i in res.data.data) {
          this.dialogCompObj.deviceTypeList.push(res.data.data[i])
        }
      }).catch(e => {
        console.log("e => ", e)
      });
    }

  },
}
</script>

<style lang="scss" scoped>

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
  &-icon{
    margin-left: 1rem;
    min-width: unset !important;
    height: 36px;
    width: 40px;
    ::v-deep .v-btn__content {
      color:#fff
    }
  }
}
</style>
