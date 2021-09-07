<template>
  <div class="config-table"
  >
    <v-card
      v-if="showConfig"
      :loading="loadingConfig"
      :loading-text="$t('global.loadingText')"
    >
      <v-tabs 
        v-model="configs"
        slider-color="#003245"
        center-active
      >
        <v-tab
          :key="title"
        >
          {{ title }}      
          <v-btn
            class="close-button"
            text
            @click="unselect(item['id'])"
          >
            <v-icon>mdi-close-circle</v-icon>
          </v-btn>
        </v-tab>
        <v-tab-item class="config-item"
          :key="title"
        >
          <v-card class="card-config">
            <v-btn class="scroll-on-top-button"
              v-if="scrolled"
              ref="onTopBtn"
              fab
              bottom
              right
              dark
              color="#003245"
              @click="toTop"
            >
            <v-icon>mdi-arrow-collapse-up</v-icon>
            </v-btn>
            <v-card-text
              ref="textPosition"
              class="config-text"
            >
              {{ data }} 
            </v-card-text> 
          </v-card>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </div>
  
</template>

<script>
// import toJson from 'xml-js'

export default {
  name: 'ShowConfigComponent',  
  data() {
    return {
      configs: null,
      scrolled: false,
    }
  },
  props: {
    item: Object,
    title: String,
    data: String,
    showConfig: Boolean,
    loadingConfig: Boolean,
  },
  computed: {
    textPosition(){
      return this.$refs.textPosition ? this.$refs.textPosition.scrollTop : null
    },
  },
  methods: {
    unselect() {
      this.$emit("unselectItem")
      this.$refs.textPosition.removeEventListener("scroll", this.onScroll)
    },
    onScroll() {
      if(this.$refs.textPosition.scrollTop >= 10){
        this.scrolled = true;
      } else {
        this.scrolled = false;
      }
    },
    toTop(){
      this.$refs.textPosition.scrollTop = 0;
    },
    
    // xml2string(value){
    //   var result = toJson.xml2js(value["expanded-xml-configuration"].configuration, {ignoreCdata: false})
    //   var result2 = toJson.xml2js(result.elements[0].cdata)
    //   var result = toJson.xml2js(value["expanded-xml-configuration"].configuration, {ignoreCdata: false})
    //   return result.elements[0].cdata;
    // }
  },
  mounted() {
    // this.$refs.textPosition.addEventListener("scroll", this.onScroll)
  },
  watch:{
    textPosition: {
      handler(value){
        console.log(value)
        // if(value){
        //   console.log("VALUE: ", this.$refs.textPosition) 
        //   this.$refs.textPosition.addEventListener("scroll", this.onScroll)
        // }
      }
    },
    item: {
      handler(value){
        if(value){
          // this.$refs.textPosition.addEventListener("scroll", this.onScroll)
        }
      }
    }
  }
}
</script>

<style scoped>
.config-table {
  margin-bottom: 3rem;
  margin-top: 2rem;
  width: 80%;
}
.card-config {
  position: relative;
  font-size: small;
  font-family:"Courier New", monospace;
  white-space: pre-wrap;
}
.config-text {
  overflow: scroll;
  height: 35rem;
}
.scroll-on-top-button {
  position: absolute;
  bottom: 1.2rem;
  right: 1.2rem;
}
</style>