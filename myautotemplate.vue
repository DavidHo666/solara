<template>
  <v-autocomplete
    :label="label"
    :items="filteredItems"
    :search-input.sync="search"
  ></v-autocomplete>
</template>

<script>
export default {
  props: {
    label: String,
    values: Array
  },
  data() {
    return {
      search: null
    };
  },
  computed: {
    filteredItems() {
      if (!this.search) return this.values.slice(0, 10);
      return this.values.filter(values => values.toLowerCase().includes(this.search.toLowerCase())).slice(0, 10);
    }
  }
}
</script>
