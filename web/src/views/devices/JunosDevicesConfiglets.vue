<template>
  <div class="applyConfiglets">
    <h1> {{deviceData && deviceData['hostName']}} ({{deviceId}}) </h1>
    <h2> {{deviceData['ipAddr']}}</h2>
    <br>
    <h3> {{ $t('devices.applicableConfiglets')}} </h3>
    <div class="applyConfiglets-table">
      <!-- Shows avaliable devices table to apply config -->
      <SelectTableComp
        :loading="loading"
        :tableHeaders="items.headers"
        :tableItems="applicableConfiglets"
        @selectedItems="bindSelectedConfiglets"
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
          :disabled="!configletsToApply"
          color="green"
          class="configlet-button"
          @click="validateConfigletData()"
        > {{ $t('configlet.validateConfiglet') }} </v-btn>
      </div>
    </div>

    <!-- Table to edit configlet data -->
    <div class="editConfiglet">
      <v-card
        v-if="configletsToApply"
      >
        <v-tabs 
          v-model="configletParams"
          slider-color="#003245"
          center-active
        >
          <v-tab
            v-for="conf in configletsToApply"
            :key="conf['id']"
          >
            {{ conf.name }}      
            <v-btn
              class="close-button"
              text
              @click="unselect(conf)"
            >
              <v-icon>mdi-close-circle</v-icon>
            </v-btn>
          </v-tab>
          <v-tab-item 
            class="configletTab"
             v-for="conf in configletsToApply"
            :key="conf['id']"
          >
            <div class="configletForm">
              <v-form
                v-model="conf.dataToValidate"
              >
                <div class="configletForm-rowContainer"
                  v-for="param in configletDataToApply[conf['id']].params"
                  :key="param.id"
                >
                  <div class="configletForm-rowContainer-formLabel">
                    {{param['display-name']}}
                  </div>
                  <div class="configletForm-rowContainer-formInput">
                    <v-text-field
                      v-model="param.value"
                      :hint="param.description"
                      :label="param.parameter"
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
      :name="deviceData['hostName']+' '+deviceData['ipAddr']"
      :pagesAction="'configlets'"
      :loading="loadingValidateData"
      :dialogObjPages="configletValidation"
      @confirmDialog="sendApplyData"
      @closeDialog="closeValidateComp"
    ></PagesDialogComp>

  </div>
</template>

<script>
import {getDeviceDataJUNOS, getApplicableConfigletsJUNOS, getConfigletsDataJUNOS, validateConfigletJUNOS, getValidateResultJUNOS, applyConfigletJUNOS} from '@/api/junos.js'
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'
import SelectTableComp from '@/components/utilityComponents/SelectTableComp.vue'
import validateTemplate from '@/assets/configlets/validate-configlets.json'
import PagesDialogComp from '@/components/utilityComponents/PagesDialogComp.vue'
import applyTemplate from '@/assets/configlets/apply-cli-configlet.json'

export default {
  name: 'JunosDevicesConfiglets',
  components: {
    AlertComponent,
    SelectTableComp,
    PagesDialogComp,
  },
  data(){
    return {
      deviceId: this.$route.params.id,
      deviceData: {},
      selectedConfiglets: [],

      // Data table comp
      loading: false,
      applicableConfiglets: [],
      
      // Tabs to edit configlets
      configletsToApply: null,
      configletDataToApply: {},
      configletParams: null, 
      loadingValidateData: false,
      configletsLoaded: false,
      
      // ConfigletValidation
      configletValidation: {
        showComponent: false,
        action: "",
        headerText: "",
        bodyText: "",
        pages: [],
        disableValidation: false,
      },
      pagesAction: "configlets",

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
          { text: this.$t("configlet.configletComp.headers.descriptionHeader"), value: "description" },
          { text: this.$t("configlet.configletComp.headers.execTypeHeader"), value: "execution-type" },
          { text: this.$t("configlet.configletComp.headers.updateHeader"), value: "last-updated-time" },
          { text: this.$t("configlet.configletComp.headers.modifiedHeader"), value: "last-modified-by" },
        ]
      }
    },
    someSelected(){
      return this.selectedConfiglets.length >= 1
    },
  },
  methods: {
    // JUNOS API GET METHODS
    getDeviceData(){
      getDeviceDataJUNOS(this.deviceId).then( res => {
        console.log("DEVICE",res.data.device)
        this.deviceData = res.data.device
      }).catch( (e) => {
        console.log(e)
      })
    },
    getApplicableConfiglets(){
      getApplicableConfigletsJUNOS(this.deviceId).then (res => {
        this.applicableConfiglets = res.data["applicable-configlets"]["applicable-configlet"]
      })
    },
    // Get single configlet data
    getConfigletData(configletId){
      return getConfigletsDataJUNOS(configletId)
    },

    //===========================================
    // Show data methods
    //===========================================
    showConfigletData(){
      this.configletsToApply = JSON.parse(JSON.stringify(this.selectedConfiglets))
      // Clear object
      this.configletDataToApply = {}
      this.configletsLoaded = false
      this.fillConfigletsArray(this.configletsToApply)
    },
    validateConfigletData(){
      var jobResults = []
      let promises = []
      this.configletValidation.showComponent = true
      this.loadingValidateData = true

      Object.keys(this.configletDataToApply).forEach(item => {
        let newTemplate = Object.assign(validateTemplate)
        // Validate configlet data for every devices
        newTemplate["validate-cli-configlet"].device["@href"] = "/api/space/device-management/devices/" + this.deviceId
        newTemplate["validate-cli-configlet"]["cli-configlet-params"]["cli-configlet-param"] = []
        // Fill configlet params template with previously added form values
        for(var param in this.configletDataToApply[item]['params']){
            newTemplate["validate-cli-configlet"]["cli-configlet-params"]["cli-configlet-param"].push(
            {
              'parameter': {
                '@href': "/api/space/configuration-management/cli-configlets/"+item+"/cli-configlet-params/"+param
              },
              'parameter-value': this.configletDataToApply[item]['params'][param].value
            }
          )
        }
        promises.push(this.sendValidateData(newTemplate, item).then((res) => {
          jobResults.push(res)
        }).catch((e) => {
          this.displayAlertTime(10, 'error', (this.$t('configlet.validatingConfigletError')+' (ID: '+ this.configletDataToApply[item]['id']+  '):\n '+e ) )
        }))
      })
      Promise.all(promises).then( () => {
        this.createValidateComp(jobResults)
      }).catch( (e) => {
        console.log(e)
      })
    },

    //===========================================
    // Methods to validate configlet data
    //===========================================
    sendValidateData(template, configletId){ 
      return new Promise((resolve, reject) => {
        // Sending data to Junos Space API
        validateConfigletJUNOS(configletId, template).then(res => {
          // Getting job if exists
          if(res.data.task.id != null){
            // Calls get API method until job finish. Still trying if job request is "INPROGRESS"
            let interval = setInterval( () => {
              getValidateResultJUNOS(res.data.task.id).then( res => {
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
    //===========================================
    // Methods to apply configlet data
    //===========================================
    sendApplyData(){
      Object.keys(this.configletDataToApply).forEach( item => {
        var newTemplate = applyTemplate
        newTemplate["apply-cli-configlet-request"].device["@href"] = "/api/space/device-management/devices/"+this.deviceId
        newTemplate["apply-cli-configlet-request"].context = "/device"
        newTemplate["apply-cli-configlet-request"]["cli-configlet-params"]["cli-configlet-param"] = []
        for(var param in this.configletDataToApply[item]['params']){
          newTemplate["apply-cli-configlet-request"]["cli-configlet-params"]["cli-configlet-param"].push(
            {
              'parameter': {
                '@href': "/api/space/configuration-management/cli-configlets/"+this.configletDataToApply[item].id+"/cli-configlet-params/"+param
              },
              'parameter-value': this.configletDataToApply[item]['params'][param].value
            }
          )
        }
        applyConfigletJUNOS(this.configletDataToApply[item].id, applyTemplate).then( () => {
          this.displayAlertTime(5, 'success', (this.$t('configlet.applySuccess')))
        }).catch( (e) => {
          console.log("Applying configlet error => ", e)
          this.displayAlertTime(10, 'error', (this.$t('configlet.applyError')+' '+ e ) )
        })
      })
      this.closeValidateComp()
      this.closeEditConfiglet()
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
        this.configletValidation.headerText = this.deviceData.name
        this.configletValidation.bodyText = this.$t("configlet.confirmApply")
        this.configletValidation.action = 'confirm'
        this.configletValidation.pages = jobResults
        this.configletValidation.showComponent = true
      }else{
        this.loadingValidateData = false
        this.configletValidation.showComponent = false
        this.closeValidateComp()
      }
    },
    closeValidateComp(){
      this.configletValidation.showComponent = false,
      this.configletValidation.action = ''
      this.configletValidation.headerText = ''
      this.configletValidation.bodyText = ''
      this.configletValidation.pages = []
    },
    closeEditConfiglet(){
      this.configletsToApply = null
    },
    bindSelectedConfiglets(value) {
      this.selectedConfiglets = value;
    },

    //===========================================
    // Utilities
    //===========================================
    fillConfigletsArray(selectedConfiglets){
      selectedConfiglets.forEach(conf => {
        this.$set(this.configletDataToApply, conf.id, {})
      })
      let promises = []
      
      Object.keys(this.configletDataToApply).forEach(item => {
        // Get item that matchs with item id
        let conf = selectedConfiglets.find(c => c.id == item)
        this.$set(this.configletDataToApply[item], "id", conf.id)
        this.$set(this.configletDataToApply[item], "params", {})
        let params
        promises.push(this.getConfigletData(conf.id).then( res=>{
          params =  res.data["cli-configlet"]

          // If there is a single param, transform it on one-value array
          if(!params["cli-configlet-params"]["cli-configlet-param"].length){
            params["cli-configlet-params"]["cli-configlet-param"] = [params["cli-configlet-params"]["cli-configlet-param"]]
          }

          // Binding param value to variables
          params["cli-configlet-params"]["cli-configlet-param"].forEach(param => {
            delete this.configletDataToApply[item]['parms']
            this.$set(this.configletDataToApply[item]['params'], param['id'], {} )
            this.$set(this.configletDataToApply[item]['params'][param['id']], 'id', param['id'] )
            this.$set(this.configletDataToApply[item]['params'][param['id']], 'value', (param["default-value"] || '') )
            this.$set(this.configletDataToApply[item]['params'][param['id']], 'parameter', param['parameter'] )
            this.$set(this.configletDataToApply[item]['params'][param['id']], 'description', param['description'] )
            this.$set(this.configletDataToApply[item]['params'][param['id']], 'display-name', param['display-name'] )
            this.$set(this.configletDataToApply[item]['params'][param['id']], 'configured-value-xpath', param['configured-value-xpath'] )
            this.$set(this.configletDataToApply[item]['params'][param['id']], 'order', param['order'] )
          })
        }))
      })
      Promise.all(promises).then( () => {
        
      }).catch( (e) => {
        console.log(e)
      })

      this.configletsLoaded = true

    },
    unselect(configlet){
      if(this.configletsToApply.includes(configlet)){
        this.configletsToApply[this.configletsToApply.indexOf(configlet)].dataToValidate=null
        this.configletsToApply.splice(this.configletsToApply.indexOf(configlet),1)
        // Deleteing created object
        delete this.configletDataToApply[configlet.id]
      }
      if(this.configletsToApply.length < 1){
        this.configletsToApply = null
      }
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
    this.getDeviceData()
    this.getApplicableConfiglets()
  },
}
</script>



<style lang="scss" scoped>
.applyConfiglets{
  width: 50%;
}
.configlets{
  width: 100%;
  margin-right: 4rem;
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