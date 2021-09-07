import Vue from 'vue';
import VueI18n from 'vue-i18n';
import es from './messages/es.js';
import en from './messages/en.js';


Vue.use(VueI18n);

const messages = {
    es,
    en
}


export const i18n = new VueI18n({
    locale: 'es',
    messages // se puede poner messages = messages
});