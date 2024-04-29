<template>
  <div class="auth-wrapper auth-v2">
    <b-row class="auth-inner m-0">
      <b-link
        class="brand-logo d-flex justify-content-center align-items-center"
      >
        <img :src="this.appLogoImage" width="50" height="50" />
      </b-link>

      <b-col lg="3" class="d-none d-lg-flex align-items-center p-5">
        <!-- <div class="overlay"></div> -->
        <div
          class="w-100 d-lg-flex align-items-center justify-content-center"
        ></div>
      </b-col>

      <b-col lg="6" class="d-flex align-items-center auth-bg px-2 p-lg-5">
        <b-col sm="8" md="6" lg="12" class="px-xl-2 mx-auto">
          <b-card-text class="mb-2">
            Please sign-in to your account
          </b-card-text>

          <validation-observer ref="loginFormValidation">
            <b-form class="auth-login-form mt-2" @submit.prevent>
              <b-form-group label="Username" label-for="username">
                <validation-provider
                  #default="{ errors }"
                  name="Username"
                  rules="required"
                >
                  <b-form-input
                    id="username"
                    v-model="username"
                    :state="errors.length > 0 ? false : null"
                    name="username"
                    placeholder="Username"
                  />
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>

              <b-form-group label="Password" label-for="password">
                <validation-provider
                  #default="{ errors }"
                  name="Password"
                  rules="required"
                >
                  <b-input-group
                    class="input-group-merge"
                    :class="errors.length > 0 ? 'is-invalid' : null"
                  >
                    <b-form-input
                      id="password"
                      v-model="password"
                      :state="errors.length > 0 ? false : null"
                      class="form-control-merge"
                      :type="passwordFieldType"
                      name="password"
                      placeholder="············"
                    />
                    <b-input-group-append is-text>
                      <feather-icon
                        class="cursor-pointer"
                        :icon="passwordToggleIcon"
                        @click="togglePasswordVisibility"
                      />
                    </b-input-group-append>
                  </b-input-group>
                  <small class="text-danger">{{ errors[0] }}</small>
                </validation-provider>
              </b-form-group>

              <b-button
                type="submit"
                variant="primary"
                block
                @click="validateForm"
              >
                Sign in
              </b-button>
            </b-form>
          </validation-observer>
        </b-col>
      </b-col>
      
      <b-col lg="3" class="d-none d-lg-flex align-items-center p-5">
        <!-- <div class="overlay"></div> -->
        <div
          class="w-100 d-lg-flex align-items-center justify-content-center"
        ></div>
      </b-col>

    </b-row>
  </div>
</template>

<script>
// import Navbar from "@/components/dashboard/Navbar.vue";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { required } from "@validations";
import { togglePasswordVisibility } from "@core/mixins/ui/forms";
import { $themeConfig } from "@themeConfig";
import { mapActions } from "vuex";
import util from "@/util.js";
import store from "@/store";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    // Navbar,
  },
  mixins: [togglePasswordVisibility, util],
  data() {
    return {
      appName: "",
      appFullName: "",
      appFullName: "",
      appMissionStatement: "",
      password: "",
      username: "",
      required,
      internal: false,
    };
  },
  created() {
    this.internal = store.getters["appData/isInternal"];
    this.appName = $themeConfig.app.appName;
    this.appFullName = $themeConfig.app.appFullName;
    this.appLogoImage = $themeConfig.app.appLogoImage;
    this.appMissionStatement = $themeConfig.app.appMissionStatement;
  },
  methods: {
    ...mapActions({ login: "appData/login" }),
    async validateForm() {
      const success = await this.$refs.loginFormValidation.validate();
      if (success) {
        await this.submit();
      }
    },
    async submit() {
      try {
        const res = await this.login({
          username: this.username,
          password: this.password,
        });
        if (res.status === 200) {
          this.$swal({
            title: "Logged in successfully",
            icon: "success",
          });
          if (store.getters["appData/hasPermission"]("dashboard_show")) {
            this.$router.push({ name: "Dashboard" });
          } else {
            if (
              store.getters["appData/hasPermission"]("application_show")
            ) {
              if (store.getters["appData/hasPermission"]("eng_application_show"))
              {
                this.$router.push({ name: "Engineering Application" });
              }
              else if (store.getters["appData/hasPermission"]("med_application_show"))
              {
                this.$router.push({ name: "Medical Application" });
              }
              else if (store.getters["appData/hasPermission"]("misc_application_show"))
              {
                this.$router.push({ name: "Miscellaneous Application" });
              }
              else if (store.getters["appData/hasPermission"]("dip_application_show"))
              {
                this.$router.push({ name: "Diploma Application" });
              }
            }
            else if (
              store.getters["appData/hasPermission"]("stu_eng_application_show")
            ) {
              this.$router.push({ name: "Student Engineering Applications" });
            } else if (
              store.getters["appData/hasPermission"]("stu_med_application_show")
            ) {
              this.$router.push({ name: "Student Medical Applications" });
            } else if (
              store.getters["appData/hasPermission"](
                "stu_misc_application_show"
              )
            ) {
              this.$router.push({ name: "Student Miscellaneous Applications" });
            } else if (
              store.getters["appData/hasPermission"]("stu_dip_application_show")
            ) {
              this.$router.push({ name: "Student Diploma Applications" });
            } else if (
              store.getters["appData/hasPermission"](
                "coro_eng_application_show"
              )
            ) {
              this.$router.push({ name: "Coro Engineering Applications" });
            } else if (
              store.getters["appData/hasPermission"](
                "verify_serving_eng_application_show"
              )
            ) {
              this.$router.push({
                name: "Verify Serving Engineering Applications",
              });
            } else if (
              store.getters["appData/hasPermission"](
                "data_eng_application_show"
              )
            ) {
              this.$router.push({
                name: "Data Carrier Engineering Applications",
              });
            } else if (
              store.getters["appData/hasPermission"](
                "data_med_application_show"
              )
            ) {
              this.$router.push({
                name: "Data Carrier Medical Applications",
              });
            } else if (
              store.getters["appData/hasPermission"](
                "data_misc_application_show"
              )
            ) {
              this.$router.push({
                name: "Data Carrier Miscellaneous Applications",
              });
            } else if (
              store.getters["appData/hasPermission"](
                "data_dip_application_show"
              )
            ) {
              this.$router.push({
                name: "Data Carrier Diploma Applications",
              });
            }
          }
        }
      } catch (error) {
        this.displayError(error);
      }
    },
  },
  computed: {
    passwordToggleIcon() {
      return this.passwordFieldType === "password" ? "EyeIcon" : "EyeOffIcon";
    },
  },
};
</script>

<style lang="scss">
@import "@core/scss/vue/pages/page-auth.scss";
</style>

<style scoped>
.overlay {
  /* background: rgba(9, 65, 32, 0.7) url("~@/assets/images/slider/01.jpg"); */
  background: rgba(213, 243, 254, 1) url("~@/assets/images/slider/01.jpg");
  background-size: cover;
  position: absolute;
  background-blend-mode: multiply;
  height: 100%;
  width: 100%;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  -webkit-transition: all 0.4s ease-in-out 0s;
  -moz-transition: all 0.4s ease-in-out 0s;
  transition: all 0.4s ease-in-out 0s;
}
</style>
