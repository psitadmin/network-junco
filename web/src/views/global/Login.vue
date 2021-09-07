<template>
  <div class="registro">
    <div class=imgLogin>
      <img class=imgLogin-img alt="Vue logo" src="@/assets/images/logo-junco.png">
    </div>
    <div class="loginuser">
      <v-form v-model="valid" class="form">
        <div class=formLogin>
          <div class="fieldLogin">
            <div class="loginLabel">
              {{ $t('login.userLabel') }}:
            </div>
            <div class="input">
              <v-text-field
                data-test="login-username"
                v-model="user"
                :label="$t('login.userMessage')" 
                :rules="rules"
                solo
                clearable
                rounded
                filled
                required
              ></v-text-field>
            </div>
          </div>
          <div class="fieldLogin">
            <div class="loginLabel">
              {{ $t('login.passwordLabel') }}:
            </div>
            <div class="input">
              <v-text-field
                v-model="password"
                data-test="login-password"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="rules"
                :type="showPassword ? 'text' : 'password'"
                :label="$t('login.passwordMessage')" 
                solo
                rounded
                filled
                required
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </div>
          </div>
          <v-btn
            data-test="login-button"
            block
            margin=10px
            rounded
            color="#003245"
            class="login-button"
            @click="submit"
          > {{ $t('login.loginMessage') }} </v-btn>
          <div>
            <p v-if="errorAuth" data-test="login-error-auth" class="errorMessage">{{ $t('login.loginError') }}.</p>
          </div>
          <div>
            <p v-if="emptyAuth" data-test="login-error-empty" class="errorMessage">{{ $t('login.loginEmpty') }}.</p>
          </div>
        </div>
      </v-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {loginMocked, mockedUser, mockedPassword} from '@/api/mock_login';

export default {
  data () {
    return{
      valid: true,
      acceptHeader: 'application/vnd.net.juniper.space.user-management.user-ref+xml;version=1',
      showPassword: false,
      errorAuth: false,
      emptyAuth: false,
      user: "",
      password: "",
      rules: [
        v => !!v || this.$t('global.requiredField')
      ],
    }
  },
  methods: {
    /**
     * MOCKED SUBMIT WITH PREDEFINED USER AND PASSWORD TO MAKE API CALLS
     */
    async mockedSubmit() {
      try {
          loginMocked().then( () => {
          sessionStorage.setItem("userSession", mockedUser)
          sessionStorage.setItem("passwordSession", mockedPassword)
          this.$router.push("/")
        })
      } catch (err) {
        if(this.user != "" && this.password != "") {
          this.errorAuth = true;
          this.emptyAuth = false;
        } else {
          this.errorAuth = false;
          this.emptyAuth = true;
        }
        console.error("ERROR", err)
      }
    },
    /**
     * Authentication against ClearPass via Flask python utility
     */
    async submit() {
      const path = process.env.VUE_APP_BACK_URL+'/login'
      console.log("path = ", process.env, path)
      try {
        await axios.post(path, {}, {
          headers: {
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
          },
          auth: {
            username: this.user,
            password: this.password,
          },
          verify: false
        })
        .then( () => {
          sessionStorage.setItem("userSession", this.user)
          sessionStorage.setItem("passwordSession", this.password)
          this.$router.push("/")
          this.emptyAuth = true;
        })
      } catch (err) {
        if(this.user == "" || this.password == "") {
          this.errorAuth = false;
          this.emptyAuth = true;
        } else {
          this.errorAuth = true;
          this.emptyAuth = false;
        }
        console.error("ERROR", err)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.registro {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.loginuser {
  padding: 20px;
  margin: 20px;
  display: flex;
  justify-content: center;
}
.formLogin{
  padding: 20px;
  max-width: 500px;
  width: 35rem;
  margin: 20px;
}
.fieldLogin {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.input{
  width: 20rem;
  float: right
}
.loginLabel {
  font-size: 16pt;
  margin-left: auto;
  margin-right: 0.5rem;
  margin-bottom: 1.7rem;
}
.login-button {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  ::v-deep .v-btn__content {
    color:#fff
  }
}
.imgLogin {
  display: flex;
  justify-content: center;
  &-img{
    max-width: 20rem;
  }
}
.errorMessage {
  text-align: center;
  color: rgb(226, 34, 82)
}
</style>