<template>
  <EditableProTable
      :mode="radio"
      :columns="column"
      :data="query.params"
      ref="table"
      @onChange="onChange"
      @del="deleteAction"
      @add="addAction"
  />
</template>

<script setup lang="ts">
import EditableProTable from "@/components/Table/EditableProTable/index.vue";
import {ref, reactive} from "vue";
import {ElMessage} from "element-plus";
import {deepObjClone} from "@/utils"

const emit = defineEmits(['updateRouter'])

const query = reactive({
  params: []
});
const radio = ref('bottom')

const table = ref()

const routerPath = ref()

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

const dataSource = ref(query.params)
const onChange = (val) => {
  dataSource.value = val
  let obj = dataSource.value
  if (obj.length){
    let newRouter = []
    let routerAdd = function(key: any, value: any) {
      return key + '=' + value
    }
    for (let i = 0; i < obj.length; i++) {
      console.log(query.params[i])
      newRouter.push(routerAdd(obj[i]['name'], obj[i]['value']))
    }
    routerPath.value = '?' + newRouter.join('&')
    emit('updateRouter', routerPath.value)
  }
}

const deleteAction = (row) => {
  let newRouter = []
  let newRout = routerPath.value.split('?')[1]
  let tagRout = row['name'] + '=' + row['value']
  let arrRout = newRout.split("&")
  for (let i = 0; i < arrRout.length; i++) {
    if (arrRout[i] != tagRout && arrRout.length>1) {
      newRouter.push(arrRout[i])
    }
  }
  routerPath.value = '?' + newRouter.join('&')
  emit('updateRouter', routerPath.value)
  ElMessage.success('点击删除')
}

const addAction = (row) => {
  console.log('添加', row)
  ElMessage.success('点击添加')
}

const setData = (data) => {
  query.params = data ? data : []
}

const getData = () => {
  query.params = deepObjClone(dataSource.value)
  return query.params
}

defineExpose({
  setData,
  getData
})
</script>

<style scoped lang="scss">

</style>