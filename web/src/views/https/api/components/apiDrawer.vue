<template>
  <el-drawer v-model="dialogVisible" size="85%" @close="close">
    <template #header="scope">
      <h4 class="titleClass">{{ title }}</h4>
    </template>
    <el-form
        :inline="true"
        label-position="right"
        ref="ruleFormRef"
        :model="ruleForm"
        :rules="rules"
        label-width="100px"
        style="text-align: right"
    >
      <el-form-item label="接口名称" prop="name" style="width: 350px">
        <el-input v-model="ruleForm.name" placeholder="请输入接口名称"/>
      </el-form-item>
      <el-form-item label="优先级" prop="priority" style="width: 370px">
        <el-select v-model="ruleForm.priority" filterable placeholder="请选择接口优先级">
          <el-option
              v-for="item in priority"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status" style="width: 370px">
        <el-select v-model="ruleForm.status" filterable placeholder="请选择接口当前状态">
          <template #prefix>
            <span :class="`${statusClass}`"></span>
          </template>
          <el-option
              v-for="item in status"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            <span :class="`status-${item.type}`"></span>
            <span>&nbsp;&nbsp;{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="请求类型" prop="requestType" style="width: 350px">
        <el-select v-model="ruleForm.requestType" filterable placeholder="请选择请求类型">
          <template #prefix>
            <el-icon :class="`${requestTypeClass}`"><component :is="icon" /></el-icon>
          </template>
          <el-option
              v-for="item in requestType"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            <el-icon :class="`request-type-${item.label.toLowerCase()}`"><component :is="item.icon" /></el-icon>
            <span>&nbsp;&nbsp;{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="场景标签" prop="roleIdentification" style="width: 370px">
        <el-select v-model="ruleForm.status" filterable placeholder="请选择场景标签">
          <el-option
              v-for="item in status"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="场景类型" prop="roleIdentification" style="width: 370px">
        <el-select v-model="ruleForm.status" filterable placeholder="请选择场景类型">
          <template #prefix>
            <span :class="`${statusClass}`"></span>
          </template>
          <el-option
              v-for="item in status"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane name="first">
          <template #label>
            <span>
              <el-icon class="request-type-http"><Promotion/></el-icon>
              <span>&nbsp;&nbsp;接口请求</span>
            </span>
          </template>
          <el-input style="width: 100%"
              v-model="ruleForm.name"
              placeholder="Please input"
          >
            <template #prepend>
              <el-select v-model="ruleForm.priority" placeholder="Select" style="width: 100px">
                <el-option label="ddddd" value="1" />
                <el-option label="1223123 No." value="2" />
                <el-option label="Te444444l" value="3" />
              </el-select>
            </template>
          </el-input>
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
        </el-tab-pane>
        <el-tab-pane label="Config" name="second">Config</el-tab-pane>
        <el-tab-pane label="Role" name="third">Role</el-tab-pane>
        <el-tab-pane label="Task" name="fourth">Task</el-tab-pane>
      </el-tabs>
    </el-form>
    <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleClose(ruleFormRef)">确定</el-button>
        </span>
    </template>
  </el-drawer>
</template>
<script lang="ts" setup>
import {reactive, ref, watch} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import type { TabsPaneContext } from 'element-plus'
import {menuData} from '@/mock/system'
import {Plus, Promotion} from '@element-plus/icons-vue'
import EditableProTable from "@/components/Table/EditableProTable/index.vue";

const ruleFormRef = ref<FormInstance>()
const dialogVisible = ref(false)
const title = ref('新建接口')
const ruleForm = reactive({
  name: '',
  priority: '',
  status: '',
  requestType: '',
})
const defaultProps = {
  children: 'children',
  label: 'menuName',
}

const priority = ref([{
  value: "P0",
  label: "P0"
}, {
  value: "P1",
  label: "P1"
}, {
  value: "P2",
  label: "P2"
}, {
  value: "P3",
  label: "P3"
}])

const status = ref([{
  value: 0,
  label: "调试中",
  type: "debug"
}, {
  value: 1,
  label: "已废弃",
  type: "discard"
}, {
  value: 2,
  label: "正常",
  type: "normal"
}])

const requestType = ref([{
  value: 1,
  label: "HTTP",
  icon: "Promotion"
}, {
  value: 2,
  label: "GRPC",
  icon: "Smoking"
}, {
  value: 3,
  label: "Dubbo",
  icon: "Sugar"
}])

const statusClass = ref()

const requestTypeClass = ref()

const icon = ref()

const activeName = ref('first')

const radio = ref('bottom')

const table = ref()

const column = [
  { name: 'name', label: '参数名', width: 160 },
  { name: 'value', label: '参数值', width: 160 },
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
  { name: 'description', label: '参数描述', valueType: 'input'}
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

const add = (row) => {}
const dataSource = ref(data)
const onChange = (val) => {
  dataSource.value = val
}

const deleteAction = (row) => {
  console.log('删除', row)
  ElMessage.success('点击删除')
}

const handleClick = (tab: TabsPaneContext, event: Event) => {
  console.log(tab, event)
}

function close() {
  ruleFormRef.value.resetFields()
  Object.keys(ruleForm).forEach(key => {
    if (key === 'status') ruleForm[key] = true
    else ruleForm[key] = null

  })
}

const show = (item = {}) => {
  title.value = '新建接口'
  if (item.roleName) {
    title.value = '编辑接口'
    Object.keys(item).forEach(key => {
      ruleForm[key] = item[key]
    })
  }
  dialogVisible.value = true
}

const rules = reactive({
  name: [
    {required: true, message: '请输入接口名称', trigger: 'blur'},
  ],
  roleIdentification: [{required: true, message: '请输入角色标识', trigger: 'blur'}],
})

const handleClose = async (done: () => void) => {
  await ruleFormRef.value.validate((valid, fields) => {
    if (valid) {
      dialogVisible.value = false
      console.log('submit!', obj)
    } else {
      console.log('error submit!', fields)
    }
  })
}

watch(() => ruleForm.status, (newVal, oldVal) => {
  if (newVal == "0") {
    statusClass.value = 'status-debug'
  }
  if (newVal == "1") {
    statusClass.value = 'status-discard'
  }
  if (newVal == "2") {
    statusClass.value = 'status-normal'
  }
  console.log(`"${oldVal}" to "${newVal}"`)
})


watch(() => ruleForm.requestType, (newVal, oldVal) => {
  if (newVal == "1") {
    requestTypeClass.value = 'request-type-http'
    icon.value = "Promotion"
  }
  if (newVal == "2") {
    requestTypeClass.value = 'request-type-grpc'
    icon.value = "Smoking"
  }
  if (newVal == "3") {
    requestTypeClass.value = 'request-type-dubbo'
    icon.value = "Sugar"
  }
  console.log(`"${oldVal}" to "${newVal}"`)
})

defineExpose({
  show,
})

</script>
<style lang="scss" scoped>
.titleClass {
  flex: 1;
  margin: 0;
  color: rgba(0, 0, 0, 0.88);
  font-weight: 600;
  font-size: 16px;
  line-height: 1.5;
  white-space: nowrap;
}

.el-input {
  width: 260px;
}

//.separateline{
//  border-top: solid 1px #eee;
//  border-bottom: solid 1px #eee;
//  margin-left: -20px;
//  margin-right: -40px;
//  margin-bottom: 20px;
//  margin-top: -20px;
//}

.status-debug {
  position: relative;
  background-color: #1890ff;
  top: -1px;
  display: inline-block;
  width: 6px;
  height: 6px;
  vertical-align: middle;
  border-radius: 50%;
  animation: fade 600ms infinite;
}

.status-discard {
  position: relative;
  background-color: #d92911;
  top: -1px;
  display: inline-block;
  width: 6px;
  height: 6px;
  vertical-align: middle;
  border-radius: 50%;
  animation: fade 600ms infinite;
}

.status-normal {
  position: relative;
  background-color: #83f106;
  top: -1px;
  display: inline-block;
  width: 6px;
  height: 6px;
  vertical-align: middle;
  border-radius: 50%;
  animation: fade 600ms infinite;
}

.request-type-http {
  color: #25b864
}

.request-type-dubbo {
  color: #0d8ddb
}

.request-type-grpc {
  color: #8852e0
}
</style>