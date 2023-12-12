<template>
  <EditableProTable
      :mode="radio"
      :columns="column"
      :data="sate.params"
      @add="add"
      ref="table"
      @onChange="onChange"
      @del="deleteAction"
  />
</template>

<script setup lang="ts">
import EditableProTable from "@/components/Table/EditableProTable/index.vue";
import {reactive, ref} from "vue";
import {ElMessage} from "element-plus";
import {deepObjClone} from "@/utils";

const sate = reactive({
  params: []
});
const radio = ref('bottom')

const table = ref()

const column = [
  {name: 'name', label: '参数名', width: 160},
  {name: 'value', label: '参数值', width: 160},
  {name: 'description', label: '参数描述', valueType: 'input'}
]

const add = (row) => {
}
const dataSource = ref(sate.params)

const onChange = (val) => {
  dataSource.value = val
}

const deleteAction = (row) => {
  console.log('删除', row)
  ElMessage.success('点击删除')
}

const setData = (data) => {
  data = eval(data)
  sate.params = data ? data : []
  table.value.getData(data)
}

const getData = () => {
  sate.params = deepObjClone(dataSource.value)
  return sate.params
}

const updateContentType = (mode: any, language: any, remove: any) => {
  let headerValue = ""
  switch (mode) {
    case "form_data":
      headerValue = ""
      break
    case "x_www_form_urlencoded":
      headerValue = "application/x-www-form-urlencoded"
      break
    case "raw":
      language = language.toLowerCase()
      if (language === "json") {
        headerValue = "application/json"
      } else if (language === "xml") {
        headerValue = "application/xml"
      } else if (language === "html") {
        headerValue = "text/html"
      } else if (language === "text") {
        headerValue = "text/plain"
      }
      break
  }
  // 查找带有Content-Type的请求头
  let contentType = '';
  sate.params.find(param => {
    if (param.name.toLowerCase() === 'content-type') {
      contentType = param.name;
    }
  });
  // 切换Raw更新原本Content-Type
  if (contentType) {
    sate.params = sate.params.filter(obj => Object.values(obj).every(value => value !== "Content-Type"))
  }
  if (headerValue) {
    sate.params.unshift({name: "Content-Type", value: headerValue, description: ""})
  }
  if (remove) {
    sate.params =  sate.params.filter(obj => Object.values(obj).every(value => value !== "Content-Type"));
  }
}

defineExpose({
  setData,
  getData,
  updateContentType
})
</script>

<style scoped lang="scss">

</style>