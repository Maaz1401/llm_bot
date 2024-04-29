<template>
  <b-modal
    id="role-create-modal"
    title="Role Create Modal"
    centered
    hide-footer
    size="lg"
    @hidden="resetModal"
    :no-close-on-esc="true"
    :no-close-on-backdrop="true"
  >
    <template #modal-title> <h2 class="m-0">Create Role</h2> </template>
    <validation-observer ref="roleCreateFormValidation">
      <b-form @submit.prevent>
        <b-row>
          <b-col md="6">
            <b-form-group label="Name" label-for="name">
              <template #label>
                Name <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Name"
                rules="required|alpha"
              >
                <b-form-input
                  id="name"
                  v-model="name"
                  :state="errors.length > 0 ? false : null"
                  placeholder="Name"
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
          <b-col md="6">
            <b-form-group label="Code Name" label-for="codeName">
              <template #label>
                Code Name <span class="text-danger">*</span>
              </template>
              <validation-provider
                #default="{ errors }"
                name="Code Name"
                rules="required|alpha"
              >
                <b-form-input
                  id="codeName"
                  v-model="codeName"
                  :state="errors.length > 0 ? false : null"
                  placeholder="Code Name"
                />
                <small class="text-danger">{{ errors[0] }}</small>
              </validation-provider>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="6">
            <h6 class="text-primary font-weight-bold mb-2 text-center">
              Available Permissions
            </h6>
            <b-form-group>
              <b-form-input
                v-model="availablePermissionSearch"
                placeholder="Search"
                :disabled="availablePermissionList.length === 0"
              />
            </b-form-group>
            <vue-perfect-scrollbar
              :settings="perfectScrollbarSettings"
              class="scroll-area-size border border-primary"
            >
              <draggable
                :list="availablePermissionList"
                tag="ul"
                group="permissions"
                class="list-group list-group-flush cursor-move"
              >
                <b-list-group-item
                  v-for="(listItem, index) in filterAvailablePermissionByName"
                  :key="index"
                  tag="li"
                >
                  <div class="d-flex">
                    <div class="ml-25">
                      <b-card-text class="mb-0 font-weight-bold">
                        {{ listItem.name }}
                      </b-card-text>
                      <b-card-text class="mb-0">
                        {{ listItem.module_name }}
                      </b-card-text>
                      <small>{{ listItem.description }}</small>
                    </div>
                  </div>
                </b-list-group-item>
              </draggable>
            </vue-perfect-scrollbar>
          </b-col>
          <b-col md="6">
            <h6 class="text-primary font-weight-bold mb-2 text-center">
              Allowed Permissions
            </h6>
            <b-form-group>
              <b-form-input
                v-model="allowedPermissionSearch"
                placeholder="Search"
                :disabled="allowedPermissionList.length === 0"
              />
            </b-form-group>
            <vue-perfect-scrollbar
              :settings="perfectScrollbarSettings"
              class="scroll-area-size border border-primary"
            >
              <draggable
                :list="allowedPermissionList"
                tag="ul"
                group="permissions"
                class="list-group list-group-flush cursor-move"
              >
                <b-list-group-item
                  v-for="(listItem, index) in filterAllowedPermissionByName"
                  :key="index"
                  tag="li"
                >
                  <div class="d-flex">
                    <div class="ml-25">
                      <b-card-text class="mb-0 font-weight-bold">
                        {{ listItem.name }}
                      </b-card-text>
                      <b-card-text class="mb-0">
                        {{ listItem.module_name }}
                      </b-card-text>
                      <small>{{ listItem.description }}</small>
                    </div>
                  </div>
                </b-list-group-item>
              </draggable>
            </vue-perfect-scrollbar>
          </b-col>
        </b-row>
        <b-form-group class="text-right">
          <b-button
            type="submit"
            variant="primary"
            pill
            class="mr-1"
            @click="validationForm"
          >
            Submit
          </b-button>
          <b-button
            type="reset"
            variant="outline-secondary"
            @click="reset"
            pill
          >
            Reset
          </b-button>
        </b-form-group>
      </b-form>
    </validation-observer>
  </b-modal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { required } from "@validations";
import VuePerfectScrollbar from "vue-perfect-scrollbar";
import draggable from "vuedraggable";
import util from "@/util.js";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    VuePerfectScrollbar,
    draggable,
  },
  mixins: [util],
  data() {
    return {
      perfectScrollbarSettings: {
        maxScrollbarLength: 150,
        wheelPropagation: false,
        useBothWheelAxes: false,
        suppressScrollX: true,
      },
      name: "",
      codeName: "",
      availablePermissionSearch: "",
      allowedPermissionSearch: "",
      required,
      availablePermissionList: [],
      allowedPermissionList: [],
    };
  },
  async mounted() {
    try {
      const res = await this.getPermissions();
      this.availablePermissionList = res.data;
    } catch (error) {
      this.displayError(error);
    }
  },
  methods: {
    ...mapActions({
      createRole: "appData/createRole",
      getPermissions: "appData/getPermissions",
    }),
    async validationForm() {
      const success = await this.$refs.roleCreateFormValidation.validate();
      if (success) {
        await this.submit();
      }
    },
    async submit() {
      try {
        const permissions_id = this.allowedPermissionList.map((permission) => {
          return permission.id;
        });

        const res = await this.createRole({
          name: this.name,
          code_name: this.codeName,
          permissions: this.allowedPermissionList,
          permissions_id,
          created_by: this.getLoggedInUser.id,
          updated_by: this.getLoggedInUser.id,
        });
        if (res.status === 201) {
          this.$swal({
            title: "Role created successfully",
            icon: "success",
          });
          await this.resetModal();
          this.$nextTick(() => {
            this.$bvModal.hide("role-create-modal");
          });
          this.$emit("modalClosed");
        }
      } catch (error) {
        this.displayError(error);
      }
    },
    reset() {
      this.availablePermissionList = [
        ...new Set([
          ...this.availablePermissionList,
          ...this.allowedPermissionList,
        ]),
      ];
      this.allowedPermissionList = [];
    },
    resetModal() {
      this.name = "";
      this.codeName = "";
      this.availablePermissionList = [];
      this.allowedPermissionList = [];
    },
  },
  computed: {
    ...mapGetters({ getLoggedInUser: "appData/getLoggedInUser" }),
    filterAvailablePermissionByName: function () {
      return this.availablePermissionList.filter(
        (permission) =>
          !permission.name
            .toLowerCase()
            .indexOf(this.availablePermissionSearch.toLowerCase())
      );
    },
    filterAllowedPermissionByName: function () {
      return this.allowedPermissionList.filter(
        (permission) =>
          !permission.name
            .toLowerCase()
            .indexOf(this.allowedPermissionSearch.toLowerCase())
      );
    },
  },
};
</script>

<style lang="scss" scoped>
.scroll-area-size {
  height: 45vh;
}

.scroll-area-size ul {
  height: 100%;
}
</style>
