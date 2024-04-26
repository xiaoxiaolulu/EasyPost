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
      <el-form-item label="触发事件" prop="project">
        <el-select
          popper-class="custom-header"
          multiple
          clearable
          collapse-tags
          :max-collapse-tags="1"
          class="selectOpt" v-model="form.trigger_events" placeholder="请选择触发项目"
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
      <el-form-item label="通知渠道" prop="msg_type">
        <el-space :size="10" class="button-container">
          <el-check-tag
            class="custom-check-tag"
            v-for="(button, index) in buttons" @change="onChange(button)" v-model="form.msg_type"
            :checked="button.checked" :key="index" style="width: 110px;height: 48px;margin-bottom: 10px">
            <SvgIcon :icon-class="button.svg"
                     style="width: 30px; height: 30px"/>
            <span class="content" style="">{{button.content}}</span>
          </el-check-tag>
        </el-space>
      </el-form-item>
      <el-form-item label="服务URL" :required="true" prop="url">
        <el-input v-model="form.url" placeholder="请输入账号"></el-input>
      </el-form-item>
    </el-form>
    <div class="pull-right">
      <el-button type="warning" @click="onSureClick(ruleFormRef)">确 认</el-button>
      <el-button @click="dialog = false">取消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref, watch } from "vue";
import { CheckboxValueType, ElMessage, FormInstance } from "element-plus";
import {noticeSaveOrUpdate} from "@/api/setting";
import {showErrMessage} from "@/utils/element";
import { projectList, projectDetail } from "@/api/project";
import SvgIcon from "@/components/SvgIcon/index.vue";

const dialog = ref<boolean>(false)

const checkAll = ref(false)

const indeterminate = ref(false)

const queryParams = reactive({
  id: []
})

let form = reactive({
  name: '',
  trigger_events: [],
  url: '',
  msg_type: 'qiyeweixin'
})

const ruleFormRef = ref<FormInstance>()

const pk = ref(0)

const title = ref()

const projectOption = ref([])

const buttons = ref([
  {id: 1,  content: '企业微信', checked: true, svg: 'qiyeweixin'},
  {id: 2, content: '钉钉', checked: false, svg: 'dingding'},
  {id: 3, content: '飞书', checked: false, svg: 'feishu'},
  {id: 4, content: 'Webhook', checked: false, svg: 'webhook'},
]);

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入通知名称！"}],
  url: [{required: true, trigger: "blur", message: "请输入服务URL！"}],
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
    form.trigger_events = projectOption.value.map((_) => _.value)
  } else {
    form.trigger_events = []
  }
}

const onChange = (button) => {

  let buttonT = buttons.value.find(item => item.id === button.id);
  let buttonF = buttons.value.filter(item => item.id !== button.id);

  if (buttonT) {
    // 选中的设置为相反值
    buttonT["checked"] = !buttonT["checked"];
  }
  // 未当次选中设置为false, 避免出现多个按钮出现选中状态
  buttonF.forEach(item => {
    item["checked"] = false;
  });
  form.msg_type = button.svg
}

const initProjectList = () => {
  projectList().then((response) => {
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

const initTriggerEvents = () => {
  for (let i = 0; i < queryParams.id.length; i++) {

    projectDetail({id: queryParams.id[i]}).then((response) => {
      let res = response.data.data
      console.log(res['name'])
      console.log(res['id'])
      form.trigger_events.push({
        "label": res["name"],
        "value": res["id"],
        "avatar": res["avatar"]
      })
      console.log(form.trigger_events)
    }).catch((error) => {
    })
  }
}

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      let ret: any = null
      form["id"] = pk.value
      ret = await noticeSaveOrUpdate(form)
      const {code, data, msg} = ret.data
      dialog.value = false
      showErrMessage(code.toString(), msg)
      formName.resetFields()
    } else {
      console.log('error submit!')
      ElMessage.error("通知设置编辑失败请重试!")
      return false
    }
  })
}

const show = (item = {}) => {
  title.value = '新增通知事件'
  queryParams.id = []
  form.trigger_events = []
  if (item.id) {
    title.value = '编辑通知事件'
    pk.value = item.id
    Object.keys(item).forEach(key => {
      form.name = item.name
      form.msg_type = item.msg_type
      queryParams.id = eval(item.trigger_events)
      form.url = item.url
      initTriggerEvents()
    })
  }
  dialog.value = true
}

onMounted(() => {
  initProjectList()
})

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
</style>
