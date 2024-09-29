<template>
  <el-drawer
    v-model="state.openApiInfoPage"
    size="70%"
    append-to-body
    direction="rtl"
    destroy-on-close
    :with-header="true">
    <template #header>
      <strong>步骤详情</strong>
    </template>
    <ApiDetail :isView="true" :api_id="state.data.id"></ApiDetail>
  </el-drawer>

</template>

<script setup name="apiInfoController">
import {reactive} from 'vue';
import ApiDetail from "@/views/https/api/components/detail.vue";

const state = reactive({
  openApiInfoPage: false,
  data: null
})

const onOpenApiInfoPage = (data) => {
  state.data = data
  state.openApiInfoPage = !state.openApiInfoPage
}

defineExpose({
  onOpenApiInfoPage,
})
</script>

<style lang="scss" scoped>

.controller-content {
  padding: 5px 10px;
}
</style>