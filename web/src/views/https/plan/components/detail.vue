<template>
  <div class="app-container">
    <div class="header-container">
      <div class="card-head-title">
        <div class="card-description">
          <span class="el-icon-back" @click="goBack">
            <el-icon>
              <component :is="Back"/>
            </el-icon>
          </span>
          <span class="page-header-heading-title">
            {{ route.query.editType === 'update' ? "更新" : "新增" }}
          </span>
        </div>
      </div>
    </div>
    <div class="container">
      <el-row :gutter="12">
        <el-col :span="6">
          <el-card style="height:100%;min-height: 600px;overflow:scroll;">
            <template #header>
              <div>
                <span style="margin-right:8px;color: #7a8b9a"><el-icon><component :is="Odometer"/></el-icon></span>
                <span style="font-size: 18px; color: #7a8b9a">计划配置</span>
              </div>
            </template>
            <div>
              <el-form autoComplete="on" :model="state.form" :rules="rules" ref="ruleFormRef"
                       label-width="auto"
                       label-position="top"
                       size="small"
              >
                <el-form-item label="用例名称：" prop="name" :required="true">
                  <el-input v-model.trim="state.form.name"
                            style="width: 100%;"
                            size="small"
                            placeholder="请输入用例名称"></el-input>
                </el-form-item>
                <el-form-item label="所属项目" :required="true" prop="project">
                  <el-select
                      class="selectOpt" v-model="state.form.project" placeholder="请选择"
                      :popper-append-to-body="false"
                      style="width: 150px;"
                  >
                    <el-option
                        v-for="item in projectOption"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="优先级：" prop="priority" :required="true">
                  <el-select v-model="state.form.priority" filterable placeholder="请选择接口优先级" size="small">
                    <el-option
                        v-for="item in priority"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="cron表达式：" prop="">
                  <el-input v-model.trim="state.form.cron"
                            style="width: 100%;"
                            size="small">
                    <template #append>
                      <el-popover v-model:visible="state.cronPopover" width="700px" trigger="manual">
                        <no-cron
                            :cron-value="state.form.cron"
                            @change="changeCron"
                            @close="state.cronPopover=false"
                            max-height="400px"
                            i18n="cn"
                        ></no-cron>
                        <template #reference>
                          <el-button @click="state.cronPopover = !state.cronPopover">设置</el-button>
                        </template>
                      </el-popover>
                    </template>
                  </el-input>
                </el-form-item>
              </el-form>
              <el-button type="primary" @click="onSureClick(ruleFormRef)" size="small">保存</el-button>
            </div>
          </el-card>
        </el-col>
        <el-col :span="18">
          <el-card style="height:100%;min-height: 600px;overflow:scroll;">
            <template #header>
              <div>
                <span style="font-size: 18px; color: #7a8b9a">用例配置</span>
              </div>
            </template>
            <div>
              <div style="margin-top: 15px">
                <el-table
                    :data="tableData"
                    :header-cell-style="{ background: '#F2F3F8', color: '#1D2129' }"
                    style="width: 100%"
                    ref="dragTable"
                    row-key="id"
                    :show-header="false"
                >
                  <el-table-column width="30">
                    <template #default>
                      <span
                          :class="getStepTypeInfo('api','icon')" class="fab-icons move"
                          :style="{color:getStepTypeInfo('api','color')}"
                      ></span>
                    </template>
                  </el-table-column>
                  <el-table-column>
                    <template #default="scope">
                      <div>
                        <span class="opblock-summary-description">
                            {{ scope.row.name }}
                        </span>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>
                <el-dropdown :hide-on-click="false" style="width: 100%">
                  <el-button size="small" style="width: 100%">
                    <el-icon style="margin-right: 4px">
                      <plus/>
                    </el-icon>
                    添加用例
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item v-for="(value, key)  in state.optTypes"
                                        :key="key"
                                        style="margin: 5px 0"
                                        :style="{ color: getStepTypeInfo(key,'color')}"
                                        @click="handleAddData(key)">

                        <i :class="getStepTypeInfo(key,'icon')" class="fab-icons"
                           :style="{color:getStepTypeInfo(key,'color')}"></i>
                        {{ value }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
            <step
                ref="stepControllerRef"
                use_type="case"
                style="margin-bottom: 10px"
                v-model="state.form.case_data"
                @change="changeAction"
            >
            </step>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import {Back, Odometer} from "@element-plus/icons-vue";
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, reactive, ref, watch, nextTick} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {savePlanOrUpdate, getCaseDetail} from "@/api/http";
import {projectList} from "@/api/project";
import {showErrMessage} from "@/utils/element";
import {getStepTypesByUse, getStepTypeInfo, parseTime} from '@/utils/index'
import Step from "@/views/https/plan/components/step.vue";
import Sortable from "sortablejs"
import noCron from "@/components/no-cron/index.vue";

const route = useRoute()
const router = useRouter()

const ruleFormRef = ref<FormInstance>()

const tableData = reactive([
])

const loading = ref(false)

const createForm = () => {
  return {
    name: '',
    cron: '',
    priority: '',
    case_list: [],
    remarks: '',
    project: ''
  }
}

const priority = ref([{
  value: 0,
  label: "P0"
}, {
  value: 1,
  label: "P1"
}, {
  value: 2,
  label: "P2"
}, {
  value: 3,
  label: "P3"
}, {
  value: 4,
  label: "P4"
}])

const stepControllerRef = ref()

const selectCaseData = ref()

const projectOption = ref([])


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

const state = reactive({
  optTypes: getStepTypesByUse("case"),
  form: createForm(),
  case_id: 0,
  cronPopover: false
})

const changeCron = (val) => {
  if(typeof(val) !== 'string') return false
  state.form.cron = val
}

const handleAddData = (optType) => {
  stepControllerRef.value.handleAddData(optType)
}

const goBack = () => {
  router.push({
    name: "apis",
  })
}

const rules = reactive({})

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      try {
        let caseData = {
          id: state.case_id,
          name: state.form.name,
          cron: state.form.cron,
          priority: state.form.priority,
          case_list: state.form.case_list,
          project: state.form.project,
          pass_rate: "100%",
          msg_type: 1,
          receiver: ''
        }
        const ret = await savePlanOrUpdate(caseData)
        const {code, data, msg} = ret.data
        state.case_id = data.case_id
        showErrMessage(code.toString(), msg)
      } catch (e) {
        console.log(e)
      }

    } else {
      console.log('error submit!')
      ElMessage.error("新增接口失败请重试!")
      return false
    }
  })
}


const initApi = () => {
  let case_id = route.query.id
  if(case_id){
    state.case_id = case_id
  }
  console.log("api_id------>", case_id)
  if (case_id) {
    getCaseDetail({id: case_id}).then((response) => {
      const {data, code, msg} = response.data
      state.form.name = data.name
      state.form.remarks = data.desc
      state.form.priority = data.priority
      setStepData(eval(data.step))
      showErrMessage(code.toString(), msg)
    })
  }
}

const dragTable = ref()
const initDropTable = () => {
  const el = dragTable.value.$el.querySelector('.el-table__body tbody')
  Sortable.create(el, {
    animation: 150, //动画
    disabled: false,
    handle: '.move', //指定列拖拽
    filter: '.disabled',
    // 设置拖拽样式类名
    dragClass: 'drop-dragClass',
    // 设置拖拽停靠样式类名
    ghostClass: 'drop-ghostClass',
    // 设置选中样式类名
    chosenClass: 'drop-chosenClass',

    onStart: () => {
      console.log('开始拖动')
    },

    onEnd(evt: any) {
      const { newIndex, oldIndex } = evt
      console.log(newIndex)
      console.log(oldIndex)
      const currRow = tableData.splice(oldIndex, 1)[0]
      tableData.splice(newIndex, 0, currRow)
    }
  })
}

const changeAction = (data) => {
  selectCaseData.value = data
  setStepData(eval(data))
}

const setStepData = (data) => {
  for (let i = 0; i < data.length; i++) {
    tableData.push(data[i])
    state.form.case_list.push(data[i]['id'])
  }
}

onMounted(() => {
  initApi()
  nextTick(() => {
    initDropTable()
  })
})

defineExpose({
})

</script>
<style lang="scss">

.move {
  cursor: pointer;
}

.page-header-back-button {
  text-decoration: none;
  outline: none;
  transition: color .3s;
  color: #000;
  cursor: pointer;
  margin-right: 16px;
  font-size: 15px;
  line-height: 1;
}

.page-header-heading-title {
  margin-right: 12px;
  margin-bottom: 0;
  color: rgba(0, 0, 0, .85);
  font-weight: 600;
  font-size: 14px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis
}


.method-color-get {
  color: #61affe
}

.method-color-post {
  color: #49cc90
}

.method-color-delete {
  color: #f93e3d
}

.method-color-put {
  color: #fca130
}

.method-color-na {
  color: #f56c6c
}

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

.api-body {
  margin-top: 20px;
}

.custom-table .cell {
  font-size: 12px;
  color: #7a8b9a;
}

.opblock-summary-description {
  color: #3b4151;
  font-family: sans-serif;
  font-size: 13px;
  word-break: break-word;
}

.drop-dragClass {
  background: #e4e4ee !important;
  opacity: 0.5 !important;
}

// 停靠
.drop-ghostClass {
  background: #C0C0C0 !important;
  opacity: 0.5 !important;
}

// 选择
.drop-chosenClass:hover > td {
  background: #e4e4ee !important;
  opacity: 0.5 !important;
}
</style>
