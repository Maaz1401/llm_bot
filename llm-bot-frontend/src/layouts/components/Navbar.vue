<template>
  <div class="navbar-container d-flex content align-items-center">
    <ul class="nav navbar-nav d-xl-none">
      <li class="nav-item">
        <b-link class="nav-link" @click="toggleVerticalMenuActive">
          <feather-icon icon="MenuIcon" size="21" />
        </b-link>
      </li>
    </ul>

    <div class="bookmark-wrapper align-items-center flex-grow-1 d-none d-lg-flex">
      <dark-Toggler class="d-none d-lg-block" />
    </div>

    <b-navbar-nav class="nav align-items-center ml-auto">
      <b-nav-item-dropdown right toggle-class="d-flex align-items-center dropdown-user-link" class="dropdown-user">
        <template #button-content>
          <div class="d-sm-flex d-none user-nav">
            <p class="user-name font-weight-bolder mb-0">
              {{ getLoggedInUser ? getLoggedInUser.name : "" }}
            </p>
          </div>
          <b-avatar size="40" variant="light-primary" badge :src="getLoggedInUser ? getLoggedInUser.profile_image : ''"
            class="badge-minimal" badge-variant="success" />
        </template>
        <!-- 
        <b-dropdown-item-button :to="{ name: 'Profile' }" button-class="w-100">
          <feather-icon size="16" icon="UserIcon" class="mr-50" />
          <span>Profile</span>
        </b-dropdown-item-button>

        <b-dropdown-divider /> -->

        <b-dropdown-item-button button-class="w-100" @click="logoutButtonClick">
          <feather-icon size="16" icon="LogOutIcon" class="mr-50" />
          <span>Logout</span>
        </b-dropdown-item-button>
      </b-nav-item-dropdown>
    </b-navbar-nav>
  </div>
</template>

<script>
import DarkToggler from "@core/layouts/components/app-navbar/components/DarkToggler.vue";
import { mapGetters, mapActions } from "vuex";

export default {
  components: {
    DarkToggler,
  },
  props: {
    toggleVerticalMenuActive: {
      type: Function,
      default: () => { },
    },
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
