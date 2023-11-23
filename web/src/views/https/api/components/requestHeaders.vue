<template>
  <EditableProTable
      :mode="radio"
      :columns="column"
      :data="list"
      @add="add"
      ref="table"
      :editableKeys="editableKeys"
      @onChange="onChange"
      @del="deleteAction"
  />
</template>

<script setup lang="ts">
import EditableProTable from "@/components/Table/EditableProTable/index.vue";
import {ref} from "vue";
import {ElMessage} from "element-plus";

const radio = ref('bottom')

const table = ref()

const column = [
  {name: 'name', label: '参数名', width: 160},
  {name: 'value', label: '参数值', width: 160},
  {
    name: 'type',
    label: '类型',
    options: [
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
      },
    ],
    valueType: 'select',
    width: 120
  },
  {name: 'description', label: '参数描述', valueType: 'input'}
]


let data = [
  {
    id: 6247418504,
    title: '活动名称一',
    readonly: '活动名称一',
    decs: '这个活动真好玩',
    state: 1,
    created_at: '2020-05-26',
    update_at: '2020-05-26',
  },
  {
    id: 6246921229,
    title: '活动名称二',
    readonly: '活动名称二',
    decs: '这个活动真好玩',
    state: 0,
    created_at: '2020-05-26',
    update_at: '2020-05-26',
  },
  {
    id: 6242991229,
    title: '活动名称三',
    readonly: '活动名称三',
    decs: '这个活动真好玩',
    state: 1,
    created_at: '2020-05-26',
    update_at: '2020-05-26',
  },
  {
    id: 6242981229,
    title: '活动名称四',
    readonly: '活动名称四',
    decs: '这个活动真好玩',
    state: 1,
    created_at: '2020-05-26',
    update_at: '2020-05-26',
  },

]

let arrKeys = data
    .map((item) => item.id)
    .filter((item) => ![6247418504, 6246921229].includes(item))
let editableKeys = ref(arrKeys)

const list = ref(data)

const add = (row) => {
}
const dataSource = ref(data)
const onChange = (val) => {
  dataSource.value = val
}

const deleteAction = (row) => {
  console.log('删除', row)
  ElMessage.success('点击删除')
}

</script>

<style scoped lang="scss">

</style>