import Vue from "vue";

import axios from "axios";

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const axiosIns = axios.create({
  baseURL: process.env.VUE_APP_API,
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN",
  headers: {
    "X-CSRFTOKEN": getCookie("csrftoken"),
  },
});

const COOKIE_EXPIRED_MSG = "Token is invalid or expired";

axiosIns.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    let error_message = null;
    if (error.response.data.messages) {
      error_message = error.response.data.messages[0].message;
    }
    switch (error.response.status) {
      case 401:
        if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
          error.config.retry = true;
          // axiosIns.defaults.xsrfCookieName = "csrf_refresh_token";
          await axiosIns.post("/refresh");
          // axiosIns.defaults.xsrfCookieName = "csrf_access_token";
          return axiosIns(error.config);
        } else {
          throw new Error("Error");
        }
        break;
      default:
        break;
    }
    return Promise.reject(error);
  }
);

Vue.prototype.$http = axiosIns;

export default axiosIns;
