<template>
  <div class="deviceTable">
    <div class="searchBar">
      <v-data-table
        class="table"
        data-test="device-table"
        width=100%
        v-model="selected"
        :headers="items.headers"
        :items="deviceList"
        :loading="loading"
        :loading-text="$t('global.loadingText')"
        item-key="device-id"
        show-select
        :search="searchText"
        fixed-header
        dense
      >
        <template 
          class="status"
          v-slot:[`item.connectionStatus`]="{ item }"
        >
          <v-icon
            small
            :color="getColor(item.connectionStatus)"
          > mdi-circle </v-icon>
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
    </div>
  </div>
</template>

<script>
export default {
  
  name: 'DeviceComp',
  data() {
    return {
      searchText: '',
      selected: [],
    }
  },
  computed: {
    items() {
      return {
        headers: [
          { text: this.$t("devices.deviceComp.headers.statusHeader"), value: "connectionStatus" },
          { text: this.$t("devices.deviceComp.headers.nameHeader"), value: "name" },
          { text: this.$t("devices.deviceComp.headers.ipHeader"), value: "ipAddr" },
          { text: this.$t("devices.deviceComp.headers.vendorHeader"), value: "deviceFamily" },
          { text: this.$t("devices.deviceComp.headers.serialNumberHeader"), value: "serialNumber" },
          { text: this.$t("devices.deviceComp.headers.platformHeader"), value: "device_model" },
          { text: this.$t("devices.deviceComp.headers.idHeader"), value: "device-id" },
          { text: this.$t("devices.deviceComp.headers.osVersionHeader"), value: "OSVersion" },  
        ],
        searchLabel: this.$t("global.searchMessage"),
      }
    },
    selectedLenght() {
      return this.selected.length === 1;
    },
  },
  methods: {
    addDevice() {
      console.log(1,"addDevice", this.selected)
    },
    deleteDevice() {
      console.log(2,"deleteDevice", this.selected)
    },
    applyConfig() {
      console.log("JUNOOOS",this.selected)
      this.$router.push({
        path: `/junosdevices/${this.selected[0]["device-id"]}`
      });
    },
    seeConfig() {
      var device = this.selected[0]
      this.$emit('selectedDevice', device)
    },
    getColor(status){
      if(status.toUpperCase() === "UP"){
        return "green"
      }else{
        return "red"
      }
    }
  },
  props: {
    deviceList: Array,
    loading: Boolean,
  },
  watch: {
    selected: {
      handler(){
        this.$emit('selectedItems', this.selected)
      }, deep: true
    }
  }

}
</script>

<style lang="scss" scoped>
::v-deep tr{
  td:nth-child(2){
    width: 6rem;
  }
}
.table{
  width: 70%;
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
