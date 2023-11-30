<template>
  <div class="app-container m-user">
    <Side @change="changeAction"/>
    <Table ref="table"/>
  </div>
</template>

<script lang="ts" setup>
  import Table from './components/Table.vue'
  import Side from './components/Side.vue'
  import { ref } from "vue";

  const table = ref()
  const queryParams = ref()

  const changeAction = (data)=>{
    queryParams.value = data.value
    table.value.getList(queryParams.value)
  }
</script>

<style scoped lang="scss">
@import "./index";
</style>
