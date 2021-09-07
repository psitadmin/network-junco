<template>
<div class="taskcontainer">
  <h3>{{device.name}} ({{deviceId}}) - {{device.ip}}</h3>
  <h4>{{ $t('tasks.selectTask')}}</h4>
  <v-sheet class="taskSheet"> 
    <v-data-table
      :headers="headers"
      :items="task"
      item-key="id"
      :search="searchText"
      fixed-header
    >
      <template 
        v-slot:[`item.actions`]="{ item }"
        class="taskTable-icons"
      >
        <v-icon
          color="green darken-2"
          @click="taskRun(item.id)"
        > mdi-play </v-icon>
        <v-icon
          color="primary"
          @click="taskInfo(item.id)"
        > mdi-information </v-icon>
      </template>
    </v-data-table>
  </v-sheet>
  <InterfacesComp
  :device="device"
  :showComponent="interfacesComp.showComponent"
  @closeDialog="closeDialogController"
  ></InterfacesComp>


  <!-- Displays alert message whenever backend actions occurs -->
  <AlertComponent
    :showAlert="showAlert"
    :message="alertMessage"
    :type="alertType"
  ></AlertComponent>
</div>
</template>

<script>
import {getDeviceByIDAPI} from '@/api/devices.js';
import InterfacesComp from '@/components/tasks/InterfacesComp.vue';
import AlertComponent from '@/components/utilityComponents/alertComponent.vue'

export default {
  name: 'Task',
  components: {
    InterfacesComp,
    AlertComponent
  },
  data(){
    return{
      deviceId: this.$route.params.id,
      device: {},
      dialog: true,
      searchText: '',
      headers: [
        {text: "id", value: "id"},
        {text: "task", value: "task"},
        {text: "description", value: "description"},
        { text: '', value: 'actions', sortable: false },
      ],
      task: [
        {id: '1', task: "Interfaces", description: "Permite ver las interfaces del equipo y activarlas/desactivarlas"},
        {id: '2', task: "Tarea 2", description: "Descripción de la tarea 2"},
        {id: '3', task: "Tarea 3", description: "Descripción de la tarea 3"},
        {id: '.', task: "...", description: "..."},
        {id: 'n', task: "Tarea N", description: "Descripción de la tarea N"},
      ],
      // Task components
      interfacesComp: {
        showComponent: false,
      },

      // Alert component
      alertMessage: '',
      alertType: 'info',
      showAlert: false,
    }
  },
  computed: {
  },
  methods: {
    taskRun(id){
      console.log("taskRun",id)
      this.interfacesComp.device=this.device
      this.interfacesComp.showComponent = true

    },
    taskInfo(id){
      console.log("taskInfo",id)
    },

    // COMPONENTS CONTROLLERS
    closeDialogController(component){
      switch(component){
        case'InterfacesComp':
          this.interfacesComp.showComponent = false
          this.interfacesComp.device = {}
          break;
      }
    },
    confirmDialogController(component){
      switch(component){
        case'InterfacesComp':
          this.closeDialogController(component)
          break;
      }
    },
    /**
     * Configure the alert component showed
     * @param time seconds to display alert component
     * @param type the type of alert component
     * @param message string displayed by alert component
     */
    displayAlertTime(time, type, message){
      this.alertType = type
      this.showAlert = true
      this.alertMessage = message
      let seconds = time*1000
      setTimeout( () => {
        this.showAlert = false
      }, seconds)
    }
  },
  mounted(){
    this.interfacesComp.showComponent = false
    getDeviceByIDAPI([this.deviceId]).then( res => {
      this.device = res.data.data
    }).catch( () => {
      this.displayAlertTime(5, "error", this.$t('errors.databaseError'))
    })
  }
}
</script>

<style lang="scss" scoped>
.taskcontainer {
  width: 80%;
}
</style>