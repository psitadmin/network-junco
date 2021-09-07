<template>
  <div class="menuBarContainer">
    <v-card class="menuBar"
    >
      <v-navigation-drawer 
        v-model="drawer"
        permanent
      >
        <v-list-item
          v-model="group"
        > 
          <v-list-item-content>
            <div class="collapse-bar">
              <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
              <v-list-item-title class="title">
                Junco
              </v-list-item-title>
            </div>
            <v-list-item-subtitle>
              {{ $t('global.selectAnOption') }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
          dense
          nav
        >
          <v-list-item
            data-test="menu-bar-item"
            v-for="item in items"
            :key="item.title"
            :to="item.link"
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      drawer: true,
      group: null,
    }
  },
  computed: {
    items () {
      return [
        { title: this.$t("menuBar.configlets"), link: '/configlets' },
        { title: this.$t("menuBar.junosDevices"), link: '/junosdevices'},
        { title: this.$t("menuBar.arpTables"), link: '/arpTables'},
        { title: this.$t("menuBar.allDevices"), link: '/alldevices'},
      ]
    }
  },
  methods: {
    prueba (){
      console.log("prueba")
    }
  },
  watch: {
    group () {
      this.drawer = false
    }
  }
}
</script>

<style lang="scss" scoped>
.collapse-bar {
  display: flex;
  justify-content: space-between;
  text-align: right;
}
.menuBarContainer {
  height: 100%;
  width: 80%
}
.menuBar {
  height: 100%;
}
</style>