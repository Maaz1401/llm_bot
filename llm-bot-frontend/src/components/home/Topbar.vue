<template>
  <div style="height: 8%">
    <div class="
          d-flex
          justify-content-center
          align-items-center
          h-100
          px-2
        ">
      <div class="d-flex justify-content-center align-items-center mx-auto">
        <h4 class="m-0 ml-1 brand-text text-primary font-weight-bolder">
          <h3>
            <!-- <strong>Chat with Llama 3</strong> -->
            <strong>Chat with GPT 3.5</strong>
          </h3>
        </h4>
      </div>

      <b-navbar-nav class="nav align-items-center">
        <b-nav-item-dropdown right toggle-class="d-flex align-items-center dropdown-user-link" class="dropdown-user">
          <template #button-content>
            <div class="d-sm-flex d-none user-nav">
              <p class="user-name font-weight-bolder mb-0">
                {{ getLoggedInUser ? getLoggedInUser.name : "" }}
              </p>
            </div>
            <b-avatar size="40" variant="light-primary" badge :src="getLoggedInUser ? getLoggedInUser.profile_image : ''"
              class="badge-minimal ml-50" badge-variant="success" />
          </template>
          <b-dropdown-item-button @click="logoutButtonClick" button-class="w-100">
            <feather-icon size="16" icon="LogOutIcon" class="mr-50" />
            <span>Logout</span>
          </b-dropdown-item-button>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { $themeConfig } from "@themeConfig";
export default {
  data() {
    return {
      appName: "",
      appFullName: "",
      appLogoImage: "",
    };
  },
  created() {
    this.appName = $themeConfig.app.appName;
    this.appFullName = $themeConfig.app.appFullName;
    this.appLogoImage = $themeConfig.app.appLogoImage;
  },
  methods: {
    ...mapActions({ logout: "appData/logout" }),
    async logoutButtonClick() {
      try {
        const res = await this.logout();
        if (res.status === 204) {
          this.$router.push({ name: "Login" });
        }
      } catch (error) {
        console.log(error);
      }
    },
  },
  computed: {
    ...mapGetters({
      hasRole: "appData/hasRole",
      getLoggedInUser: "appData/getLoggedInUser",
    }),
  },
};
</script>

<style></style>
