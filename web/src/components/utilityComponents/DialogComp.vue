<template>
  <v-dialog
    class="dialogComponent"
    v-model="dialogObj.showComponent"
    persistent
    max-width="800"
  >
    <v-card>
      <v-card-title class="headline"> {{ dialogObj.headerText }} </v-card-title>
      <v-card-text>{{ dialogObj.bodyText }}</v-card-text>
      <div class="dialogContent">
        <v-card-actions class="dialogContent-cardActions">
          <v-spacer></v-spacer>
          <!-- CONFIRM data-table  -->
          <v-data-table 
            class=dialogContent-table
            v-if="dialogObj.action==='confirm'"
            width=100%
            :headers="dialogObj.headers"
            :items="dialogObj.items"
            item-key="id"
            hide-default-footer
            fixed-header
            dense
          ></v-data-table>
          <!-- DELETE data-table  -->
          <v-data-table 
            class=dialogContent-table
            v-else-if="dialogObj.action==='delete'"
            width=100%
            :headers="dialogObj.headers"
            :items="dialogObj.items"
            item-key="id"
            hide-default-footer
            fixed-header
            dense
          ></v-data-table>

          <!-- ADD / EDIT form  -->
          <div class="dialogContent-formDialog" v-else-if="dialogObj.action==='add' || dialogObj.action==='edit'">
            <v-form
              ref="form"
              v-model="valid"
            >
              <!-- Dialog Header -->
              <div class="dialogContent-formDialog-header">
                <div class="dialogContent-formDialog-rowContainer">
                  <div class="dialogLabelHeader">
                  {{ dialogObj.headers[0].text }}
                  </div> 
                  <div class="dialogInputHeader">
                  {{ dialogObj.headers[1].text }}
                  </div> 
                </div>
              </div>

              <!-- Dialog Body -->
              <div class="inputDialog-body">
                
                <div class="dialogContent-formDialog-rowContainer">
                  <div class="dialogLabel">
                    {{ dialogObj.params[0].parameter }}
                  </div>
                  <div class="dialogInput">
                    <v-text-field
                        v-model="deviceIP"
                        :rules="[rules.required, rules.ip]"
                        maxlength="15"
                        required
                        :hint="dialogObj.params[0].parameter"
                        :label="dialogObj.params[0].placeholder"
                    ></v-text-field>
                  </div>
                </div>

                <div class="dialogContent-formDialog-rowContainer">
                  <div class="dialogLabel">
                    {{ dialogObj.params[1].parameter }}
                  </div>
                  <div class="dialogInput">
                    <v-text-field
                        v-model="deviceName"
                        :rules="[rules.required, rules.devicename]"
                        counter="25"
                        maxlength="25"
                        required
                        :hint="dialogObj.params[1].parameter"
                        :label="dialogObj.params[1].placeholder"
                    ></v-text-field>
                  </div>
                </div>

                <div class="dialogContent-formDialog-rowContainer">
                  <div class="dialogLabel">
                    {{ dialogObj.params[2].parameter }}
                  </div>
                  <div class="dialogInput">
                    <v-select
                      v-model="vendor"
                      dense
                      :rules="rules.selectRequired"
                      required
                      :items="dialogObj.params[2].selectOptions"
                      :label="dialogObj.params[2].placeholder"
                    ></v-select>
                  </div>
                </div>

                <div class="dialogContent-formDialog-rowContainer">
                  <div class="dialogLabel">
                    {{ dialogObj.params[3].parameter }}
                  </div>
                  <div class="dialogInput">
                    <v-select
                      v-model="protocol"
                      dense
                      :rules="rules.selectRequired"
                      required
                      :items="dialogObj.params[3].selectOptions"
                      :label="dialogObj.params[3].placeholder"
                    ></v-select>
                  </div>
                </div>

                <div class="dialogContent-formDialog-rowContainer">
                  <div class="dialogLabel">
                    {{ dialogObj.params[4].parameter }}
                  </div>
                  <div class="dialogInput">
                    <v-select
                      v-model="deviceType"
                      dense
                      :rules="rules.selectRequired"
                      required
                      :items="dialogObj.params[4].selectOptions"
                      :label="dialogObj.params[4].placeholder"
                    ></v-select>
                  </div>
                </div>
                <p v-if="errorForm" class="errorMessage">{{ $t('errors.invalidForm') }}.</p>
              </div>
            </v-form>
          </div>
          <!-- BUTTONS -->
          <div class="dialogContent-buttons">
            <v-btn
              text
              @click="resetForm(), $emit('closeDialog'), errorForm=false"
            >{{ $t('global.cancel') }}</v-btn>
            <v-btn 
              v-for="(item, index) in dialogObj.buttons"
                :key="'customButton'+index"
                :class="item.class"
                :color="item.color"
                @click="dialogCompActionController(item.action)"
            > {{ item.text }} </v-btn>
          </div>
          
        </v-card-actions>
      </div>
    </v-card>
  </v-dialog> 
</template>

<script>
import {ipRegex} from '@/utils/constants.js'

export default {
  name: 'DialogComp',
  props: {
    dialogObj: Object
  },
  data(){
    return {
      valid: true,
      deviceName: '',
      deviceIP: '',
      vendor: "",
      protocol: "",
      deviceType: "",
      rules: {
        devicename: value => (value && value.length <= 25) || this.$t("devices.deviceComp.cards.nameRule"),
        required: value => !!value || this.$t("global.requiredField"),
        selectRequired: [ (value => !!value) || this.$t("global.requiredField")],
        ip: value => {
          const pattern = ipRegex
          return pattern.test(value) || this.$t("global.invalidIP")
        },
      },
      errorForm: false,
    }
  },
  methods: {
    // ACTION METHOD CONTROLLER: watch event emitted by button and emits to parent
    dialogCompActionController(action){
      if(action === "add"){
        let device = {
          'name': this.deviceName,
          'ip': this.deviceIP, 
          'vendor': this.vendor, 
          'protocol': this.protocol, 
          'device_type': this.deviceType
        }
        // Call validate method to emit action
        if(this.$refs.form.validate()){
          this.$emit('acceptDialog', action, device)
          this.resetForm()
        }else{
          this.errorForm = true
        }
      }else if(action === "edit"){
        let device = {  
          'id': this.dialogObj.editableDevice.id,
          'name': this.deviceName,
          'ip': this.deviceIP, 
          'vendor': this.vendor, 
          'protocol': this.protocol, 
          'device_type': this.deviceType
        }
        // Call validate method to emit action
        if(this.$refs.form.validate()){
          this.$emit('acceptDialog', action, device)
          this.resetForm()
        }else{
          this.errorForm = true
        }
      }else if(action === "delete"){
        this.$emit('acceptDialog', action)
      }else if(action === "confirm"){
        this.$emit('acceptDialog', action)
      }else if(action === "clear"){
        this.resetForm()
      }else{
        console.log("Unknow action")
      }
    },
    // Check form validation
    validate () {
      this.$refs.form.validate();
      if (this.valid){
        return true
      } else {
        return false
      }
    },
    resetForm () {
      if (this.dialogObj.action !== 'delete' && this.dialogObj.action !==  'confirm'){
        this.$refs.form.reset() 
      }
      this.errorForm = false
    },

    mounted(){
      this.errorForm = false;
    }
  },
  watch: {
    'dialogObj.showComponent': {
      handler(value) {
        if(value && this.dialogObj.action === 'edit'){
          this.deviceName = this.dialogObj.editableDevice.name
          this.deviceIP = this.dialogObj.editableDevice.ip  
          this.vendor = this.dialogObj.editableDevice.vendor
          this.protocol = this.dialogObj.editableDevice.protocol
          this.deviceType = this.dialogObj.editableDevice.device_type
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.dialogContent{
  display:flex;
  justify-content: center;
  &-cardActions {
    width: 100%;
    flex-direction: column;
  }
  &-formDialog {
    width: 100%;

    &-rowContainer{
      display: flex;
      align-items: baseline;
      margin-bottom: 2rem;
      &:first-child{
        margin-bottom: 0rem;
      }
    }
  }
  .dialogLabel{
    width: 30%;
    text-align: right;
    margin-right: 2rem;
  }
  .dialogInput{
    width: 40%;
    // text-align: left;
    margin-left: 2rem;
  }
  .dialogLabelHeader{
    width: 30%;
    height: fit-content;
    text-align: right;
    margin-right: 2rem;
    font-size: large;
    color: #003245;
    font-weight: bold;
  }
  .dialogInputHeader{
    width: 40%;
    height: fit-content;
    margin-left: 2rem;
    font-size: large;
    color: #003245;
    font-weight: bold;
  }
  &-buttons {
    width: 100%;
    margin-top: 1rem;
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