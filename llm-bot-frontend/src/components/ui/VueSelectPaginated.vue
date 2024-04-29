<template>
  <validation-provider #default="{ errors }" :name="name" :rules="rules">
    <b-form-group class="labelStyle">
      <template #label>
        {{ name }}
        <span class="text-danger" v-if="rules === 'required'">*</span>
      </template>
      <v-select
        v-model="selected"
        :dir="$store.state.appConfig.isRTL ? 'rtl' : 'ltr'"
        :label="label"
        :multiple="multiple"
        :options="filtered"
        :filterable="false"
        :disabled="disabled"
        @open="onOpen"
        @close="onClose"
        @search="(query) => (search = query)"
        class="vSelectStyle"
        :placeholder="`${name}`"
        @input="(item) => $emit('setMethod', item)"
      >
        <template #list-footer>
          <li v-show="hasNextPage" ref="load" class="loader">
            Loading more options...
          </li>
        </template>
      </v-select>
      <b-form-invalid-feedback :state="errors.length > 0 ? false : null">
        {{ errors[0] }}
      </b-form-invalid-feedback>
    </b-form-group>
  </validation-provider>
</template>

<script>
import { ValidationProvider, ValidationObserver } from "vee-validate";
import util from "@/util.js";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  props: {
    name: String,
    label: String,
    rules: String,
    multiple: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    parameters: Object,
    prevSelected: Number,
    getMethod: Function,
    getListMethod: Function,
  },
  mixins: [util],
  data: () => ({
    observer: null,
    search: "",
    results: [],
    selected: null,
    currentPage: 1,
    hasNextPage: false,
  }),
  async mounted() {
    this.observer = new IntersectionObserver(this.infiniteScroll);

    try {
      if (this.prevSelected) {
        const res = await this.getMethod({
          pk: this.prevSelected,
        });
        this.results.push(res.data);
        this.selected = res.data;
        this.$emit("setMethod", this.selected);
      }

      await this.fetchPaginatedData();
    } catch (error) {
      this.displayError(error);
    }
  },
  methods: {
    async fetchPaginatedData() {
      try {
        let data = {
          pageNumber: this.currentPage,
        };
        if (this.parameters) {
          data = {
            ...data,
            ...this.parameters,
          };
        }

        const res = await this.getListMethod(data);
        for (let i = 0; i < res.data.results.length; i++) {
          const element = res.data.results[i];
          if (!this.results.find((e) => e.id === element.id)) {
            this.results.push(element);
          }
        }
        res.data.next ? (this.hasNextPage = true) : (this.hasNextPage = false);
      } catch (error) {
        console.log(error);
        this.displayError(error);
      }
    },
    async onOpen() {
      if (this.hasNextPage) {
        await this.$nextTick();
        this.observer.observe(this.$refs.load);
      }
    },
    onClose() {
      this.observer.disconnect();
    },
    async infiniteScroll([{ isIntersecting, target }]) {
      if (isIntersecting) {
        const ul = target.offsetParent;
        const scrollTop = target.offsetParent.scrollTop;

        this.hasNextPage = false;
        this.currentPage += 1;
        await this.fetchPaginatedData();

        await this.$nextTick();
        ul.scrollTop = scrollTop;
      }
    },
  },
  computed: {
    filtered() {
      return this.results.filter((item) =>
        item
      );
    },
  },
  watch: {
    prevSelected: {
      async handler(newValue, oldValue) {
        if (newValue) {
          const res = await this.getMethod({
            pk: newValue,
          });
          if (!this.results.find((e) => e.id === res.data.id)) {
            this.results.push(res.data);
          }
          this.selected = res.data;
          this.$emit("setMethod", this.selected);
        }
      },
    },
  },
};
</script>

<style lang="scss">
.loader {
  text-align: center;
  color: #bbbbbb;
}
.vSelectStyle .vs__deselect {
  fill: #fff !important;
}
.labelStyle legend {
  display: block;
  color: #5e5873;
  font-size: 0.857rem;
  padding-bottom: 0;
  margin-bottom: 0.2857rem;
}
</style>
