<template>
  <el-dialog
      class="api-info-list"
      draggable
      title="添加接口"
      v-model="state.showDatabaseList"
      width="60%">
    <DatabaseList ref="databaseListRef" style="width: 100%"></DatabaseList>

    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="addDbSetting">添加</el-button>
      </span>
    </template>
  </el-dialog>

</template>

<script setup name="SelectDatabase">
import {reactive, ref} from 'vue';
import DatabaseList from "@/views/system/database/index.vue";

const emit = defineEmits(['addDbSetting'])

const databaseListRef = ref()

const state = reactive({
  showDatabaseList: false,
});

const getSelectionData = () => {
  return databaseListRef.value.getData()
}


const addDbSetting = () => {
  emit("addDbSetting")
  onOpenDatabaseList()
}

const onOpenDatabaseList = () => {
  state.showDatabaseList = !state.showDatabaseList
}

defineExpose({
  getSelectionData,
  onOpenDatabaseList,
})

</script>

<style lang="scss" scoped>

</style>