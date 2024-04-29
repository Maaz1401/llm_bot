<template>
  <b-modal id="user-edit-modal" title="User Edit Modal" centered hide-footer size="lg" @hidden="reset"
    :no-close-on-esc="true" :no-close-on-backdrop="true">
    <template #modal-title>
      <h2 class="m-0">Edit User</h2>
    </template>
    <validation-observer ref="userEditFormValidation">
      <b-form @submit.prevent>
        <b-row>
          <b-col>
            <v-select id="roles" inputId="id" label="name" v-model="selectedRole" :options="roles"
              placeholder="Selected Role" class="v-style-chooser" />
          </b-col>
        </b-row>
        <b-form-group class="text-right">
          <b-button type="submit" variant="primary" pill class="mr-1" @click="validationForm">
            Update
          </b-button>
        </b-form-group>
      </b-form>
    </validation-observer>
  </b-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { required, email } from "@validations";
import util from "@/util.js";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  props: {
    user: Object,
  },
  mixins: [util],
  data() {
    return {
      required,
      selectedRole: null,
      roles: []
    };
  },
  async mounted() {
    await this.getUnpaginatedRoles();
    if (this.user) {
      this.selectedRole = this.user.role_data;
    }
  },
  methods: {
    ...mapActions({
      updateUser: "appData/updateUser",
      getRoles: "appData/getRoles",
      getRole: "appData/getRole",
      getRolesUnpaginated: "appData/getRolesUnpaginated",
      createUser: "appData/createUser",
    }),
    async validationForm() {
      const success = await this.$refs.userEditFormValidation.validate();
      if (success) {
        await this.submit();
      }
    },
    async getUnpaginatedRoles() {
      try {
        const res = await this.getRolesUnpaginated({});
        this.roles = res.data;
      } catch (error) {
        console.log(error)
        this.displayError(error);
      }
    },
    async submit() {
      try {
        let res = await this.createUser({
          payload: {
            id: this.user.id,
            username: this.user.username,
            name: this.user.name,
            profile_status: this.user.profile_status,
            telephone: this.user.telephone,
            rank_name: this.user.rank_name,
            service_name: this.user.service_name,
            rank_order: this.user.rank_order,
            rank_id: this.user.rank_id,
            appointment_id: this.user.appointment_id,
            appointment_name: this.user.appointment_name,
            appointment_order: this.user.appointment_order,
            executive_order: this.user.executive_order,
            appointment_type: this.user.appointment_type,
            data_center_id: this.user.data_center_id,
            organization: this.user.organization,
            role: this.selectedRole ? this.selectedRole.id : null,
            created_by: this.getLoggedInUser.id,
            updated_by: this.getLoggedInUser.id,
          },
        });
        if (res.status === 200) {
          this.$swal({
            title: "User updated successfully",
            icon: "success",
          });
          this.$nextTick(() => {
            this.$bvModal.hide("user-edit-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        this.displayError(error);
      }
    },
    reset() {
      this.name = "";
    },
  },
  computed: {
    ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
  },
};
</script>

<style lang="scss">
.vSelectStyle .vs__deselect {
  fill: #fff !important;
}
</style>
