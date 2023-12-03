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
  {name: 'name', label: '表达式'},
  {
    name: 'type',
    label: '类型',
    options: [
      {
        value: '相等',
        label: '相等',
      },
      {
        value: '不相等',
        label: '不相等',
      },
      {
        value: '约等于',
        label: '约等于',
      },
      {
        value: '不约等于',
        label: '不约等于',
      },
      {
        value: '大于',
        label: '大于',
      },
      {
        value: '大于等于',
        label: '大于等于',
      },
      {
        value: '小于',
        label: '小于',
      },
      {
        value: '小于等于',
        label: '小于等于',
      },
      {
        value: '包含',
        label: '包含',
      },
      {
        value: '不包含',
        label: '不包含',
      },
    ],
    valueType: 'select',
    width: 120
  },
  {name: 'value', label: '期望值', width: 160},
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