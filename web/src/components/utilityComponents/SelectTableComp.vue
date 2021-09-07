<template>
  <v-data-table
    data-test="configlet-table"
    width=100%
    v-model="selected"
    :headers="tableHeaders"
    :items="tableItems"
    :loading="loading"
    :loading-text="$t('global.loadingText')"
    item-key="id"
    show-select
    :search="searchText"
    fixed-header
    dense
  >
    <template v-slot:top>
      <v-text-field
        data-test="configlet-search-bar"
        v-model="searchText"
        :label="items.searchLabel"
      ></v-text-field>
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: 'SelectTableComp',
  data(){
    return{
      searchText: '',
      selected: [],
    }
  },
  props: {
    loading: Boolean,
    tableItems: Array,
    tableHeaders: Array,
  },
  computed: {
    items () {
      return {
        // Table search bar
        searchLabel: this.$t("global.searchMessage"),
      }
    },
  },
  methods:{
    resetSelected(){
      this.selected = []
    }
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