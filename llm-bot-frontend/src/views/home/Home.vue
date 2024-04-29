<template>
  <div style="height: 100vh">
    <Topbar />
    <Main />
    <Footer />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Topbar from "@/components/home/Topbar.vue";
import Main from "@/components/home/Main.vue";
import Footer from "@/components/home/Footer.vue";
import util from "@/util.js";

export default {
  components: {
    Topbar,
    Main,
    Footer,
  },
  mixins: [util],
  data() {
    return {
      data: {},
    };
  },
  async mounted() {},
  methods: {
    ...mapActions({
      getDashboardData: "appData/getDashboardData",
      getDashboardLineChart: "appData/getDashboardLineChart",
    }),
  },
  computed: {
    ...mapGetters({
      hasPermission: "appData/hasPermission",
      getLoggedInUser: "appData/getLoggedInUser",
    }),
  },
};
</script>

<style lang="scss">
@import "@core/scss/vue/libs/vue-flatpicker.scss";
</style>
