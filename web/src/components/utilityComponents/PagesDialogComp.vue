<template>
  <v-dialog
    class="PagesDialog"
    v-model="dialogObjPages.showComponent"
    persistent
    max-width="800"
  >
    <v-card
      class="PagesDialog-header"
    >
      <v-card-title class="headline"> {{ dialogObjPages.headerText }} </v-card-title>
      <v-card-text>{{ dialogObjPages.bodyText }}</v-card-text>
    </v-card>
    <v-card class="card-config">
      <div class="loading"
        v-if="loading"
      >
        <v-progress-circular
          class="loading-item"
          :size="200"
          indeterminate
          color="primary"
        ></v-progress-circular>
      </div>
      <v-carousel
        v-if="!loading"
        light
        show-arrows-on-hover
        hide-delimiter-background
        delimiter-icon="mdi-minus"
        height="300"
      >
        <v-carousel-item
          v-for="page in dialogObjPages.pages"
          :key="page.device.id"
        >
          <div class="card-config-carouselContent-header">
            <!-- Devices case -->
            <div
              v-if="pagesAction=='devices'"
            >
              <div 
                v-if="page['job-status']=='FAILED'"
                class="card-config-carouselContent-header-errorMsg"
              > {{page["device-name"]}} (ID: {{page["device-id"]}}) </div>
              <div 
                v-else
                class="card-config-carouselContent-header-successMsg"
              > {{page["device-name"]}} (ID: {{page["device-id"]}}) </div>
            </div>
            <!-- Configlets case -->
            <div
              v-if="pagesAction=='configlets'"
            >
              <div 
                v-if="page['job-status']=='FAILED'"
                class="card-config-carouselContent-header-errorMsg"
              > {{page["cli-configlet-name"]}} (ID: {{page["cli-configlet-id"]}}) </div>
              <div 
                v-else
                class="card-config-carouselContent-header-successMsg"
              > {{page["cli-configlet-name"]}} (ID: {{page["cli-configlet-id"]}}) </div>
            </div>
          </div>
          <div class="card-config-carouselContent-body">
          <v-card-text class="card-config-carouselContent-body-configText">
            <div 
              class="card-config-carouselContent-body-errorMsg"
              v-if="page['job-status']=='FAILED'"
            >
              {{page["job-remarks"]}}
            </div>
            {{page["validated-configuration"]}}
          </v-card-text>
          </div>
        </v-carousel-item>
      </v-carousel>
    </v-card>
    <v-card>
      <div 
        class="pagesDialog-buttons"
        v-if="!loading"
      >
        <v-btn
          text
          @click="$emit('closeDialog')"
        >{{ $t('global.cancel') }}</v-btn> 
        <v-btn
          margin=10px
          color="#003245"
          class="device-button"
          :disabled="dialogObjPages.disableValidation"
          :title="$t('global.applyConfig')"
          @click="$emit('confirmDialog')"
        > {{$t('global.confirm')}} </v-btn>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'PagesDialogComp',
  props:{
    name: String,
    dialogObjPages: Object,
    loading: Boolean,
    disableValidate: Boolean,
    pagesAction: String,
  },
  data(){
    return {
    }
  },
  watch: {
  }
}
</script>

<style lang="scss" scoped>
::v-deep .v-dialog{
  overflow-y: unset;
}
.description{
  padding-left: 1.5rem;
}
.PagesDialog{
  display: flex;
  justify-content: center;
  overflow-y: unset;
  &-header{
    color: #003245;
  }
  &-cardActions {
    width: 100%;
    flex-direction: column;
  }
  &-formDialog {
    width: 100%;
    &-rowContainer{
      display: flex;
      justify-content: space-around;
    }
  }
  &-buttons {
    width: 100%;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
}
.card-config{
  width: 100%;
  display: flex;
  position: relative;
  justify-content: center;
  white-space: pre-wrap;
  &-carouselContent{
    &-header{
      color: white;
      font-size: medium;
      font-weight: bold;
      &-errorMsg{
        background-color: red;
      }
      &-successMsg{
        background-color: green;
      }
    }
    &-body{     
      padding-right: 4rem;
      padding-left: 4rem;
      overflow: scroll;
      height: 100%;
      font-size: small;
      font-family:"Courier New", monospace;
      &-configText{
      line-height: -2pt;
        color: black;
        height: 35rem;
      }
      &-errorMsg{
        color: red;
      }
    }
  }
}
.loading{
  display: flex;
  justify-content: center;
  padding: 2rem;
}
.device-button {
  margin: 10px;
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
.configText {
  overflow: scroll;
  color: black;
  height: 35rem;
}
.errorMessage {
  text-align: center;
  color: rgb(226, 34, 82)
}
</style>
