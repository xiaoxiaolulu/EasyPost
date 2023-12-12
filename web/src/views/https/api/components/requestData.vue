<template>
  <EditableProTable
      :mode="radio"
      :columns="column"
      :data="form.params"
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

const form = reactive({
  params: []
});
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

const add = (row) => {
}
const dataSource = ref(form.params)
const onChange = (val) => {
  dataSource.value = val
}

const deleteAction = (row) => {
  console.log('删除', row)
  ElMessage.success('点击删除')
}

const setData = (data) => {
  form.params = data ? data : []
  table.value.getData(data)
}

const getData = () => {
  form.params = deepObjClone(dataSource.value)
  return form.params
}

defineExpose({
  setData,
  getData
})
</script>

<style scoped lang="scss">

</style>