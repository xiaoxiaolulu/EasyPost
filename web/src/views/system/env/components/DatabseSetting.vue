<template>
  <div>
    <div>
      <el-form :inline="true">
        <el-form-item>
          <el-button
              type="text"
              size="small"
              :icon="Plus"
              @click="selectDatabase">
            添加关联
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button
              type="text"
              size="small"
              :icon="Delete"
              @click="cancelDatabase">
            删除关联
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    <div>
      <db-config
          ref="dbControllerRef"
          style="margin-bottom: 10px"
          v-model="state.form.database_data"
          @change="changeAction"
      ></db-config>
    </div>
  </div>
</template>
<script setup lang="ts">
import {Plus, Delete} from "@element-plus/icons-vue";
import DbConfig from "@/views/system/env/components/dbConfig.vue";
import {reactive, ref} from "vue";
import {getStepTypesByUse} from "@/utils";

const createForm = () => {
  return {
    name: '',
    remarks: '',
    priority: '',
    database_data: []
  }
}

const state = reactive({
  form: createForm(),
})

const selectDbData = ref()

const tableData = reactive([
])

const changeAction = (data:any) => {
  selectDbData.value = data
  setData(data)
}

const setData = (data:any) => {
  for (let i = 0; i < data.length; i++) {
    tableData.push(data[i])
  }
}
const dbControllerRef = ref()


const selectDatabase = () => {
  dbControllerRef.value.handleAddData()
}

const cancelDatabase = () => {
}
</script>
<style scoped lang="scss">

</style>