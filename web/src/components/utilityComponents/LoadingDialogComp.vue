<template>
  <v-dialog
    class="loadingDialogComp"
    v-model="loadingDialogObj.showComponent"
    persistent
    max-width="800"
  >
    <v-card class="loadingDialogComp-headerCard">
      <v-card-title class="headline">
        {{ loadingDialogObj.headerText }}
      </v-card-title>
      <v-card-text>{{ loadingDialogObj.bodyText }}</v-card-text>
    </v-card>
    <v-card class="loadingDialogComp-bodyCard">
      <div class="loadingDialogComp-bodyCard-loading" v-if="loading">
        <v-progress-circular
          class="oadingDialogComp-bodyCard-loading-item"
          :size="50"
          indeterminate
          color="primary"
        ></v-progress-circular>
      </div>
      <div class="loadingDialogComp-bodyCard-alert" v-if="!loading && loadingDialogObj.status">
        <div class="loadingDialogComp-bodyCard-alert-error" v-if="loadingDialogObj.status == 'FAILED'">
          {{loadingDialogObj.alertMessage}}
        </div>
        <div class="loadingDialogComp-bodyCard-alert-success" v-else>
          {{loadingDialogObj.alertMessage}}
        </div>
      </div>
      <div class="loadingDialogComp-bodyCard-content">
        {{ loadingDialogObj.content }}
      </div>
    </v-card>
    <v-card>
      <div class="loadingDialogComp-buttons" v-if="!loading">
        <v-btn
          v-for="(item, index) in loadingDialogObj.buttons"
          :key="'customButton' + index"
          :class="item.class"
          :color="item.color"
          @click="dialogCompActionController(item.action)"
        >
          {{ item.text }}
        </v-btn>
        <v-btn
          margin="10px"
          color="#003245"
          class="device-button"
          @click="$emit('closeDialog')"
          >{{ $t("global.confirm") }}</v-btn
        >
        </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "LoadingDialogComp",
  props: {
    loadingDialogObj: Object,
    loading: Boolean,
    showComponent: Boolean,
  },
  data() {
    return {};
  },
  watch: {},
};
</script>

<style lang="scss" scoped>
::v-deep .v-dialog{
  overflow-y: unset;
}
.description{
  padding-left: 1.5rem;
}
.loadingDialogComp{
  display: flex;
  justify-content: center;
  overflow-y: unset;
  &-header{
    color: #003245;
  }
  &-bodyCard {
    &-loading {
      display: flex;
      justify-content: center;
      padding: 2rem;
    }
    &-alert{
      color: white;
      font-size: medium;
      font-weight: bold;
      &-error{
        background-color: red;
      }
      &-success{
        background-color: green;
      }
    }
    &-content {
      width: 100%;
      display: flex;
      position: relative;
      justify-content: center;
      white-space: pre-wrap;
      overflow: scroll;
      padding-right: 4rem;
      padding-left: 4rem;
      height: 100%;
      font-size: medium;
      font-family:"Courier New", monospace;
    }
  }
  &-buttons {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
}

.device-button {
  margin: 10px;
  margin-left: 1rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
.errorMessage {
  text-align: center;
  color: rgb(226, 34, 82)
}
</style>
