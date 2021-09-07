<template>
  <v-dialog
    class="arpDialog"
    v-model="arpConfObj.showComponent"
    persistent
    max-width="800"
  >
    <v-card>
      <div class="arpDialog-headers">
        <v-card-title class="headline"> {{arpConfObj.header}} </v-card-title>
      </div>
        <div class="arpDialog-loading"
          v-if="loading"
        >
          <v-progress-circular
            class="loading-item"
            :size="50"
            indeterminate
            color="primary"
          ></v-progress-circular>
        </div>
        <div class="arpDialog-content"
          v-else
        >
          <!-- TRANSIT INTERFACES MODE -->
          <v-card-text v-if="arpConfObj.action==='transit_interfaces'">
            <!-- Transit interfaces table -->
            <v-form
              ref="form"
              v-model="valid"
            >
            <v-data-table
              class="arpDialog-content-table"
              :item-class="getBackgroundColor"
              :headers="transitHeaders"
              :items="editedTransitInterfaces"
              hide-default-footer
              fixed-header
              dense
            >
              <!-- Select action item -->
              <template 
                v-slot:[`item.vendor`]="{ item }"
              > 
                <v-select
                  class="arpDialog-content-table-select"
                  v-model="item.vendor"
                  :rules="rulesSelect"
                  hide-details="true"
                  solo
                  flat
                  outlined
                  dense
                  required
                  :items="vendorList"
                ></v-select>
              </template> 
              
              <!-- Description textfield item -->
              <template 
                v-slot:[`item.transit_interface`]="{ item }"
              > 
                <v-text-field
                  class="arpDialog-content-table-textfield"
                  v-model="item.transit_interface"
                  :rules="rulesTextField"
                  hide-details="true"
                  required
                  solo
                  dense
                  append-icon="mdi-replay"
                  @click:append="restoreDescription(item)"
                ></v-text-field>
              </template>
              <template v-slot:[`item.delete`]="{ item }">
                <v-icon
                  small
                  @click="deleteTransitInterface(item)"
                > mdi-delete </v-icon>
              </template>
              </v-data-table>
            </v-form>
          </v-card-text>
        </div>
        
    <!-- Displays alert message whenever backend actions occurs -->
    <AlertComponent
      :showAlert="showAlert"
      :message="alertMessage"
      :type="alertType"
    ></AlertComponent>
      <div 
        class="arpDialog-buttons"
      >
        <v-btn
          text
          @click="closeComponent"
        >{{ $t('global.cancel') }}</v-btn> 
        <v-btn v-if="arpConfObj.action==='transit_interfaces'"
          margin=10px
          color="#003245"
          class="device-button-icon"
          :disabled="loading"
          :title="$t('global.add')"
          @click="addTransitInterface()"
        > <v-icon>mdi-plus</v-icon> </v-btn>
        
        <v-btn v-if="arpConfObj.action==='transit_interfaces'"
          margin=10px
          color="green"
          class="device-button-icon"
          :disabled="loading"
          :title="$t('global.apply')"
          @click="applyTransitInterface()"
        > <v-icon>mdi-check-circle</v-icon> </v-btn>
      </div>
    </v-card>  
  </v-dialog>
</template>
<script>
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'
import {getTransitInterfacesAPI, postTransitInterfacesAPI} from '@/api/arp.js'
import {getVendorsAPI} from '@/api/devices.js';

export default {
  props: {
    arpConfObj: Object,
  },
  components: {
    AlertComponent
  },
  data() {
    return {
      valid: true,
      transitInterfaces: [],
      editedTransitInterfaces: [],
      interfacesToDelete: [],
      interfacesToAdd: [],
      interfacesToModify: [],
      vendorList: [],
      loading: true,
      rulesTextField: [
        value => !!value || this.$t("global.requiredField"),
      ],
      rulesSelect: [
        value => !!value || this.$t("global.requiredField"),
      ],
      // Alert component
      alertMessage: '',
      alertType: 'info',
      showAlert: false,
      transitHeaders: [
        {text: this.$t('arpTables.arpComp.headers.vendor'), value: 'vendor'},
        {text: this.$t('arpTables.arpConf.transitInterfacesConf.transitInterface'), value: 'transit_interface'},
        {text: this.$t('global.delete'), value: 'delete'},
      ]
    }
  },
  methods: {
    getTransitInterfaces(){
      this.editedTransitInterfaces = []
      this.transitInterfaces = []
      this.getVendorsList()
      getTransitInterfacesAPI().then( (res) => {
        this.transitInterfaces = res.data
        this.editedTransitInterfaces = JSON.parse(JSON.stringify(res.data))
        this.loading = false
      }).catch(e => {
        this.loading = false
        this.displayAlertTime(3, "error", this.$t("arpTables.arpConf.transitInterfacesConf.error"), e)
      })
    },
    applyTransitInterface(){
      this.interfacesToAdd = []
      this.interfacesToModify = []
      this.editedTransitInterfaces.forEach( (item) => {
        if(!this.transitInterfaces.some(int => int.id === item.id)){
          this.interfacesToAdd.push(item)
        }
        var original = this.transitInterfaces.find( originalItem => originalItem.id === item.id )
        if(original && !this.interfacesToDelete.some(int => int.id === original.id)){
          if(item.transit_interface !== original.transit_interface || item.vendor !== original.vendor){
            this.interfacesToModify.push(item)
          }
        }
      })
      if(this.interfacesToAdd.length || this.interfacesToModify.length || this.interfacesToDelete.length){
        if(this.$refs.form.validate()){
          postTransitInterfacesAPI(this.interfacesToAdd, this.interfacesToModify, this.interfacesToDelete).then( () => {
            this.loading = true,
            this.interfacesToDelete = []
            this.getTransitInterfaces()
          }).catch(e => {
            this.displayAlertTime(3, "error", this.$t("errors.applyError"), e)
          })
        }else{
          this.displayAlertTime(3, "error", this.$t("errors.invalidForm"))  
        }
      }else{
        this.displayAlertTime(3, "error", this.$t("errors.noChangesError"))
      }
    },
    addTransitInterface(){
      var id
      if(this.editedTransitInterfaces.length > 0){
        id = Math.max.apply(Math, this.editedTransitInterfaces.map(o => o.id))
      }else{
        id = 0
      }
      this.editedTransitInterfaces.push({id: id+1})
    },
    deleteTransitInterface(item){
      if(this.transitInterfaces.find(int => int.id === item.id)){
        this.interfacesToDelete.push(item)
      }else{
        this.editedTransitInterfaces = this.editedTransitInterfaces.filter(int => int.id !== item.id)
      }
    },
    restoreDescription(item){
      var original = this.transitInterfaces.find(newItem => newItem.id === item.id)
      item.transit_interface = original.transit_interface
    },
    // Retrieves vendor list data from database
    getVendorsList(){
      getVendorsAPI().then(res=>{
        for (let i in res.data.data) {
          this.vendorList.push(res.data.data[i])
        }
      }).catch(e => {
        this.displayAlertTime(3, "error", e)
      });
    },
    closeComponent(){
      this.interfacesToDelete = [],
      this.interfacesToAdd = [],
      this.interfacesToModify = [],
      this.$emit('closeDialog', this.arpConfObj.action)
    },
     // =========================================================
    // Table template methods
    // =========================================================
    getBackgroundColor(item){
      var original = this.transitInterfaces.find(newItem => newItem.id === item.id )
      var deleted = this.interfacesToDelete.find(newItem => newItem.id === item.id)
      if(original){
        if(deleted){
          return 'deletedItem'
        }
        else if(original.transit_interface === item.transit_interface && original.vendor === item.vendor){
          return ''
        }
        else{
          return 'editedItem'
        }
      }else{
        if(deleted){
          return 'deletedItem'
        }else{
          return 'newItem'
        }
      }
    },
    /**
     * Configure the alert component showed
     * @param time seconds to display alert component
     * @param type the type of alert component [success, info, alert, error]
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
  },
  watch: {
    'arpConfObj.action': {
      handler(value) {
        switch(value){
          case "transit_interfaces":
            this.getTransitInterfaces()
            break;
          default:
            this.loading = true
            break;
        }
      }
    },
  }
}
</script>
<style lang="scss" scoped>
.arpDialog{
  display:flex;
  justify-content: center;
  &-loading{
    display: flex;
    justify-content: center;
  }
  &-buttons{
    width: 100%;
    margin-top: 1rem;
    padding-bottom: 1rem;
    padding-right: 1rem;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
}

::v-deep .editedItem {
  background-color: oldlace;
  color: orange;
  &:hover{
    background-color: bisque !important;
  }
}
::v-deep .newItem {
  background-color: lightgreen;
  &:hover{
    background-color: limegreen !important;
  }
}
::v-deep .deletedItem {
  background-color: salmon;
  &:hover{
    background-color: red !important;
  }
}
.device-button-icon {
  min-width: unset !important;
  height: 36px;
  width: 40px;
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}

</style>