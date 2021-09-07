<template>
  <div class="header">
    <div class="header-logo">
      <img
        data-test="home-route"
        class="logo"
        alt="Vue logo"
        src="@/assets/images/logo-junco-dark.png"
        @click="goHome()"
      />
    </div>
    
    <div class="header-routes">
      <div class="header-routes__element" 
        data-test="about-route"
        @click="goAbout()">
        {{ $t("headers.about") }}
      </div>
      <div class="header-routes__element"
        @click="logOut">
        <span>
          {{ $t("headers.logout") }}
        </span>
      </div>
      <!-- <div class="header-routes__element"
        @click="$router.push('/login').catch(() => {})">
        <span>
          {{ $t("login.loginMessage") }}
        </span>
      </div> -->
      <div class="header-routes__element"
        :title="$t('headers.languageSelector')"
      >
        <v-select class="select-language"
          v-model="languageSelector"
          :items="items"
        >
          <template slot="selection" slot-scope="data">
            <img :src="data.item.image" />
          </template>
          <template slot="item" slot-scope="data">
            <img :src="data.item.image" />
          </template>
        </v-select>
      </div>
    </div>
  </div>
</template>

<script>
import spain from "@/assets/images/spain-flag-button-round-icon-16.png";
import uk from "@/assets/images/united-kingdom-flag-button-round-icon-16.png";
export default {
  name: "MainHeader",
  data() {
    return {
      logedUser: false,
      languageSelector: this.$i18n.locale,
      items: [
        { image: spain, value: 'es'},
        { image: uk, value: 'en'},
      ]
    };
  },
  methods: {
    goHome () {
      if (this.$route.path !== "/") this.$router.push("/")
    },
    goAbout () {
      if (this.$route.path !== "/about") this.$router.push("/about")
    },
    logOut () {
      sessionStorage.removeItem("userSession")
      sessionStorage.removeItem("passwordSession")
      this.$router.push("/login").catch(e => {console.log(e)});
    }
  },
  watch: {
    languageSelector (value) {
      this.$i18n.locale = value;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.header {
  width: 100%; /* hacemos que la cabecera ocupe el ancho completo de la página */
	left: 0; /* Posicionamos la cabecera al lado izquierdo */
	top: 0; /* Posicionamos la cabecera pegada arriba */
	position: fixed; /* Hacemos que la cabecera tenga una posición fija */
  z-index: 100;
  height: 3rem;
  background-color: #003245;
  background-size: cover;
  display: flex;
  margin-bottom: 2rem;
  justify-content: space-between;
  align-items: center;
  text-align: center;
  color: white;

  &-routes{
    display: flex;
    height: 100%;
    &__element {
      .v-input {
        ::v-deep &__slot::after {
          display: none;
        }
        padding: 0%;
      }
      height: 100%;
      padding: 0 0.5rem;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      border-left: 0.5px solid  #2c3e50;
      &:hover{
        background:white;
        color: #2c3e50;
      }
      letter-spacing: 0.1rem;
      cursor: pointer;
      .select-language{
        padding-top: 0.3rem;
        display: flex;
        height: 100%;
        width: 3rem;  
      }
    }

  }

}
.header-logo {
  display: flex;
  max-width: 100%;
  max-height: 100%;
  cursor: pointer;
}
.logo {
  max-width: 3rem;
}
</style>
