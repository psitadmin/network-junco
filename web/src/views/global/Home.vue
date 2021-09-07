<template>
  <div class="home">
    <HomeComp :msg="$t('global.helloMessage')"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HomeComp from '@/components/global/HomeComp.vue'

export default {
  name: 'Home',
  components: {
    HomeComp
  }
}
</script>

<style lang="scss" scoped>

</style>

