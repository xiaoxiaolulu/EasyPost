<template>
  <el-dialog
      class="api-info-list"
      draggable
      title="添加用例"
      v-model="state.showCaseList"
      width="60%">
    <CaseList ref="apiCaseRef" style="width: 100%"></CaseList>

    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="addCase">添加</el-button>
      </span>
    </template>
  </el-dialog>

</template>

<script setup name="SelectCase">
import {reactive, ref} from 'vue';
import CaseList from "@/views/https/case/components/Table.vue";

const emit = defineEmits(['addCase'])

const apiCaseRef = ref()

const state = reactive({
  showCaseList: false,
});

// 获取选中用例
const getSelectionData = () => {
  return apiCaseRef.value.getSelectionData()
}


const addCase = () => {
  emit("addCase")
  onOpenCaseList()
}

const onOpenCaseList = () => {
  state.showCaseList = !state.showCaseList
}

defineExpose({
  getSelectionData,
  onOpenCaseList,
})

</script>

<style lang="scss" scoped>

</style>