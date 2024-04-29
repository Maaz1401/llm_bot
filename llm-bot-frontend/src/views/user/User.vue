<template>
  <div>
    <div class="d-flex justify-content-center align-items-center flex-nowrap mb-1">

      <div class="
            d-flex
            justify-content-center
            align-items-center
            flex-nowrap
            mr-5
          ">
        <b-form-input id="usernameFilter" v-model="usernameFilter" placeholder="Search by username" />
      </div>

      <div class="
            d-flex
            justify-content-center
            align-items-center
            flex-nowrap
            mr-5
          ">
        <b-form-input id="nameFilter" v-model="nameFilter" placeholder="Search by name" />
      </div>

      <div class="
            d-flex
            justify-content-center
            align-items-center
            flex-nowrap
            mr-5
          ">
        <b-button variant="primary" pill @click="filter">
          <feather-icon icon="SearchIcon" class="mr-50" />
          <span class="align-middle">Search</span>
        </b-button>
      </div>

      <div class="
            d-flex
            justify-content-center
            align-items-center
            flex-nowrap
            mr-5
          ">
        <b-button variant="primary" pill @click="search">
          <feather-icon icon="RefreshCwIcon" class="mr-50" />
          <span class="align-middle">Refresh</span>
        </b-button>
      </div>
    </div>
    <b-card>
      <b-table responsive="sm" :fields="fields" :items="users" details-td-class="m-0 p-0" small
        v-if="hasPermission('user_read')">
        <template #cell(role_data)="row">
          {{ row.item.role_data ? row.item.role_data.name : "" }}
        </template>
        <template #cell(manage)="row">
          <b-button variant="info" pill size="sm" class="mr-1" @click="editUser(row.item)"
            v-if="hasPermission('user_update')">
            Edit
          </b-button>
        </template>
      </b-table>
      <div class="d-flex justify-content-center align-items-center flex-nowrap m-2">
        <b-pagination size="md" :total-rows="totalItems" v-model="currentPage" :per-page="perPage"></b-pagination>
      </div>
    </b-card>
    <user-edit-modal :user="user" @modalClosed="onModalClosed" :key="`edit-${userEditModalCount}`" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import UserEditModal from "@/components/user/UserEditModal.vue";
import util from "@/util.js";

export default {
  components: {
    UserEditModal,
  },
  data() {
    return {
      fields: [
        { key: "manage", label: "Manage" },
        { key: "id", label: "Id" },
        { key: "username", label: "Username", },
        { key: "name", label: "Name" },
        { key: "role_data", label: "Role" },
      ],
      currentPage: 1,
      perPage: 0,
      totalItems: 0,
      users: [],
      user: null,
      userEditModalCount: 0,
      usernameFilter: '',
      nameFilter: ''
    };
  },
  mixins: [util],
  async mounted() {
    await this.fetchPaginatedData();
  },
  methods: {
    ...mapActions({
      getUsers: "appData/getUsers",
      getGHQUsers: "appData/getGHQUsers",
    }),
    async filter() {
      this.currentPage = 1;
      await this.search();
    },
    async search() {
      await this.fetchPaginatedData();
    },
    async fetchPaginatedData() {
      try {
        // const res = await this.getUsers({
        //   pageNumber: this.currentPage,
        // });
        let tempParams = {
          pageNumber: this.currentPage,
        }
        if (this.usernameFilter) {
          tempParams['username'] = this.usernameFilter;
        }
        if (this.nameFilter) {
          tempParams['name'] = this.nameFilter;
        }
        const res = await this.getGHQUsers(tempParams);
        console.log(res.data)
        this.users = res.data.results;
        this.totalItems = res.data.count;
        this.perPage = res.data.per_page;
      } catch (error) {
        this.displayError(error);
      }
    },
    editUser(user) {
      this.user = user;
      this.userEditModalCount += 1;
      this.$nextTick(() => {
        this.$bvModal.show("user-edit-modal");
      });
    },
    async onModalClosed() {
      await this.fetchPaginatedData();
    },
  },
  computed: {
    ...mapGetters({
      hasPermission: "appData/hasPermission",
    }),
  },
  watch: {
    currentPage: async function (val) {
      await this.fetchPaginatedData();
    },
  },
};
</script>

<style></style>
