<template>
  <el-table :data="query.params" style="width: 100%" row-key="id" border size="small" :show-header="false">
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
    <el-table-column label="请选择类型" prop="type" width="160px">
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
import {ref, reactive} from "vue";
import {ElMessage} from "element-plus";
import {deepObjClone} from "@/utils"

const emit = defineEmits(['updateRouter'])

const query = reactive({
  params: []
});

const routerPath = ref()

const type = [
      {
        value: 'Boolean',
        label: 'Boolean',
      },
      {
        value: 'Date',
        label: 'Date',
      },
      {
        value: 'Number',
        label: 'Number',
      },
      {
        value: 'Float',
        label: 'Float',
      },
      {
        value: 'Integer',
        label: 'Integer',
      },
      {
        value: 'String',
        label: 'String',
      }
]

const deleteCurrent = (row) => {
  // pass
}

const add = (row) => {
  let obj = {name: "", value: "", description: ""};
  query.params.push(obj);
  // 同步地址参数
  // if (query.params.length){
  //   let newRouter = []
  //   let routerAdd = function(key: any, value: any) {
  //     return key + '=' + value
  //   }
  //   for (let i = 0; i < query.params.length; i++) {
  //     console.log(query.params[i])
  //     newRouter.push(routerAdd(obj[i]['name'], obj[i]['value']))
  //   }
  //   routerPath.value = '?' + newRouter.join('&')
  //   emit('updateRouter', routerPath.value)
  // }
}

const deleteAction = (scope) => {
  scope.row.visible = false
  query.params.splice(scope.$index, 1)
  // 同步地址参数
  // let newRouter = []
  // let newRout = routerPath.value.split('?')[1]
  // let tagRout = scope.row['name'] + '=' + scope.row['value']
  // let arrRout = newRout.split("&")
  // for (let i = 0; i < arrRout.length; i++) {
  //   if (arrRout[i] != tagRout && arrRout.length>1) {
  //     newRouter.push(arrRout[i])
  //   }
  // }
  // routerPath.value = '?' + newRouter.join('&')
  // emit('updateRouter', routerPath.value)
  // ElMessage.success('点击删除')
}

const setData = (data) => {
  query.params = data ? data : []
}

const getData = () => {
  return query.params
}

defineExpose({
  setData,
  getData
})
</script>

<style scoped lang="scss">

</style>