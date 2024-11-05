<template>
  <el-table :data="sate.params" style="width: 100%" row-key="id" border size="small" :show-header="false">
    <el-table-column label="参数名" width="160px" prop="name">
      <template #default="scope">
        <el-input
            size="small"
            clearable
            placeholder="请输入参数名"
            :value="scope.row.name"
            v-model.trim="scope.row.name"
        ></el-input>
      </template>
    </el-table-column>
    <el-table-column label="参数值" width="160px" prop="value">
      <template #default="scope">
        <el-input
            size="small"
            clearable
            placeholder="请输入参数值"
            :value="scope.row.value"
            v-model.trim="scope.row.value"
        ></el-input>
      </template>
    </el-table-column>
    <el-table-column label="参数描述" prop="value">
      <template #default="scope">
        <el-input
            size="small"
            clearable
            placeholder="请输入参数描述"
            :value="scope.row.description"
            v-model.trim="scope.row.description"
        ></el-input>
      </template>
    </el-table-column>
    <el-table-column prop="operator" label="操作" width="300px" fixed="right">
      <template #default="scope">
        <el-popover
            trigger="click"
            v-model:visible="scope.row.visible"
            placement="top"
            :width="160"
            size="small"
        >
          <p style="display: flex; align-items: center; margin-bottom: 10px">
            <el-icon color="#faad14" style="margin-right: 10px"><warning-filled /></el-icon>
            删除此行？</p
          >
          <div style="text-align: right; margin: 0">
            <el-button size="small" @click="scope.row.visible = false">取消</el-button>
            <el-button size="small" type="primary" @click="deleteAction(scope)"
            >确定</el-button
            >
          </div>
          <template #reference>
            <el-button icon="Delete" @click="deleteCurrent(scope.row)" type="danger" size="small"
            >删除</el-button
            >
          </template>
        </el-popover>
      </template>
    </el-table-column>
  </el-table>
  <div style="margin-top: 15px">
    <el-button style="width: 100%" @click="add" size="small">
      <el-icon style="margin-right: 4px"><plus /></el-icon> 添加一行数据</el-button
    >
  </div>
</template>

<script setup lang="ts">
import {reactive} from "vue";

const sate = reactive({
  params: []
});

const add = (row:any) => {
  let obj = {name: "", value: "", description: ""};
  sate.params.push(obj);
}

const deleteAction = (scope: any) => {
  scope.row.visible = false
  sate.params.splice(scope.$index, 1)
}

const deleteCurrent = (row:any) => {
  // pass
}

const setData = (data:any) => {
  data = eval(data)
  sate.params = data ? data : []
}

const getData = () => {
  return sate.params
}

defineExpose({
  setData,
  getData
})
</script>

<style scoped lang="scss">
.edit-input {
  padding-right: 100px;
}
.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
.inline-edit-table {
  width: 100%;
}
</style>