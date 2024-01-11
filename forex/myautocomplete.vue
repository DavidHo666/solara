<template>
  <v-autocomplete
    :label="label.toLowerCase()"
    :items="values"
    v-model="value"
    :search-input.sync="keyword"
    :style="style"
  ></v-autocomplete>
</template>

<script>
export default {
  props: {
    label: String,
    values: Array,
    keyword: String,
  }
  // watch: {
  //   keyword: function (newVal) {
  //     console.log('keyword changed', newVal);
  //     // this.$emit('update_keyword', newVal);
  //     this.keyword(newVal);
  //   }
  // }
}
</script>
