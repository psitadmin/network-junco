<template>
  <div class="arp">
    <h3> {{ $t('arpTables.messageARP')}} </h3>
    <div class="arp-input">
      <div class="arp-input-find">
        <div class="loginLabel">
          {{ $t('arpTables.arpSearch') }}:
        </div>
        <div class="arp-input-buttons">
          <v-text-field
            v-model="searchData"
            :disabled="showARP"
            :label="$t('arpTables.arpInput')" 
            clearable
            solo
            rounded
            filled
            required
          ></v-text-field>
          <v-btn
            v-if="showARP"
            rounded
            fab
            :title="$t('global.refresh')"
            color="green"
            class="search-button"
            @click="showARP=false"
            ><v-icon>mdi-refresh</v-icon>  </v-btn>
          <v-btn
            v-else
            rounded
            fab
            :title="$t('global.searchLabel')"
            color="#003245"
            class="search-button"
            @click="sendARPData"
          ><v-icon>mdi-magnify</v-icon></v-btn>

          
          <!-- <v-btn
            rounded
            fab
            :title="$t('global.searchLabel')"
            color="#003245"
            class="search-button"
            @click="arpOptions"
          ><v-icon>mdi-menu</v-icon></v-btn> -->
          <v-menu 
            offset-x
            transition="scale-transition"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                rounded
                fab
                :title="$t('global.searchLabel')"
                color="#003245"
                class="search-button"
                v-bind="attrs"
                v-on="on"
              ><v-icon>mdi-menu</v-icon></v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, index) in arpOptionsMenu"
                :key="index"
                @click="optionsController(item)"
                link
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        
        </div>
      </div>
    </div>
    
    <ARPConfComp
      :arpConfObj="arpConfObj"
      :loading="arpConfLoading"
      @closeDialog="closeARPConfController"
    ></ARPConfComp>
    <ARPTablesComp
      v-if="showARP"
      :deviceFound="deviceFound"
      :addressFound="addressFound"
    ></ARPTablesComp>
    
    <AlertComponent
      :showAlert="showAlert"
      :message="alertMessage"
      :type="alertType"
    ></AlertComponent>
    
  </div>
</template>
<script>
import ARPTablesComp from '@/components/arptables/ARPTablesComp.vue'
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'
import ARPConfComp from '@/components/arptables/ARPConfComp.vue'
import {resolveARPAPI} from '@/api/arp.js'
import {formatAddress} from '@/utils/functions.js'

export default {
  name: 'ARPTables',
  components: {
    ARPTablesComp,
    AlertComponent,
    ARPConfComp,
  },
  data() {
    return {
      searchData: '',
      showARP: false,
      loading: false,
      deviceFound: [],
      addressFound: [],
      alertMessage: '',
      alertType: 'info',
      showAlert: false,
      
      // ARP options menu
      arpOptionsMenu: [
        {title: this.$t('arpTables.arpConf.transitInterfacesConf.transitInterfaces'), action: 'transit_interfaces'},
        {title: 'OTHER', action: 'other'},
      ],

      // ARP config component
      arpConfLoading: false,
      arpConfObj: {
        action: '',
        headerText: '',
        buttons: [],
        showComponent: false
      }
    }
  },
  methods: {
    // ==========================
    // ARP SEARCH METHODS
    // ==========================
    sendARPData(){
      var data = formatAddress(this.searchData)
      if(data){
        this.loading = true
        resolveARPAPI(data).then(res=>{
          this.deviceFound = res.data.device_found
          this.addressFound = res.data.addresses
          this.showARP = true
        }).catch(e => {
          this.loading = false
          if(e.response){
            if(e.response.status == 500){
              this.displayAlertTime(5, "error", this.$t('errors.databaseError'))
              console.log("e => ", typeof(e), e.response)
            }else{
              this.displayAlertTime(5, "error", this.$t('arpTables.arpNotFound'))
              console.log("e => ", typeof(e), e.response)
            }
          }else{
            this.displayAlertTime(5, "error", this.$t('errors.databaseError'))
          }
        });
      }else{
        this.displayAlertTime(5, "warning", this.$t('arpTables.arpInvalid'))
      }
    },
    
    // ==========================
    // COMPONENTS SEARCH METHODS
    // ==========================
    closeARPConfController(action){
      switch(action){
        case "transit_interfaces":
          this.arpConfObj.action = ''
          this.arpConfObj.headerText = ''
          this.arpConfObj.buttons = []
          this.arpConfObj.showComponent = false
          break;
        default:
          this.arpConfObj.action = ''
          this.arpConfObj.headerText = ''
          this.arpConfObj.buttons = []
          this.arpConfObj.showComponent = false
          break;
      }
    },
    optionsController(item){
      switch(item.action){
        case "transit_interfaces":
          this.arpOptions()
          break;
        default:
          this.arpConfObj.showComponent = true
          this.arpConfObj.action = ""
          break;
      }
    },
    arpOptions(){
      this.arpConfObj.showComponent = true
      this.arpConfObj.action = "transit_interfaces"
    },
    closeARPDialog(){
      this.arpConfObj.showComponent = false
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
}
</script>

<style lang="scss" scoped>
.arp {
  &-input{
    &-find{
      width: 30rem;
    }
    &-tables{
      width: 1rem;
    }
    &-buttons{
      margin-top: 1rem;
      display: flex;
    }
  }
}
.search-button {
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff;
  }
}
</style>
