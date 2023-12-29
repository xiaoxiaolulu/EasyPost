<template>
  <div class="app-container m-user">
    <Side ref="side" @change="changeAction" @switch="switchCurrent"/>
    <Table ref="table"/>
  </div>
</template>

<script lang="ts" setup>
  import Table from './components/Table.vue'
  import Side from './components/Side.vue'
  import {onMounted, ref} from "vue";
  import {projectList} from "@/api/project";

  const table = ref()
  const queryParams = ref()
  const current = ref()
  const side = ref()

  const init = () => {
    projectList({}).then((response) => {
      let res = response.data.results
      let currentProject = res[0]['id']
      table.value.setCurrentProject(currentProject)
      table.value.queryList()
      side.value.setProjectList(res)
      side.value.queryList()
    }).catch((error) => {
    })
  }

  const changeAction = (data)=>{
    queryParams.value = data.value
    table.value.getList(queryParams.value)
  }

  const switchCurrent = (data) => {
    current.value = data.value
    table.value.setCurrentProject(current.value)
    table.value.queryList()
  }

  onMounted(() => {
    init()
  })
</script>

<style scoped lang="scss">
@import "./index";
</style>
