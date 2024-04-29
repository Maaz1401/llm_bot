<template>
  <div style="height: 87%" class="py-50 px-50">
    <!-- ADD ANY POPUP COMPONENTS HERE TO SHOW USING ON-CLICK OR V-IF -->
  <!-- <b-row > -->
    <ChatBox/>
  <!-- </b-row> -->
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { $themeColors } from "@themeConfig";
import moment from "moment";
import util from "@/util.js";
import "swiper/css/swiper.css";
import ChatBox from "@/components/chat/ChatBox.vue";

export default {
  components: {
    ChatBox
  },
  mixins: [util],
  data() {
    return {
      data: {},
    };
  },
  created() { },
  async mounted() {
  },
  methods: {
    ...mapActions({
      getDashboardData: "appData/getDashboardData",
    }),
    async dashboardData() {
      try {
      } catch (error) {
        this.displayError(error);
      }
    },
  },
  computed: {
    ...mapGetters({
      hasPermission: "appData/hasPermission",
      getLoggedInUser: "appData/getLoggedInUser",
    }),
  },
  watch: {
  }
};
</script>

<style lang="scss">
</style>
