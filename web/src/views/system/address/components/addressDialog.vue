<template>
  <el-dialog
             @close="close"
             v-model="dialog"
             :title="title"
             :show-close="false"
             class="addressWidth">
    <el-form autoComplete="on" :model="form" :rules="rules" ref="ruleFormRef"
             label-position="right"
             label-width="100px">
      <el-form-item label="环境" :required="true" prop="env">
        <el-select
            class="selectOpt" v-model="form.env" placeholder="请选择"
            :popper-append-to-body="false"
            style="width: 150px;"
        >
          <el-option
              v-for="item in envOption"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="地址名称" :required="true" prop="name">
        <el-input v-model="form.name" placeholder="请输入地址名称"></el-input>
      </el-form-item>
      <el-form-item label="服务地址" :required="true" prop="host">
        <el-input v-model="form.host" placeholder="请输入服务名称">></el-input>
      </el-form-item>
    </el-form>
    <div class="pull-right">
      <el-button type="primary" @click="onSureClick(ruleFormRef)">确 认</el-button>
      <el-button @click="dialog = false">取消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>

import {computed, reactive, ref, watch} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {addressCreate, addressUpdate} from "@/api/setting";
import {showErrMessage} from "@/utils/element";

const dialog = ref<boolean>(false)

const props = defineProps({
  rowData: {
    type: Object,
    default: () => {
    }
  }
})

const envOption = ref([])

let form = reactive({
  name: '',
  env: '',
  host: '',
})

const ruleFormRef = ref<FormInstance>()

const pk = ref()

const title = ref()

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入环境名称！"}],
  env: [{required: true, trigger: "blur", message: "请输选择环境！"}],
  host: [{required: true, trigger: "blur", message: "请输入服务地址！"}],
})

const emits = defineEmits(['queryList'])

function close() {
  ruleFormRef.value.resetFields()
  Object.keys(form).forEach(key=>{
    form[key] = null
  })
  emits('queryList');
}

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      let ret: any = null
      console.log(pk.value)
      if(pk.value){
        form["id"] = pk.value
        ret = await addressUpdate(form)
      } else {
        ret = await addressCreate(form)

      }
      const {code, data, msg} = ret.data
      dialog.value = false
      showErrMessage(code.toString(), msg)
      formName.resetFields()
    } else {
      console.log('error submit!')
      ElMessage.error("地址新增失败请重试!")
      return false
    }
  })
}

const show = (item={})=>{
  title.value = '新增地址'
  if(item.id){
    title.value = '编辑地址'
    pk.value = item.id
    Object.keys(item).forEach(key=>{
      form.name = item.name
      form.host = item.host
      form.env = item.env.id
    })
  }
  dialog.value = true
}

watch(() => props.rowData, () => {
  envOption.value = props.rowData.envList
}, {deep: true, immediate: true})

defineExpose({
  show,
})

</script>

<style lang="scss">
.addressWidth {
  width: 30%;
  height: 40%
}

.pull-right {
  float: right;
}
</style>
