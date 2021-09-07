import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/global/Home.vue'
import About from '../views/global/About.vue'
import Login from '../views/global/Login.vue'
import Configlets from '../views/configlets/Configlets.vue'
import ApplyConfiglet from '../views/configlets/ApplyConfiglet.vue'
import JunosDevices from '../views/devices/JunosDevices.vue'
import JunosDevicesConfiglets from '../views/devices/JunosDevicesConfiglets.vue'
import AllDevices from '../views/devices/AllDevices.vue'
import Task from '../views/task/Task.vue'
import ARPTables from '../views/arptables/ARPTables.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/configlets',
    name: 'Configlets',
    component: Configlets,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/configlets/:id',
    name: 'ApplyConfiglets',
    component: ApplyConfiglet,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/junosdevices',
    name: 'JunosDevices',
    component: JunosDevices,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/junosdevices/:id',
    name: 'JunosDevicesConfiglets',
    component: JunosDevicesConfiglets,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/alldevices',
    name: 'AllDevices',
    component: AllDevices,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/alldevices/task/:id',
    name: 'Task',
    component: Task,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/arpTables',
    name: 'ARP Tables',
    component: ARPTables,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path :'*',
    redirect: '/',
    component: Home
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

router.beforeEach( (to, from, next) => {
  const requiresAuth = to.matched.some(x => x.meta.requiresAuth);
  const currentUser = sessionStorage.userSession;

  if (requiresAuth && !currentUser) {
    if (from.path !== '/login') {
      next('/login');
    }
  } else {
    next();
  }

});

export default router