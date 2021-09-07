<template>
  <v-alert elevation="24"
    v-model="showAlert"
    text
    :type="type"
  > {{message}} </v-alert>
</template>

<script>
export default {
  data() {
    return {
      };
  },
  props: [
    "showAlert",
    "message",
    "type",
  ],
  watch: {
    showAlert: {
      handler(value) {
        this.showAlert = value
      }
    }
  }
};
</script>