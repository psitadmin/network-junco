<template>
  <div class="configlets">
    <h3> {{ $t('configlet.messageConfiglet')}} </h3>
    <v-checkbox
      data-test="configlet-default-button"
      v-model="checkboxConfiglets"
      :label="$t('configlet.configletComp.showDefault')"
      color="#003245"
      hide-details
    />
    <div class="table-comp">
      <!-- Shows configlet table -->
      <SelectTableComp
        :loading="loading"
        :tableHeaders="headers"
        :tableItems="newConfiglets"
        @selectedItems="bindSelectedConfiglets"
        ref="SelectTableComp"
      ></SelectTableComp>
    </div>

    <DialogComp
      :dialogObj="dialogCompObj"
      @closeDialog="closeDialogComp"
      @acceptDialog="acceptDialogComp"
    ></DialogComp>

    <div class="button-table">
      <!-- Left buttons -->
      <div class="button-table-left">
        <v-btn
          data-test="show-config-button"
          margin=10px
          color="#003245"
          class="configlet-button"
          :disabled="!selectedLenght"
          :title="$t('global.seeConfig')"
          @click="seeConfigletConfig()"
        > {{$t('global.seeConfig')}} </v-btn>
        <v-btn
          data-test="configlet-apply-button"
          margin=10px
          :disabled="!selectedLenght"
          color="#003245"
          class="configlet-button"
          @click="applyConfiglets()"
        > {{ $t('configlet.configletComp.messageButton') }} </v-btn>
      </div>
      <!-- Right buttons -->
      <div class="button-table-right">
        <v-btn
          margin=10px
          color="red"
          class="device-button"
          :disabled="!someSelected"
          :title="$t('devices.deviceComp.deleteDevice')"
          @click="deleteBtn()"
        > <v-icon>mdi-delete</v-icon> </v-btn>
        <v-btn
          margin=10px
          color="green"
          class="device-button"
          :title="$t('global.refresh')"
          @click="getConfiglets()"
        > <v-icon>mdi-refresh</v-icon> </v-btn>  
      </div>
    </div>

    <!-- Shows configlet's configuration -->
    <ShowConfigComponent
      :showConfig="showConfig"
      :loadingConfig="loadingConfig"
      :title="configTitle"
      :item="configItem"
      :data="configData"
      @unselectItem="showConfig=null, configData=null"
    ></ShowConfigComponent>
    
    <!-- Displays alert message whenever backend actions occurs -->
    <AlertComponent
      :showAlert="showAlert"
      :message="alertMessage"
      :type="alertType"
    ></AlertComponent>
  </div>
</template>

<script>
import {getConfigletsJUNOS, deleteConfigletJUNOS, getConfigletsDataJUNOS} from '@/api/junos.js'
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'
import SelectTableComp from '@/components/utilityComponents/SelectTableComp.vue'
import DialogComp from '@/components/utilityComponents/DialogComp.vue';
import ShowConfigComponent from '@/components/utilityComponents/ShowConfigComponent.vue';

export default{
  name: 'Configlets',
  components:{
    AlertComponent,
    SelectTableComp,
    DialogComp,
    ShowConfigComponent,
  },
  data(){
    return {
      checkboxConfiglets: true,
      configletList: [],
      loading: false,
      selectedConfiglets: [],
      showAlert: false,
      alertMessage: '',
      alertType: 'info',

      // ShowConfigComponent props
      showConfig: false,
      loadingConfig: false,
      configTitle: '',
      configItem: null,
      configData: '',

      headers: [
        { text: this.$t("configlet.configletComp.headers.idHeader"), value: "id" },
        { text: this.$t("configlet.configletComp.headers.nameHeader"), value: "name" },
        { text: this.$t("configlet.configletComp.headers.domainHeader"), value: "domain-name" },
        { text: this.$t("configlet.configletComp.headers.deviceTypeHeader"), value: "device-family" },
        { text: this.$t("configlet.configletComp.headers.descriptionHeader"), value: "description" },
        { text: this.$t("configlet.configletComp.headers.execTypeHeader"), value: "execution-type" },
        { text: this.$t("configlet.configletComp.headers.creationHeader"), value: "creation-time" },
        { text: this.$t("configlet.configletComp.headers.updateHeader"), value: "last-updated-time" },
        { text: this.$t("configlet.configletComp.headers.modifiedHeader"), value: "last-modified-by" },
      ],
      
      // DialogComp props
      dialogCompObj: {
        headerText: String,
        bodyText: String,
        buttons: Array,
        showComponent: false,
      },
      activeObj: true,

      // Array with only certain configlets
      newConfiglets: [],
    }
  },
  methods: {
    resetSelectedComp(){
      this.$refs.SelectTableComp.resetSelected()
    },
    // Catch the event emitted by component and calls appropiate method
    acceptDialogComp(ev, configlet){
      switch (ev) {
        case "delete":  
          this.deleteConfiglets(this.selectedConfiglets)
          this.resetSelectedComp()
          this.getConfiglets()
          break;
        default:
          console.log("UNKNOW ACTION DIALOG ACCEPT", configlet)
      }
      // Closes and reset DialogComp content
      this.closeDialogComp()
    },
    // Flush all dialogCompObj attributes and delete component
    closeDialogComp(){
      this.dialogCompObj.showComponent = false
      this.dialogCompObj.action = ''
      this.dialogCompObj.headerText = ''
      this.dialogCompObj.bodyText = ''
      this.dialogCompObj.headers = []
      this.dialogCompObj.items = []
      this.dialogCompObj.buttons = []
    },
    deleteBtn() {
      // Create deleteComponent
      this.dialogCompObj.action = "delete"
      this.dialogCompObj.headerText = this.$t("devices.deviceComp.cards.deleteTitle")
      this.dialogCompObj.bodyText = this.$t("devices.deviceComp.cards.deleteText")
      this.dialogCompObj.showComponent = true
      this.dialogCompObj.items = this.selectedConfiglets
      this.dialogCompObj.headers = [
        { text: this.$t("configlet.configletComp.headers.idHeader"), value: "id" },
        { text: this.$t("configlet.configletComp.headers.nameHeader"), value: "name" },
        { text: this.$t("configlet.configletComp.headers.descriptionHeader"), value: "description" },
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
    getSelectedConfiglets(value) {
      this.selectedConfiglets = value;
    },
    bindSelectedConfiglets(value) {
      this.selectedConfiglets = value;
    },
    // ==================================================================
    // BUTTON METHODS
    // ==================================================================
    getConfiglets(){
      this.loading = true;
      return getConfigletsJUNOS().then(res=>{
        this.configletList = res.data["cli-configlets"]["cli-configlet"];
        this.loading = false;
      }).catch(e => {
        this.loading = false;
        console.log(e)
      });
    },
    deleteConfiglets(configlets){
      try{
        for (let c in configlets){
          deleteConfigletJUNOS(configlets[c].id).then( () => {})
        }
        this.loading = false
        this.getConfiglets()
        this.displayAlertTime(3, 'success', this.$t('alerts.successDeletingItem'))
      }catch(error){
        console.log(error)
      }
    },
    seeConfigletConfig(){
      this.showConfig = true
      this.loadingConfig = true
      this.configItem = this.selectedConfiglets[0]
      this.configTitle = this.selectedConfiglets[0].name
      this.configData = ""
      getConfigletsDataJUNOS(this.selectedConfiglets[0].id).then( res=>{
        this.configData = JSON.stringify(res.data["cli-configlet"]["cli-configlet-params"]["cli-configlet-param"],null, 2)
        this.loadingConfig = false
      }).catch(e => {
        this.loading = false;
        console.log(e)
      });
    },
    applyConfiglets(){
      this.$router.push({
        path: `/configlets/${this.selectedConfiglets[0].id}`
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
  computed: {
    someSelected(){
      return this.selectedConfiglets.length >= 1
    },
    selectedLenght() {
      return this.selectedConfiglets.length === 1;
    },
  },
  watch: {
    checkboxConfiglets(value) {
      if(value){
        this.newConfiglets = this.configletList
      } else {
        this.newConfiglets = this.configletList.filter(item => item.id > 16)
      }
    },
    configletList: {
      handler(value) {
        this.newConfiglets = value
      }, deep: true
    },
  },
  mounted(){
    this.getConfiglets();
  },
};
</script>

<style lang="scss" scoped>
.configlets{
  width: 80%;
  margin-right: 4rem;
}
.table-comp {
  width: 100%;
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
  min-width: unset !important;
  height: 36px;
  width: 40px;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
</style>






