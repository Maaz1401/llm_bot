import Vue from "vue";
import Vuex from "vuex";

import app from "./app";
import appConfig from "./app-config";
import verticalMenu from "./vertical-menu";
import appData from "./app-data";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    app,
    appConfig,
    verticalMenu,
    appData,
  },
  strict: process.env.DEV,
});
