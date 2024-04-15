<template>
  <el-dialog
             @close="close"
             v-model="dialog"
             :title="title"
             :show-close="false"
             class="databaseWidth">
    <el-form autoComplete="on" :model="form" :rules="rules" ref="ruleFormRef"
             label-position="right"
             label-width="100px">
      <el-form-item label="数据库名称" :required="true" prop="database">
        <el-input v-model="form.database" placeholder="请输入数据库名称"></el-input>
      </el-form-item>
      <el-form-item label="地址" :required="true" prop="host">
        <el-input v-model="form.host" placeholder="请输入地址">></el-input>
      </el-form-item>
      <el-form-item label="端口" :required="true" prop="port">
        <el-input v-model="form.port" placeholder="请输入端口号">></el-input>
      </el-form-item>
      <el-form-item label="账号" :required="true" prop="user">
        <el-input v-model="form.user" placeholder="请输入账号">></el-input>
      </el-form-item>
      <el-form-item label="密码" :required="true" prop="password">
        <el-input v-model="form.password" placeholder="请输入密码">></el-input>
      </el-form-item>
    </el-form>
    <div class="pull-right">
      <el-button type="success" @click="DbSettingTest(ruleFormRef)">测试连接</el-button>
      <el-button type="primary" @click="onSureClick(ruleFormRef)">确 认</el-button>
      <el-button @click="dialog = false">取消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>

import {reactive, ref} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {databaseCreate, databaseUpdate, databaseDebug} from "@/api/setting";
import {showErrMessage} from "@/utils/element";

const dialog = ref<boolean>(false)

let form = reactive({
  database: '',
  host: '',
  port: '',
  user: '',
  password: ''
})

const ruleFormRef = ref<FormInstance>()

const pk = ref()

const title = ref()

const rules = reactive({
  database: [{required: true, trigger: "blur", message: "请输入数据库名称！"}],
  host: [{required: true, trigger: "blur", message: "请输入地址！"}],
  port: [{required: true, trigger: "blur", message: "请输入端口！"}],
  user: [{required: true, trigger: "blur", message: "请输入账号！"}],
  password: [{required: true, trigger: "blur", message: "请输入密码！"}],
})

const emits = defineEmits(['queryList'])

function close() {
  ruleFormRef.value.resetFields()
  Object.keys(form).forEach(key=>{
    form[key] = null
  })
  emits('queryList');
}

const DbSettingTest = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      const ret = await databaseDebug(form)
      const {code, data, msg} = ret.data
      showErrMessage(code.toString(), msg)
    } else {
      console.log('error submit!')
      ElMessage.error("数据库新增失败请重试!")
      return false
    }
  })
}

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      let ret: any = null
      console.log(pk.value)
      if(pk.value){
        form["id"] = pk.value
        ret = await databaseUpdate(form)
      } else {
        ret = await databaseCreate(form)

      }
      const {code, data, msg} = ret.data
      dialog.value = false
      showErrMessage(code.toString(), msg)
      formName.resetFields()
    } else {
      console.log('error submit!')
      ElMessage.error("数据库新增失败请重试!")
      return false
    }
  })
}

const show = (item={})=>{
  title.value = '新增数据库'
  if(item.id){
    title.value = '编辑数据库'
    pk.value = item.id
    Object.keys(item).forEach(key=>{
      form.database = item.database
      form.host = item.host
      form.port = item.port
      form.user = item.user
      form.password = item.password
    })
  }
  dialog.value = true
}

defineExpose({
  show,
})

</script>

<style lang="scss">
.databaseWidth {
  width: 30%;
  height: 55%
}

.pull-right {
  float: right;
}
</style>
