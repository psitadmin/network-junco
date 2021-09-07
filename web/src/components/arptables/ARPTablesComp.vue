<template>
  <div class="arp-comp">
    <div class="arp-data">
      <h3>
        {{ $t('arpTables.arpComp.findData') }}{{ arpData }}
      </h3>
      <div class="table1">
        <v-data-table class="arp-table"
          data-test="device-table"
          width=100%
          :headers="items.headers1"
          hide-default-footer
          :items="deviceFound"
          :loading-text="$t('global.loadingText')"
          item-key="device-id"
          fixed-header
          dense
        ></v-data-table>
      </div>

      <div class="table2"
        v-if="addressFound.length"
      >
        <h3>
          {{ $t('arpTables.arpComp.result') }}
        </h3>
        <v-data-table class="arp-table"
          data-test="device-table"
          width=100%
          :headers="items.headers2"
          hide-default-footer
          :items="addressFound"
          :loading="loading"
          :loading-text="$t('global.loadingText')"
          item-key="device-id"
          fixed-header
          dense
        ></v-data-table>
      </div>
      <div 
        v-else
      >
        <h3 class="errorText">
          {{ $t('arpTables.arpEmpty1') }} [IP: {{deviceFound[0].ip}}; MAC: {{deviceFound[0].mac}}] {{ $t('arpTables.arpEmpty2') }}
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ARPTablesComp",
  data(){
    return {
      arpRequest: {},
    }
  },
  computed: {
    items() {
      return {
        headers1: [
          { text: this.$t("arpTables.arpComp.headers.ip"), value: "ip" },
          { text: this.$t("arpTables.arpComp.headers.mac"), value: "mac" },
          { text: this.$t("arpTables.arpComp.headers.name"), value: "name" },
          // { text: this.$t("arpTables.arpComp.headers.network"), value: "net" },
          { text: this.$t("arpTables.arpComp.headers.date"), value: "date" },
        ],
        headers2: [
          { text: this.$t("arpTables.arpComp.headers.device"), value: "device_name" },
          { text: this.$t("arpTables.arpComp.headers.ip"), value: "ip" },
          { text: this.$t("arpTables.arpComp.headers.vendor"), value: "vendor" },
          { text: this.$t("arpTables.arpComp.headers.interface"), value: "interface" },
          { text: this.$t("arpTables.arpComp.headers.interfaceDescription"), value: "interface_description" },
          { text: this.$t("arpTables.arpComp.headers.vlan"), value: "vlan" },
          { text: this.$t("arpTables.arpComp.headers.date"), value: "date" },
        ]
      }
    }
  },
  methods: {
    findARPData(addresARPData){
      this.arpRequest = addresARPData;
      console.log(1, this.arpRequest)
    }
  },
  mounted(){
    this.arpRequest = null;
  },
  props: {
    arpData: String,
    loading: Boolean,
    deviceFound: Array,
    addressFound: Array,
  },
};
</script>

<style lang="scss" scoped>
.arp-table {
  margin-bottom: 3rem;
  margin-top: 1rem;
  border-left: 1px solid #003245;
  border-bottom: 1px solid #003245;
  ::v-deep .v-data-table__wrapper thead th {
      font-size: 13pt !important;;
      color: #003245 !important;
  }
  ::v-deep .v-data-table__wrapper tbody td {
    font-size: 13pt !important;
    font-family:"Courier New", monospace;
  }
}
.errorText{
  color:red;
}
</style>