import Vue from "vue";
import Toast from "vue-toastification";

import "@core/scss/vue/libs/toastification.scss";

Vue.use(Toast, {
  hideProgressBar: true,
  closeOnClick: false,
  closeButton: false,
  icon: false,
  timeout: 3000,
  transition: "Vue-Toastification__fade",
});
