<template>
  <div class="applyConfiglets">
    <h1> Configlet {{configletId}}: {{configletData && configletData['name']}} </h1>
    <h2> <i> {{configletData && configletData['description']}} </i> </h2>
    <br>
    <h3> {{ $t('configlet.applicableDevices')}} </h3>
    <div class="applyConfiglets-table">
      <!-- Shows avaliable devices table to apply config -->
      <SelectTableComp
        :loading="loading"
        :tableHeaders="items.headers"
        :tableItems="applicableDevices"
        @selectedItems="bindSelectedDevices"
      ></SelectTableComp>
    </div>
    
    <!-- Displays alert message whenever backend actions occurs -->
    <AlertComponent
      :showAlert="showAlert"
      :message="alertMessage"
      :type="alertType"
    ></AlertComponent>
    <div class="button-table">
      <!-- Left buttons -->
      <div class="button-table-left">
        <v-btn
          data-test="configlet-apply-button"
          margin=10px
          :disabled="!someSelected"
          color="#003245"
          class="configlet-button"
          @click="showConfigletData()"
        > {{ $t('configlet.configletComp.messageButton') }} </v-btn>
      </div>
      <!-- Right buttons -->
      <div class="button-table-right">
        <v-btn
          data-test="configlet-apply-button"
          margin=10px
          :disabled="!devicesToApply"
          color="green"
          class="configlet-button"
          @click="validateConfigletData()"
        > {{ $t('configlet.validateConfiglet') }} </v-btn>
      </div>
    </div>

    <!-- Table to edit configlet data -->
    <div class="editConfiglet">
      <v-card
        v-if="devicesToApply"
      >
        <v-tabs 
          v-model="configletParams"
          slider-color="#003245"
          center-active
        >
          <v-tab
            v-for="dev in devicesToApply"
            :key="dev['id']"
          >
            {{ dev.name }}      
            <v-btn
              class="close-button"
              text
              @click="unselect(dev)"
            >
              <v-icon>mdi-close-circle</v-icon>
            </v-btn>
          </v-tab>
          <v-tab-item 
            class="configletTab"
             v-for="dev in devicesToApply"
            :key="dev['id']"
          >
            <div class="configletForm">
              <v-form
                v-model="dev.dataToValidate"
              >
                <div
                  class="configletForm-rowContainer"
                  
                  v-for="param in configletData['cli-configlet-params']['cli-configlet-param']"
                  :key="param['id']"
                >
                  <div class="configletForm-rowContainer-formLabel">
                    {{param['display-name']}}
                  </div>
                  <div
                    class="configletForm-rowContainer-formInput"
                    v-if="configletData['cli-configlet-params']['cli-configlet-param'].length"
                  >
                    <v-text-field
                      v-model="configletDataToApply[dev.id]['params'][param['id']]['value']"
                      required
                      :hint="param['description']"
                      :label="param['parameter']"
                    ></v-text-field>
                  </div>
                </div>
              </v-form>
            </div>
          </v-tab-item>
        </v-tabs>
      </v-card>
    </div>
    

    <PagesDialogComp
      :name="configletData.name"
      :pagesAction="'devices'"
      :loading="loadingValidateData"
      :dialogObjPages="configletValidation"
      @confirmDialog="sendApplyData"
      @closeDialog="closeValidateComp"
    ></PagesDialogComp>
  </div>
</template>

<script>
import {getConfigletsDataJUNOS, getApplicableDevicesJUNOS, validateConfigletJUNOS, getValidateResultJUNOS, applyConfigletJUNOS} from '@/api/junos.js'
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'
import SelectTableComp from '@/components/utilityComponents/SelectTableComp.vue'
import PagesDialogComp from '@/components/utilityComponents/PagesDialogComp.vue'
import validateTemplate from '@/assets/configlets/validate-configlets.json'
import applyTemplate from '@/assets/configlets/apply-cli-configlet.json'

export default{
  name: 'ApplyConfiglet',
  components: {
    AlertComponent,
    SelectTableComp,
    PagesDialogComp,
  },
  data(){
    return {
      configletId: this.$route.params.id,
      configletParams: null, 
      configletData: {},
      loading: false,
      loadingValidateData: false,
      applicableDevices: [],
      selectedDevices: [],

      // Tabs to edit configlet
      devicesToApply: null,
      configletDataToApply: {},


      // ConfigletValidation
      configletValidation: {
        showComponent: false,
        action: "",
        headerText: "",
        bodyText: "",
        pages: [],
        disableValidation: false,
      },

      // Alert component
      showAlert: false,
      alertMessage: '',
      alertType: 'info',
    }
  },
  computed: {
    items(){
      return {
        headers: [
          { text: this.$t("configlet.configletComp.headers.idHeader"), value: "id" },
          { text: this.$t("configlet.configletComp.headers.nameHeader"), value: "name" },
          { text: "IP", value: "ip-address" },
          { text: this.$t("configlet.configletComp.headers.domainHeader"), value: "domain-name" },
          { text: this.$t("configlet.configletComp.headers.deviceTypeHeader"), value: "device-family" },
          { text: this.$t("configlet.configletComp.headers.platform"), value: "platform" },
          { text: this.$t("configlet.configletComp.headers.osVersion"), value: "os-version" },
        ],
      }
    },
    someSelected(){
      return this.selectedDevices.length >= 1
    },
  },
  
  methods: {

    //===========================================
    // Table component data methods
    //===========================================
    bindSelectedDevices(value) {
      this.selectedDevices = value;
    },

    //===========================================
    // Methods to edit configlet data
    //===========================================
    showConfigletData(){
      this.devicesToApply = JSON.parse(JSON.stringify(this.selectedDevices))
      this.configletDataToApply = {}
      
      this.devicesToApply.forEach(dev => {
        this.$set(this.configletDataToApply, dev.id, {})
      })
      Object.keys(this.configletDataToApply).forEach(item => {
        // Get item that matchs with item id
        let dev = this.devicesToApply.find(device => device.id == item)
        this.$set(this.configletDataToApply[item], "id", dev.id)
        this.$set(this.configletDataToApply[item], "params", [])

        if(!this.configletData["cli-configlet-params"]["cli-configlet-param"].length){
          this.configletData["cli-configlet-params"]["cli-configlet-param"] = [this.configletData["cli-configlet-params"]["cli-configlet-param"]]
        }
        this.configletData["cli-configlet-params"]["cli-configlet-param"].forEach(param => {
          // Binding param value to variables
          this.$set(this.configletDataToApply[item]['params'], param['id'], [] )
          this.$set(this.configletDataToApply[item]['params'][param['id']], 'id', param['id'] )
          this.$set(this.configletDataToApply[item]['params'][param['id']], 'value', (param["default-value"] || '') )
        })        
      })
    },
    validateConfigletData(){
      var jobResults = []
      let promises = []
      this.configletValidation.showComponent = true
      this.loadingValidateData = true

      Object.keys(this.configletDataToApply).forEach(item => {
        // Validate configlet data for every devices
        validateTemplate["validate-cli-configlet"].device["@href"] = "/api/space/device-management/devices/" + this.configletDataToApply[item]['id']
        validateTemplate["validate-cli-configlet"]["cli-configlet-params"]["cli-configlet-param"] = []
        
        // Fill configlet params template with previously added form values
        for(var param in this.configletDataToApply[item]['params']){
          validateTemplate["validate-cli-configlet"]["cli-configlet-params"]["cli-configlet-param"].push(
            {
              'parameter': {
                '@href': "/api/space/configuration-management/cli-configlets/"+this.configletId+"/cli-configlet-params/"+param
              },
              'parameter-value': this.configletDataToApply[item]['params'][param].value
            }
          )
        }
        promises.push(this.sendValidateData(validateTemplate).then((res) => {
          jobResults.push(res)
        }).catch((e) => {
          this.configletValidation.showComponent = true
          this.displayAlertTime(10, 'error', (this.$t('configlet.validatingConfigletError')+' (ID: '+ this.configletDataToApply[item]['id']+  '):\n '+e ) )
        }))
      })
      Promise.all(promises).then( () => {
        this.createValidateComp(jobResults)
        console.log(jobResults)
      }).catch( (e) => {
        console.log(e)
      })
    },
    sendValidateData(template){ 
      return new Promise((resolve, reject) => {
        // Sending data to Junos Space API
        validateConfigletJUNOS(this.configletId, template).then(res => {
          // Getting job if exists
          if(res.data.task.id != null){
            // Calls get API method until job finish. Still trying if job request is "INPROGRESS"
            let interval = setInterval( () => {
              getValidateResultJUNOS(res.data.task.id).then( res => {
                // console.log("tiempo, ", res)
                if(res.data["validate-cli-configlet-job-results"]["validate-cli-configlet-job-result"]["job-status"] != "INPROGRESS"){
                  clearInterval(interval)
                  interval = null
                  resolve(res.data["validate-cli-configlet-job-results"]["validate-cli-configlet-job-result"])
                }
              }).catch(e => {
                clearInterval(interval)
                interval = null
                return Promise.reject(e)
              })
            }, 2000);
          }
        }).catch(e => {
          reject(e)
        }); 
      })
    },
    // ==========================================


    //===========================================
    // Methods to apply configlet data
    //===========================================
    sendApplyData(){
      Object.keys(this.configletDataToApply).forEach( item => {
        applyTemplate["apply-cli-configlet-request"].device["@href"] = "/api/space/device-management/devices/"+this.configletDataToApply[item].id
        applyTemplate["apply-cli-configlet-request"].context = "/device"
        applyTemplate["apply-cli-configlet-request"]["cli-configlet-params"]["cli-configlet-param"] = []
        for(var param in this.configletDataToApply[item]['params']){
          applyTemplate["apply-cli-configlet-request"]["cli-configlet-params"]["cli-configlet-param"].push(
            {
              'parameter': {
                '@href': "/api/space/configuration-management/cli-configlets/"+this.configletId+"/cli-configlet-params/"+param
              },
              'parameter-value': this.configletDataToApply[item]['params'][param].value
            }
          )
        }
        applyConfigletJUNOS(this.configletId, applyTemplate).then( () => {
          this.displayAlertTime(5, 'success', (this.$t('configlet.applySuccess')))
        }).catch( (e) => {
          console.log("Applying configlet error => ", e)
          this.displayAlertTime(10, 'error', (this.$t('configlet.applyError')+' '+ e ) )
        })
      })
      this.closeValidateComp()
      this.closeEditConfiglet()
    },
    // ==========================================
    unselect(device){
      if(this.devicesToApply.includes(device)){
        this.devicesToApply[this.devicesToApply.indexOf(device)].dataToValidate=null
        this.devicesToApply.splice( this.devicesToApply.indexOf(device), 1 );
        delete this.configletDataToApply[device.id]
      }
      if(this.devicesToApply.length < 1){
        this.devicesToApply = null
      }
    },

    //===========================================
    // Component methods
    //===========================================
    createValidateComp(jobResults){
      var isValid = false
      if(jobResults.length > 0){
        if(jobResults.some(job => job["job-status"] === "FAILED" )){
          isValid = true
        }
        this.loadingValidateData = false
        this.configletValidation.disableValidation = isValid
        this.configletValidation.headerText = this.configletData.name
        this.configletValidation.bodyText = this.$t("configlet.confirmApply")
        this.configletValidation.action = 'confirm'
        this.configletValidation.pages = jobResults
        this.configletValidation.showComponent = true
        // console.log("Tenemos que meter: ", jobResults, this.configletValidation)
      }else{
        this.loadingValidateData = false
        this.configletValidation.showComponent = false
        this.closeValidateComp()
      }
    },

    // Close dialog comp
    closeValidateComp(){
      this.configletValidation.showComponent = false,
      this.configletValidation.action = ''
      this.configletValidation.headerText = ''
      this.configletValidation.bodyText = ''
      this.configletValidation.pages = []
    },
    closeEditConfiglet(){
      this.devicesToApply = null
    },

    //===========================================
    // JUNOS API METHODS
    //===========================================
    getApplicableDevices(){
      getApplicableDevicesJUNOS(this.configletId).then(res=>{
        this.applicableDevices = res.data["applicable-devices"]["applicable-device"]
      })
    },
    getConfigletsData(){
      getConfigletsDataJUNOS(this.configletId).then( res=>{
        this.configletData = res.data["cli-configlet"]
      }).catch(e => {
        this.loading = false;
        console.log(e)
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
    },
  },

  mounted(){
    this.getConfigletsData()
    this.getApplicableDevices()
  },
}
</script>

<style lang="scss" scoped>
.configlets{
  width: 100%;
  margin-right: 4rem;
}
.applyConfiglets{
  width: 50%;
}
.configletTable {
  width: 100%;
}
.configletForm{
  // display: flex;
  width: 100%;
  justify-content: center;
  &-rowContainer{
    display: flex;
    width: 100%;
    align-items: baseline;
    &-formLabel{
      width: 30%;
      text-align: right;
      margin-right: 2rem;
    }
    &-formInput{
      width: 40%;
      // text-align: left;
      margin-left: 2rem;
      margin-right: 2rem;
    }
    // flex-direction: column;
    justify-content: space-around;
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
.button-table {
  display: flex;
  justify-content: space-between;
  &-left {
    justify-content: flex-start;
  }
  &-right {
    justify-content: flex-end;
  }
}
.configlet-button {
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
.device-button {
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
.formLabel{
    justify-content: flex-start;
}
.formInput{
    justify-content: flex-end;
}
</style>






