<template>
  <el-dialog
      class="api-info-list"
      draggable
      title="添加接口"
      v-model="state.showApiList"
      width="60%">
    <ApiList ref="apiListRef" style="width: 100%"></ApiList>

    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="addApiStep">添加</el-button>
      </span>
    </template>
  </el-dialog>

</template>

<script setup name="SelectApi">
import {reactive, ref} from 'vue';
import ApiList from "@/views/https/api/components/Table.vue";

const emit = defineEmits(['addApiStep'])

const apiListRef = ref()

const state = reactive({
  showApiList: false,
});

// 获取选中用例
const getSelectionData = () => {
  return apiListRef.value.getSelectionData()
}


const addApiStep = () => {
  emit("addApiStep")
  onOpenApiList()
}

const onOpenApiList = () => {
  state.showApiList = !state.showApiList
}

defineExpose({
  getSelectionData,
  onOpenApiList,
})

</script>

<style lang="scss" scoped>

</style>