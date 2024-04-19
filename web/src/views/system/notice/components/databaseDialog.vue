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
      <el-form-item label="通知名称" :required="true" prop="name">
        <el-input v-model="form.name" placeholder="写一个第三方通知名称，标记用途"></el-input>
      </el-form-item>
      <el-form-item label="触发事件" :required="true" prop="host">
        <el-select
          popper-class="custom-header"
          multiple
          clearable
          collapse-tags
          :max-collapse-tags="1"
          class="selectOpt" v-model="form.project" placeholder="请选择触发项目"
          :popper-append-to-body="false"
          style="width: 150px;"
        >
          <template #header>
            <el-checkbox
              v-model="checkAll"
              :indeterminate="indeterminate"
              @change="handleCheckAll"
            >
              全选
            </el-checkbox>
          </template>
          <el-option
            v-for="item in projectOption"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="通知渠道" :required="true" prop="port">
        <el-space :size="10" class="button-container">
          <el-check-tag
            class="custom-check-tag"
            v-for="(button, index) in buttons" @change="onChange(button)"
            :checked="button.checked" :key="index" style="width: 110px;height: 48px;margin-bottom: 10px">
            <SvgIcon :icon-class="button.svg"
                     style="width: 30px; height: 30px"/>
            <span class="content" style="">{{button.content}}</span>
          </el-check-tag>
        </el-space>
      </el-form-item>
      <el-form-item label="服务URL" :required="true" prop="user">
        <el-input v-model="form.user" placeholder="请输入账号"></el-input>
      </el-form-item>
    </el-form>
    <div class="pull-right">
      <el-button type="warning" @click="onSureClick(ruleFormRef)">确 认</el-button>
      <el-button @click="dialog = false">取消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import {reactive, ref, watch} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {} from "@/api/setting";
import {showErrMessage} from "@/utils/element";
import { projectList } from "@/api/project";
import SvgIcon from "@/components/SvgIcon/index.vue";

const dialog = ref<boolean>(false)

const checkAll = ref(false)

const indeterminate = ref(false)

let form = reactive({
  name: '',
  project: ref<CheckboxValueType[]>([]),
  host: '',
  port: '',
  user: '',
  password: ''
})

const ruleFormRef = ref<FormInstance>()

const pk = ref()

const title = ref()

const projectOption = ref([])

const buttons = ref([
  {id: 1,  content: '企业微信', checked: true, svg: 'qiyeweixin'},
  {id: 2, content: '钉钉', checked: false, svg: 'dingding'},
  {id: 3, content: '飞书', checked: false, svg: 'feishu'},
  {id: 4, content: 'Webhook', checked: false, svg: 'webhook'},
]);

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
  Object.keys(form).forEach(key => {
    form[key] = null
  })
  emits('queryList');
}

const handleCheckAll = (val: CheckboxValueType) => {
  indeterminate.value = false
  if (val) {
    form.project = projectOption.value.map((_) => _.value)
  } else {
    form.project = []
  }
}

const initProjectList = () => {
  projectList({}).then((response) => {
    let res = response.data.results
    for (let i = 0; i < res.length; i++) {
      projectOption.value.push({
        "label": res[i]["name"],
        "value": res[i]["id"],
        "avatar": res[i]["avatar"]
      })
    }
  }).catch((error) => {
  })
}

initProjectList()

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      let ret: any = null
      console.log(pk.value)
      if (pk.value) {
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

const show = (item = {}) => {
  title.value = '新增通知事件'
  if (item.id) {
    title.value = '编辑通知事件'
    pk.value = item.id
    Object.keys(item).forEach(key => {
      form.database = item.database
      form.host = item.host
      form.port = item.port
      form.user = item.user
      form.password = item.password
    })
  }
  dialog.value = true
}

watch(form.project, (val) => {
  if (val.length === 0) {
    checkAll.value = false
    indeterminate.value = false
  } else if (val.length === cities.value.length) {
    checkAll.value = true
    indeterminate.value = false
  } else {
    indeterminate.value = true
  }
})

defineExpose({
  show,
})

</script>

<style lang="scss">
.databaseWidth {
  width: 30%;
  height: 60%
}

.pull-right {
  float: right;
}

.custom-header {
  .el-checkbox {
    display: flex;
    height: unset;
  }
}

.button-container {
  display: flex;
  flex-wrap: wrap;
}

.custom-check-tag {
  background-color: #ffffff;
  border-style: solid;
  border-color: #f7f2fd;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 75px;
}

.content {
  margin-left: 15px;
  vertical-align: middle;
  font-family: STXihei,serif;
  color: #0e0f10;
  font-weight: normal;
  font-size: 12px;
  line-height: 20px;
}
</style>
