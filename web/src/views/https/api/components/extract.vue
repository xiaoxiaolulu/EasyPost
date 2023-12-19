<template>
  <el-table :data="sate.params" style="width: 100%" row-key="id" border size="small" :show-header="false">
    <el-table-column label="变量名" width="160px" prop="name">
      <template #default="scope">
        <el-input
            size="small"
            clearable
            placeholder="请输入变量名"
            :value="scope.row.name"
            v-model.trim="scope.row.name"
        ></el-input>
      </template>
    </el-table-column>
    <el-table-column label="请选择提取方式" prop="type" width="160px">
      <template #default="scope">
        <el-select
            size="small"
            clearable
            :placeholder="`请选择`"
            v-model="scope.row.type"
        >
          <el-option
              v-for="ite in type"
              :key="ite.value"
              :label="ite.label"
              :value="ite.value"
          />
        </el-select>
      </template>
    </el-table-column>
    <el-table-column label="变量值" prop="value">
      <template #default="scope">
        <el-input
            size="small"
            clearable
            placeholder="请输入变量值"
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
import {ref, reactive} from "vue";
import {ElMessage} from "element-plus";
import {deepObjClone} from "@/utils";

const sate = reactive({
  params: []
});

const type = [
      {
        value: 'jsonpath',
        label: 'jsonpath',
      },
      {
        value: 're',
        label: 're',
      }
]

const deleteCurrent = (row) => {
  // pass
}

const add = (row) => {
  let obj = {name: "", type: "", description: ""};
  sate.params.push(obj);
}

const deleteAction = (scope) => {
  scope.row.visible = false
  sate.params.splice(scope.$index, 1)

}

const setData = (data) => {
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

</style>