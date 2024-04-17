<template>
  <div>
    <div>
      <el-form :inline="true">
        <el-form-item>
          <el-button
              link
              size="small"
              :icon="Plus"
              @click="selectDatabase">
            添加关联
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button
              link
              size="small"
              :icon="Delete"
              @click="cancelDatabase">
            删除关联
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    <div style="margin-top: 15px" v-show="selectDbData">
      <el-table
          :header-cell-style="{ color: '#adaaaa', fontSize: '13px', fontWeight: 'bold'}"
          :data="tableData"
          @selection-change="handleSelectionChange"
          style="width: 100%"
          ref="dragTable"
          row-key="id"
          border
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="database" label="数据库名称"></el-table-column>
        <el-table-column prop="host" label="地址"></el-table-column>
        <el-table-column prop="port" label="端口"></el-table-column>
        <el-table-column prop="user" label="账号"></el-table-column>
        <el-table-column prop="password" label="密码"></el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="200px">
          <template #default="scope">
            <span>{{parseTime(scope.row.create_time)}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="update_time" label="更新时间" width="200px">
          <template #default="scope">
            <span>{{parseTime(scope.row.update_time)}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建者">
          <template #default="scope">
            <div style="margin-inline-end:16px;display:inline">
              <img v-if="scope.row.creator.avatar" :src="scope.row.creator.avatar" class="avatar" alt="">
            </div>
            <div style="display:inline;color: rgba(0, 0, 0, 0.88);">
              <span style="color:rgb(22, 119, 255)">{{ scope.row.creator.username }}</span>
            </div>
          </template>
        </el-table-column>
      </el-table>
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
import {Delete, Plus} from "@element-plus/icons-vue";
import DbConfig from "@/views/system/env/components/dbConfig.vue";
import {reactive, ref} from "vue";
import {parseTime} from "@/utils";

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

const selectDbData = ref([
])

const tableData = ref([
])

const dbControllerRef = ref()

const selectionData = ref()

const changeAction = (data:any) => {
  selectDbData.value = data
  setData(data)
}

const setData = (data:any) => {
  for (let i = 0; i < data.length; i++) {
    tableData.value.push(data[i])
  }
}

const getData = () => {
  return tableData.value.length > 0 ? tableData.value : selectDbData.value
}

const selectDatabase = () => {
  dbControllerRef.value.handleAddData()
}

const cancelDatabase = () => {
  const newArray= []
  for (let i = 0; i < tableData.value.length; i++) {
    if (JSON.stringify(tableData.value[i]) != JSON.stringify(selectionData.value[i])) {
      newArray.push(tableData.value[i]);
    }
  }
  tableData.value = newArray
}

const handleSelectionChange = (val: any) => {
  selectionData.value = val
}

defineExpose({
  setData,
  getData
})
</script>
<style scoped lang="scss">

</style>