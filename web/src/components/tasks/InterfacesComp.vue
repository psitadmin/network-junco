<template>
<div>

  <v-dialog
    class="interfacesDialog"
    v-model="showComponent"
    persistent
    max-width="1000"
  >
    <DialogComp
      :dialogObj="dialogObj"
      @closeDialog="closeDialogComp"
      @acceptDialog="acceptDialogComp"
    ></DialogComp>
    <LoadingDialogComp
      @closeDialog="closeLoadingDialogComp"
      :loadingDialogObj="loadingDialogObj"
      :loading="loadingInterfacesResult"
    ></LoadingDialogComp>
    <v-card>
      <v-card-title class="headline"> {{device.name}} ({{device.ip}}) </v-card-title>
      <h3>{{$t("tasks.interfacesTask.hint")}}{{$t("global.confirm")}}</h3>
      <div class="loading"
        v-if="loading"
      >
        <v-progress-circular
          class="loading-item"
          :size="50"
          indeterminate
          color="primary"
        ></v-progress-circular>
      </div>
      <div v-else>
        <v-card-text
          v-if="interfacesList.length"
        >
          <v-data-table
            class="interfacesDialog-table"
            :headers="items.headers"
            :items="editedInterfacesList"
            :search="searchText"
            :item-class="getBackgroundColor"
            item-key="name"
            fixed-header
            dense
          >
            <!-- Color led item -->
            <template 
              class="interfacesDialog-table-status"
              v-slot:[`item.signal`]="{ item }"
            > 
              <v-icon
                small
                :color="getStatusColor(item.name)"
              > mdi-circle </v-icon>
            </template>

            <!-- Select action item -->
            <template 
              v-slot:[`item.action`]="{ item }"
            > 
              <v-select
                class="interfacesDialog-table-select"
                v-model="item.action"
                :disabled="item.description === 'LIBRE'"
                hide-details="true"
                label="enable / disable"
                solo
                flat
                outlined
                dense
                required
                :items="selectActions"
              ></v-select>
            </template> 
            
            <!-- Description textfield item -->
            <template 
              class="status"
              v-slot:[`item.description`]="{ item }"
            > 
               <v-text-field
                class="interfacesDialog-table-textfield"
                v-model="item.description"
                :disabled="item.description === 'LIBRE'"
                hide-details="true"
                solo
                dense
                append-icon="mdi-replay"
                @click:append="restoreDescription(item)"
                :label="item.description"
               ></v-text-field>
            </template>

            <!-- SEARCH BAR -->
            <template v-slot:top>
              <v-text-field
                data-test="device-search-bar"
                v-model="searchText"
                :label="items.searchLabel"
              ></v-text-field>
            </template>
          </v-data-table>
        </v-card-text>
      </div>
      <div 
        class="interfacesDialog-buttons"
      >
        <v-btn
          text
          @click="changesDetected = false, $emit('closeDialog', 'InterfacesComp')"
        >{{ $t('global.cancel') }}</v-btn> 
        <v-btn
          margin=10px
          :disabled="!changesDetected"
          color="#003245"
          class="device-button"
          :title="$t('global.applyConfig')"
          @click="confirmChanges()"
        > {{$t('global.confirm')}} </v-btn>
      </div>
    <!-- Displays alert message whenever backend actions occurs -->
    <AlertComponent
      :showAlert="showAlert"
      :message="alertMessage"
      :type="alertType"
    ></AlertComponent>
    </v-card>
  </v-dialog>
</div>


</template>

<script>
import {getDeviceInterfacesAPI, postDeviceInterfacesAPI} from '@/api/tasks.js';
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'
import DialogComp from '@/components/utilityComponents/DialogComp.vue';
import LoadingDialogComp from '@/components/utilityComponents/LoadingDialogComp.vue';

export default {
  name: 'InterfacesComp',
  components: {
    AlertComponent,
    DialogComp,
    LoadingDialogComp,
  },
  props: {
    device: Object,
    showComponent: Boolean,
  },
  data(){
    return {
      interfacesList: [],
      editedInterfacesList: [],
      changesToApply: [],
      searchText: '',
      loading: false,
      changesDetected: false,

      // Select items
      selectActions: [
        {text: 'enable', value: true},
        {text: 'disable', value: false}
      ],

      // Dialog Comp
      dialogObj: {
        headerText: '',
        bodyText: '',
        buttons: [],
        showComponent: false,
      },

      // Loading Dialog Result
      loadingInterfacesResult: false,
      loadingDialogObj: {
        headerText: '',
        bodyText: '',
        buttons: [],
        status: '',
        showComponent: false,
      },

      // Alert component
      alertMessage: '',
      alertType: 'info',
      showAlert: false,

    }
  },
  methods: {
    loadInterfaces(){
      this.loading = true
      this.changesDetected = false
      getDeviceInterfacesAPI(this.device.id).then( res => {
        this.interfacesList = res.data.data
        this.interfacesList.forEach( (item) => {
          if(this.device.vendor.toLowerCase() === "juniper"){
            item.action = item.status.toLowerCase().includes("down") ? false : true
          }else if(this.device.vendor.toLowerCase() === "cisco"){
            item.action = item.status.toLowerCase().includes("admin") ? false : true
          }
        })
        console.log("RES = ",res)
        this.editedInterfacesList = JSON.parse(JSON.stringify(res.data.data))
        this.loading = false
      }).catch(e => {
        this.loading = false
        this.displayAlertTime(5, 'error', this.$t('errors.databaseError'))
        console.log("e => ", e)
      });
    },
    confirmChanges(){
      this.changesToApply = []
      var itemCopy
      // Checking about changes on items 
      this.editedInterfacesList.forEach(item => {
        var changes = this.interfacesList.find(newItem => newItem.name === item.name )
        if(this.device.vendor.toLowerCase() === "juniper"){
          if(
            (item.action == false && item.status.toLowerCase() === "up") ||
            (item.action == true && item.status.toLowerCase().includes("down")) || 
            (item.description !== changes.description)
            ){
              // Add changes to array
              itemCopy = JSON.parse(JSON.stringify(item))
              this.changesToApply.push(itemCopy)
              // Removes unchanged items
              if((item.action == true && item.status.toLowerCase() === "up") ||
                (item.action == false && item.status.toLowerCase().includes("down"))){
                  delete this.changesToApply[this.changesToApply.indexOf(itemCopy)].action
              }
              else if(changes.description == item.description){
                delete this.changesToApply[this.changesToApply.indexOf(itemCopy)].description
              }
          } 
        }else if(this.device.vendor.toLowerCase() === "cisco"){
          if(
            (item.action == false && !item.status.toLowerCase().includes("admin")) ||
            (item.action == true && item.status.toLowerCase().includes("admin")) || 
            (item.description !== changes.description)
            ){
              // Add changes to array
              itemCopy = JSON.parse(JSON.stringify(item))
              this.changesToApply.push(itemCopy)
              // Removes unchanged items
              if((item.action == true && !item.status.toLowerCase().includes("admin")) ||
                (item.action == false && item.status.toLowerCase().includes("admin"))){
                  delete this.changesToApply[this.changesToApply.indexOf(itemCopy)].action
              }
              else if(changes.description == item.description){
                delete this.changesToApply[this.changesToApply.indexOf(itemCopy)].description
              }
            }
        }
      });
      // Creating labels to show relevant info on dialog component
      this.changesToApply.forEach(item => {
        item.label = item.action != null ? this.selectActions.find(itemAction => itemAction.value === item.action).text : null
      })
      // Creating dialog object 
      this.dialogObj.action = 'confirm'
      this.dialogObj.headerText = this.$t("tasks.interfacesTask.headerText")
      this.dialogObj.bodyText = this.$t("tasks.interfacesTask.bodyText")
      this.dialogObj.showComponent = true
      this.dialogObj.items = this.changesToApply
      this.dialogObj.headers = [
        { text: this.$t("tasks.interfacesTask.name"), value: "name" },
        { text: this.$t("tasks.interfacesTask.action"), value: "label" },
        { text: this.$t("tasks.interfacesTask.description"), value: "description" }
      ]
      this.dialogObj.buttons = [
        {
          // Accept dialog button
          color: "#003245",
          action: "confirm",
          class: "device-button",
          text: this.$t('global.apply'),
        },
      ]
    },
    // =========================================================
    // Table template methods
    // =========================================================
    getBackgroundColor(item){
      var original = this.interfacesList.find(newItem => newItem.name === item.name )
      if(this.device.vendor.toLowerCase() === "juniper"){
        if( 
          (item.action == false && original.status.toLowerCase() === "up") ||
          (item.action == true && original.status.toLowerCase().includes("down")) || 
          (item.description !== original.description) ){
            return 'editedItem'
        }else{
          return ''
        }
      }else if(this.device.vendor.toLowerCase() === "cisco"){
        if( 
          (item.action == false && !original.status.toLowerCase().includes("admin")) ||
          (item.action == true && original.status.toLowerCase().includes("admin")) || 
          (item.description !== original.description) ){
            return 'editedItem'
        }else{
          return ''
        }
      }
    },
    getStatusColor(name){
      var original = this.interfacesList.find(newItem => newItem.name === name )
      if(original.status.toUpperCase().includes("UP")){
        return "green"
      }else{
        return "red"
      }
    },
    restoreDescription(item){
      var original = this.interfacesList.find(newItem => newItem.name === item.name)
      var modified = this.editedInterfacesList.find(newItem => newItem.name === item.name)
      console.log("original ", original, " mod ", modified, " item ", item)
      modified.description = original.description
    },
    // =========================================================
    // Dialog component methods
    // =========================================================
    closeLoadingDialogComp(){
      this.loadingInterfacesResult = false
      this.loadingDialogObj.showComponent = false
      this.loadingDialogObj.headerText = ''
      this.loadingDialogObj.bodyText = ''
      this.loadingDialogObj.buttons = []
      this.loadingDialogObj.content = ''
      this.loadInterfaces()
    },
    closeDialogComp(){
      this.dialogObj.showComponent = false
      this.dialogObj.headerText = ''
      this.dialogObj.bodyText = ''
      this.dialogObj.buttons = []
      this.dialogObj.action = ''
      this.dialogObj.items = [] 
      this.dialogObj.headers = []
      this.editedInterfacesList.forEach( item => {
        delete item.label
      })
    },
    acceptDialogComp(){
      this.closeDialogComp()
        this.loadingDialogObj.headerText = this.device.name + "(" + this.device.ip + ")"
        this.loadingDialogObj.bodyText = "Aplicando cambios en las interfaces del dispositivo"
        this.loadingDialogObj.showComponent = true
        this.loadingInterfacesResult = true
      postDeviceInterfacesAPI(this.device.id, this.changesToApply).then( (res) => {
        this.loadingInterfacesResult = false
        this.loadingDialogObj.content = res.data
        this.loadingDialogObj.status = "SUCCESS"
        this.loadingDialogObj.alertMessage = this.$t("alerts.successApply")
      }).catch(e => {
        this.loading = false;
        this.loadingInterfacesResult = false
        this.loadingDialogObj.status = "FAILED"
        this.loadingDialogObj.alertMessage = this.$t("errors.applyError")
        this.loadingDialogObj.content = e
        console.log("e => ", e)
      });
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
    this.changesToApply = []
  },
  computed: {
    items(){
      return {
        headers: [
          { text: this.$t("tasks.interfacesTask.signal"), value: "signal" },
          { text: this.$t("tasks.interfacesTask.name"), value: "name" },
          { text: this.$t("tasks.interfacesTask.status"), value: "status" },
          { text: this.$t("tasks.interfacesTask.link"), value: "link" },
          { text: this.$t("tasks.interfacesTask.action"), value: "action" },
          { text: this.$t("tasks.interfacesTask.description"), value: "description" }
        ],
        searchLabel: this.$t("global.searchMessage"),
      }
    }
  },
  watch: {
    showComponent(value){
      if(value){
        this.loadInterfaces()
      }
    },
    editedInterfacesList:{
      handler(){
        this.changesDetected = false
        this.editedInterfacesList.forEach(item => {
          var original = this.interfacesList.find(newItem => newItem.name === item.name )
          if(this.device.vendor.toLowerCase() === "juniper"){
            if( (item.status.toLowerCase() === "up" && item.action==false) ||   
              (item.status.toLowerCase() === "down" && item.action==true) ||
              (original.description !== item.description) ){
                this.changesDetected = true
            }  
          }else if(this.device.vendor.toLowerCase() === "cisco"){
            if( (!item.status.toLowerCase().includes("admin") && item.action==false) ||   
              (item.status.toLowerCase().includes("admin") && item.action==true) ||
              (original.description !== item.description) ){
                this.changesDetected = true
            } 
          }
          
        });
      },
      deep: true
    }
  }
}
</script>

<style lang="scss" scoped>
.interfacesDialog{
  display: flex;
  justify-content: center;
  flex-direction: column;
  overflow-y: unset;
  &-header{
    color: #003245;
  }
  &-table {
    margin-bottom: 2rem;
    ::v-deep td:nth-child(1) {
      width: 6rem;
    }
    ::v-deep td:nth-child(2) {
      width: 8rem;
    }
    ::v-deep td:nth-child(3) {
      width: 6rem;
    }
    ::v-deep td:nth-child(4) {
      width: 6rem;
    }
    &:first-child{
      margin-bottom: 0rem;
    }
    &-select{
      margin-bottom: 0rem;
      font-size: 0.875rem;
      width: 10rem;
    }
    &-textfield{
      margin-bottom: 0rem;
      font-size: 0.875rem;
    }
  }
  &-buttons {
    width: 100%;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
}
.device-button {
  margin: 10px;
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
.loading{
  display: flex;
  justify-content: center;
  padding: 2rem;
}
h3 {
  margin: 10px;
  margin-left: 20px;
}

.selectText {
  padding-top: 0.5rem;
  ::v-deep .v-select__selection--comma {
    font-size: .875rem;
  }
}

::v-deep .editedItem {
  background-color: oldlace;
  color: orange;
  &:hover{
    background-color: bisque !important;
  }
}
</style>