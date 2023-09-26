<template>
  <el-dialog @close="close" v-model="dialogVisible" :title="title" width="25%">
    <el-form
        ref="ruleFormRef"
        :model="ruleForm"
        :rules="rules"
        label-width="100px"
    >
      <el-form-item label="分组名称" prop="name">
        <el-input v-model="ruleForm.name" placeholder="请输入分组名称"/>
      </el-form-item>
    </el-form>
    <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleClose(ruleFormRef)">确定</el-button>
        </span>
    </template>
  </el-dialog>
</template>
<script lang="ts" setup>
import {ElMessage, FormInstance } from 'element-plus'
import {reactive, ref} from "vue";
import {updateTree} from "@/api/http";

const props = defineProps({
  rowData: {
    type: Object,
    default: () => {
    }
  }
})

const ruleFormRef = ref<FormInstance>()

const dialogVisible = ref<boolean>(false)

const title = ref('新增字典项')

const pk = ref()

const editPk = ref(0)

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入名称！"}],
})

const ruleForm = reactive({
  name: null,
})

const treeData = ref([])

const currentNode = ref()

const currentData = ref()

const minId = ref(0)

const maxId = ref(0)

function close() {
  ruleFormRef.value.resetFields()
  Object.keys(ruleForm).forEach(key=>{
    ruleForm[key] = null
  })
}

const show = (item={})=>{
  title.value = '新增字典项'
  if(item.id){
    title.value = '编辑字典项'
    editPk.value = item.id
    ruleForm.name = item.currentNode.label
    console.log("xxxxxx")
    console.log(item.id)
  }
  Object.keys(item).forEach(key=>{
    pk.value = item.pk
    treeData.value = item.treeData
    currentNode.value = item.currentNode
    currentData.value = item.currentData
    minId.value = item.maxId
  })
  dialogVisible.value = true
}

const append = (data: any) => {
  let pk: number
  if(maxId.value==0){
    pk = minId.value
  }
  if (maxId.value!=0){
    pk = maxId.value
  }
  const newChild = {
    id: ++pk,
    label: ruleForm.name,
    parent: data.value.id,
    children: []
  };

  if (data === '' || treeData.value.length === 0) {
    treeData.value.push(newChild) ;
    return
  }
  if (!data.value.children) {
    data.value.children = []
  }
  data.value.children.push(newChild);
  ElMessage.success("添加分组成功");
}


const handleClose = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      if(editPk.value!=0){
        const parent = currentData.value.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === currentNode.value.id);
        children[index]["label"] = ruleForm.name
        updateTrees(pk.value, treeData.value);
      }else {
        append(currentNode);
        updateTrees(pk.value, treeData.value)
      }
      formName.resetFields()
      dialogVisible.value = false
      editPk.value = 0
    } else {
      ElMessage.error("更新目录失败请重试!")
      return false
    }
  })
}


const updateTrees = (pk, treeData) => {
  updateTree({
    id: pk,
    body: treeData,
  }).then((response) => {
    const {data, code, msg} = response.data
    maxId.value = data.maxId
    treeData.value = data.tree
  }).catch((error) => {
    console.log(error)
    ElMessage.error("更新树形结构数据失败;请重试!");
  })
}

defineExpose({
  show,
  updateTrees
})

</script>
<style lang="scss" scoped>

</style>

