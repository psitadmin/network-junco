<template>
  <v-app>
    <div id=app class="header">
      <MainHeader v-if="!$route.path.includes('login')" />
    </div>
    <div id=body>
      <div class="body-menuBar">
        <MenuBar v-if="!$route.path.includes('login')" />
      </div>
      <div class="body-content">
        <router-view/>
        <!-- <div :style="{backgroundImage: url('@/assets/imgaes/logo-junco-dark.png')}"></div> -->
      </div>
    </div>
  </v-app>
</template>

<script>
import MainHeader from '@/components/global/MainHeader.vue'
import MenuBar from '@/components/global/MenuBar.vue'

export default {

  components: {
    MainHeader,
    MenuBar
  }
  
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  padding-top: 1.5em;
    
}
#body {
  display:flex;
  height: 100%;
}
.body-content {
  display:flex;
  width: 100%;
  padding: 1em;
}
</style>
