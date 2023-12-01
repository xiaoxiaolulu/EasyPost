<template>
  <EditableProTable
      :mode="radio"
      :columns="column"
      :data="data.params"
      @add="add"
      ref="table"
      @onChange="onChange"
      @del="deleteAction"
  />
</template>

<script setup lang="ts">
import EditableProTable from "@/components/Table/EditableProTable/index.vue";
import {ref, reactive} from "vue";
import {ElMessage} from "element-plus";
import {deepObjClone} from "@/utils";

const data = reactive({
  params: []
});
const radio = ref('bottom')

const table = ref()

const column = [
  {
    name: 'type',
    label: '提取来源',
    options: [
      {
        value: 'ResponseJson',
        label: 'ResponseJson',
      },
      {
        value: 'ResponseText',
        label: 'ResponseText',
      },
      {
        value: 'ResponseHeaders',
        label: 'ResponseHeaders',
      },
      {
        value: 'ResponseCookie',
        label: 'ResponseCookie',
      }
    ],
    valueType: 'select',
    width: 120
  },
  {name: 'name', label: '变量名', width: 160},
  {
    name: 'type',
    label: '提取方式',
    options: [
      {
        value: 'jsonpath',
        label: 'jsonpath',
      },
      {
        value: 're',
        label: 're',
      }
    ],
    valueType: 'select',
    width: 120
  },
  {name: 'value', label: '变量值'},
]

const add = (row) => {
}
const dataSource = ref(data.params)
const onChange = (val) => {
  dataSource.value = val
}

const deleteAction = (row) => {
  console.log('删除', row)
  ElMessage.success('点击删除')
}

const setData = (data) => {
  data.params = data ? data : []
}

const getData = () => {
  data.params = deepObjClone(dataSource.value)
  return data.params
}

defineExpose({
  setData,
  getData
})
</script>

<style scoped lang="scss">

</style>