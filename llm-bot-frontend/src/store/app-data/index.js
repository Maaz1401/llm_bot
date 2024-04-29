import axiosIns from "@/libs/axios";

export default {
  namespaced: true,
  state: {
    isLoggedIn: false,
    user: null,
    navMenuItems: [],
    isInternal: true
  },
  getters: {
    getLoggedInUser: (state) => {
      return state.user;
    },
    hasPermission: (state) => (name) => {
      if (state.user) {
        return state.user.permissions.hasOwnProperty(name);
      }
      return false;
    },
    hasRole: (state) => (name) => {
      if (state.user.role.code_name === name) {
        return true;
      }
      return false;
    },
    isLoggedIn: (state) => state.isLoggedIn,
    getNavMenuItems: (state) => state.navMenuItems,
    isInternal: (state) => state.isInternal,
  },
  mutations: {
    login(state, data) {
      state.isLoggedIn = true;
      state.user = data.user;
    },
    logout(state) {
      state.isLoggedIn = false;
      state.user = null;
    },
    setNavMenuItems(state) {
      state.navMenuItems = [];
      // if (state.user.permissions.hasOwnProperty("dashboard_show")) {
        state.navMenuItems.push({
          title: "Home",
          route: "Home",
          icon: "HomeIcon",
        });
      // }
      if (state.user.permissions.hasOwnProperty("user_show")) {
        state.navMenuItems.push({
          title: "Users",
          icon: "UserIcon",
          route: "User",
        });
      }
      if (state.user.permissions.hasOwnProperty("role_show")) {
        state.navMenuItems.push({
          title: "Roles",
          icon: "UsersIcon",
          route: "Role",
        });
      }
    },
  },
  actions: {
    async login({ commit }, payload) {
      const res = await axiosIns.post("login", payload);
      if (res.status === 200) {
        commit("login", res.data);
        commit("setNavMenuItems");
      }
      return res;
    },
    async logout({ commit }) {
      const res = await axiosIns.post("logout");
      if (res.status === 204) {
        commit("logout");
      }
      return res;
    },
    async getCurrentUser({ commit }) {
      const res = await axiosIns.get("current");
      if (res.status === 200) {
        commit("login", res.data);
        commit("setNavMenuItems");
      }
    },
    async getRoles({ commit }, { pageNumber, name, code_name }) {
      let url = `roles/?page=${pageNumber}`;
      if (name) {
        url += `&name=${name}`;
      }
      if (code_name) {
        url += `&code_name=${code_name}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async getRolesUnpaginated({ commit }, { name, code_name }) {
      let url = `roles-unpaginated/`;
      if (name) {
        url += `&name=${name}`;
      }
      if (code_name) {
        url += `&code_name=${code_name}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async getRole({ commit }, { pk }) {
      const res = await axiosIns.get(`roles/${pk}/`);
      return res;
    },
    async createRole({ commit }, payload) {
      const res = await axiosIns.post("roles/", payload);
      return res;
    },
    async updateRole({ commit }, { payload, pk }) {
      const res = await axiosIns.put(`roles/${pk}/`, payload);
      return res;
    },
    async deleteRole({ commit }, { pk }) {
      const res = await axiosIns.delete(`roles/${pk}/`);
      return res;
    },
    async getPermissions({ commit }) {
      const res = await axiosIns.get("permissions");
      return res;
    },
    async getUser({ commit }, { pk }) {
      const res = await axiosIns.get(`users/${pk}/`);
      return res;
    },
    async getUsers({ commit }, { pageNumber, username, name }) {
      let url = `users/?page=${pageNumber}`;
      if (username) {
        url += `&username=${username}`;
      }
      if (name) {
        url += `&name=${name}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async getUsersUnPaginated({ commit }, { username, name }) {
      let url = `users-unpaginated/`;
      if (username) {
        url += `?username=${username}`;
      }
      if (name) {
        url += `?name=${name}`;
      }
      const res = await axiosIns.get(url);
      return res;
    },
    async createUser({ commit }, { payload }) {
      const res = await axiosIns.post("users-create-update", payload);
      return res;
    },
    async updateUser({ commit }, { payload, pk }) {
      const res = await axiosIns.patch(`users/${pk}/`, payload);
      return res;
    },
    async queryModel({ commit }, payload) {
      const res = await axiosIns.post("query-model", payload, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      return res;
    },
    async getLastConversation({ commit }) {
      const res = await axiosIns.get("last-conversation");
      return res;
    },
  },
};
