<template>
  <div class="app-container">
    <div class="header-container">
      <div class="card-head-title">
        <div class="card-description">
                    <span class="page-header-back-button el-icon-back" @click="goBack">
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
      <el-card>
        <template #header>
          <div>
            <strong>基本信息</strong>
          </div>
        </template>
        <el-row>
          <el-col :xs="15" :sm="15" :md="15" :lg="15" :xl="15">
            <el-input
                size="default"
                v-model="ruleForm.url"
                placeholder="请输入请求路径"
            >
              <template #prepend>
                <el-select
                    size="default"
                    v-model="ruleForm.method"
                    ref="methodRef"
                    @change="methodChange"
                    placeholder=""
                    style="width: 100px; color: #22a1c4"
                >
                  <el-option v-for="item in methodList" :value="item" :key="null" style="font-size: 12px">
                    <span :class="[`method-color-${item.toLowerCase()}`]">{{ item }}</span>
                  </el-option>
                </el-select>
              </template>
            </el-input>
          </el-col>
          <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6">
            <div style="padding-left: 12px">
              <el-button type="primary" @click="onSureClick(ruleFormRef)">保存</el-button>
              <el-button type="success" @click="debug(ruleFormRef)">调试</el-button>
            </div>
          </el-col>
        </el-row>
        <div class="api-body">
          <el-row>
            <el-form :inline="true" autoComplete="on" :model="ruleForm" :rules="rules" ref="ruleFormRef"
                     label-width="auto"
                     label-position="right">
              <el-col>
                <el-form-item label="接口名称" prop="name">
                  <el-input v-model.trim="ruleForm.name"
                            style="width: 100%;"
                            size="small"
                            placeholder="请输入接口名称"></el-input>
                </el-form-item>
                <el-form-item label="状态" prop="status">
                  <el-select v-model="ruleForm.status" filterable placeholder="请选择接口当前状态" size="small">
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
                <el-form-item label="优先级" prop="priority">
                  <el-select v-model="ruleForm.priority" filterable placeholder="请选择接口当前状态" size="small">
                    <el-option
                        v-for="item in priority"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col style="margin-bottom: 20px">
                <el-button  size="default" type="primary" link style="margin-left:10px" id="closeSearchBtn" @click="closeSetting">
                  {{ settings }}
                  <el-icon v-if="showSetting">
                    <ArrowUp/>
                  </el-icon>
                  <el-icon v-else>
                    <ArrowDown/>
                  </el-icon>
                </el-button>
              </el-col>
              <el-col>
                <el-form-item label="描述" prop="" v-show="showSetting">
                  <el-input size="default"
                            type="textarea"
                            v-model.trim="ruleForm.remarks"
                            style="width: 500px;"
                            placeholder="请输入用例描述"></el-input>
                </el-form-item>
              </el-col>
            </el-form>
          </el-row>
        </div>
      </el-card>

      <el-card style="margin-top: 20px">
        <template #header>
          <div>
            <strong>请求信息</strong>
          </div>
        </template>
        <div>
          <el-tabs v-model="activeName" style="overflow-y: auto">

            <!--请求头-->
            <el-tab-pane name='ApiRequestHeader'>
              <template #label>
                <strong>Header</strong>
              </template>
              <div>
                <request-headers ref="RequestHeadersRef"></request-headers>
              </div>
            </el-tab-pane>

            <!--地址参数-->
            <el-tab-pane name='ApiRequestQuery'>
              <template #label>
                <strong>Query</strong>
              </template>
              <div>
                <request-query ref="RequestQueryRef" @updateRouter="updateRouter"></request-query>
              </div>
            </el-tab-pane>

            <el-tab-pane name='ApiRequestBody'>
              <template #label>
                <strong>Body</strong>
              </template>
              <div>
                <request-raw ref="RequestBodyRef" @updateContentType="updateContentType"></request-raw>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestSetup'>
              <template #label>
                <strong>前置脚本</strong>
              </template>
              <div>
                <api-script ref="RequestSetup" use-type="setup"></api-script>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestTeardown'>
              <template #label>
                <strong>后置脚本</strong>
              </template>
              <div>
                <api-script ref="RequestTeardown" use-type="teardown"></api-script>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestController'>
              <template #label>
                <strong>控制器</strong>
              </template>
              <div>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestValidators'>
              <template #label>
                <strong>断言</strong>
              </template>
              <div>
                <validator ref="RequestValidators"></validator>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestExtractor'>
              <template #label>
                <strong>变量提取</strong>
              </template>
              <div>
                <extract ref="RequestExtractor"></extract>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestPerform'>
              <template #label>
                <strong>一键压测</strong>
              </template>
              <div>
                <el-form :inline="true" autoComplete="on" :model="ruleForm" :rules="rules" ref="ruleFormRef"
                         label-width="auto"
                         label-position="right">
                  <el-form-item label="并发数" prop="">
                    <el-input
                        size="small"
                        v-model="ruleForm.threads"
                        placeholder=""
                    ></el-input>
                  </el-form-item>
                  <el-form-item label="轮次" prop="">
                    <el-input
                        size="small"
                        v-model="ruleForm.iter"
                        placeholder=""
                    ></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button size="small" type="primary" @click="debug(ruleFormRef)">开始压测</el-button>
                  </el-form-item>
                </el-form>
                <el-table v-loading="performLoading" :data="performData" class="custom-table" v-show="performResponseShow">
                  <el-table-column prop="duration" label="duration"></el-table-column>
                  <el-table-column prop="mean" label="mean"></el-table-column>
                  <el-table-column prop="min" label="min"></el-table-column>
                  <el-table-column prop="median" label="median"></el-table-column>
                  <el-table-column prop="90p" label="90p"></el-table-column>
                  <el-table-column prop="95p" label="95p"></el-table-column>
                  <el-table-column prop="99p" label="99p"></el-table-column>
                  <el-table-column prop="max" label="max"></el-table-column>
                </el-table>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>

      <el-card style="margin-top: 20px" v-show="responseReport">
        <template #header>
          <div style="display: flex; justify-content: space-between">
            <div>
              <strong>响应面板</strong>
            </div>
            <div style="font-size: 12px">
              <span style="padding-left: 10px">
                <span style="color:#67c23a">
                  {{statusCode}}
                </span>
              </span>
              <span style="padding-left: 10px">
                Time: <span style="color:#67c23a;">{{runTime}}</span>
              </span>
            </div>
          </div>
        </template>
        <div style="height: 500px; overflow-y: auto">
          <response-report ref="ResponseRef"></response-report>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ArrowDown, ArrowUp, Back} from "@element-plus/icons-vue";
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, reactive, ref, watch, nextTick} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import RequestRaw from "@/views/https/api/components/requestRaw.vue";
import RequestQuery from "@/views/https/api/components/requestQuery.vue";
import RequestHeaders from "@/views/https/api/components/requestHeaders.vue";
import Extract from "@/views/https/api/components/extract.vue";
import Validator from "@/views/https/api/components/validator.vue";
import ApiScript from "@/views/https/api/components/apiScript.vue";
import {saveOrUpdate, runApi, getHttpDetail} from "@/api/http";
import {showErrMessage} from "@/utils/element";
import ResponseReport from "@/views/https/api/components/responseReport.vue";

const route = useRoute()
const router = useRouter()

const methodRef = ref()

const responseReport = ref(false)

const methodList = ['POST', "GET", "PUT", "DELETE"]

const ruleFormRef = ref<FormInstance>()

const ruleForm = reactive({
  'url': '',
  'method': 'POST',
  'name': '',
  'status': '',
  'remarks': '',
  'threads': '',
  'iter': '',
  'priority': '',
})

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

const performData = ref()

const statusCode = ref()

const statusClass = ref()

const runTime = ref()

const showSetting = ref(false)

const activeName =  ref('ApiRequestBody')

const ResponseRef = ref()

const RequestHeadersRef = ref()

const RequestQueryRef = ref()

const RequestBodyRef = ref()

const RequestExtractor = ref()

const RequestValidators = ref()

const RequestTeardown = ref()

const RequestSetup = ref()

const performResponseShow = ref(false)

const performLoading = ref(false)

const state = reactive({
  api_id: 0
})

const settings = computed(() => {
  if (showSetting.value == false) {
    return "更多设置";
  } else {
    return "收起设置";
  }
})

const toResponse = () => {
  nextTick(() => {
    ResponseRef.value.$el.scrollIntoView({
      behavior: "smooth",
      // 定义动画过渡效果， "auto"或 "smooth" 之一。默认为 "auto"
      block: "center",
      // 定义垂直方向的对齐， "start", "center", "end", 或 "nearest"之一。默认为 "start"
      inline: "nearest"
    })
  })
}

const closeSetting = () => {
  showSetting.value = !showSetting.value
}

const goBack = () => {
  router.push({
    name: "apis",
  })
}

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入接口名称！"}],
})

const getMethodColor = (method: any) => {
  let color = ""
  if (method === "GET") {
    color = "#61affe"
  } else if (method === "POST") {
    color = "#49cc90"
  } else if (method === "DELETE") {
    color = "#f93e3d"
  } else if (method === "PUT") {
    color = "#fca130"
  } else if (method === "N/A") {
    color = "#f56c6c"
  }
  return color
}

const methodChange = (method: any) => {
  let selectInputEl = methodRef.value.$el.getElementsByTagName("input")
  if (selectInputEl.length > 0) selectInputEl[0].style.color = getMethodColor(method)
}

const setData = (form: any) => {
  methodChange(form.method)
}

const updateRouter = (newValue: any) => {
  initializeUrl()
  ruleForm.url += newValue
}

const initializeUrl = () => {
  // 初始化逻辑
  // if(ruleForm.url.includes('?')){
  //   ruleForm.url = ruleForm.url.split('?')[0]
  // }
  // console.log('Initialized:', ruleForm.url);
};

const updateContentType = (mode: any, language: any, remove: any) => {
  RequestHeadersRef.value.getData()
  RequestHeadersRef.value.updateContentType(mode, language, remove)
}

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      try{

        let ApiRequestHeader = RequestHeadersRef.value.getData()
        let ApiRequestQuery = RequestQueryRef.value.getData()
        let ApiRequestBody = RequestBodyRef.value.getData()
        let ApiRequestSetup = RequestSetup.value.getData()
        let ApiRequestTeardown = RequestTeardown.value.getData()
        let ApiRequestValidators = RequestValidators.value.getData()
        let ApiRequestExtractor = RequestExtractor.value.getData()
        let apiData = {
          id: state.api_id,
          directory_id: route.query.node,
          project: route.query.project,
          name: ruleForm.name,
          url: ruleForm.url,
          method: ruleForm.method,
          priority: ruleForm.priority,
          status: ruleForm.status,
          desc: ruleForm.remarks,
          headers: ApiRequestHeader,
          raw: ApiRequestBody,
          params: ApiRequestQuery,
          setup_script: ApiRequestSetup,
          teardown_script: ApiRequestTeardown,
          validate: ApiRequestValidators,
          extract: ApiRequestExtractor
        }
        const ret = await saveOrUpdate(apiData)
        const {code, data, msg} = ret.data
        state.api_id = data.api_id
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

const debug = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      try{
        let mode = 'normal'
        if (ruleForm.iter && ruleForm.threads){
          mode = 'perform'
        }else {
          mode = 'normal'
        }
        performLoading.value = true
        performResponseShow.value = false
        let ApiRequestHeader = RequestHeadersRef.value.getData()
        let ApiRequestQuery = RequestQueryRef.value.getData()
        let ApiRequestBody = RequestBodyRef.value.getData()
        let ApiRequestSetup = RequestSetup.value.getData()
        let ApiRequestTeardown = RequestTeardown.value.getData()
        let ApiRequestValidators = RequestValidators.value.getData()
        let ApiRequestExtractor = RequestExtractor.value.getData()
        let apiData = {
          mode: mode,
          threads: ruleForm.threads,
          iterations: ruleForm.iter,
          directory_id: route.query.node,
          project: route.query.project,
          name: ruleForm.name,
          url: ruleForm.url,
          method: ruleForm.method,
          tags: '',
          status: ruleForm.status,
          desc: ruleForm.remarks,
          headers: ApiRequestHeader,
          raw: ApiRequestBody,
          params: ApiRequestQuery,
          setup_script: ApiRequestSetup,
          teardown_script: ApiRequestTeardown,
          validate: ApiRequestValidators,
          extract: ApiRequestExtractor
        }
        const ret = await runApi(apiData)
        const {code, data, msg} = ret.data
        const res = data['class_list'][0]['cases'][0]
        statusCode.value = res['status_code']
        runTime.value = res['run_time']
        ResponseRef.value.setData(res)
        performData.value = [res['perform']]
        performResponseShow.value = true
        performLoading.value = false
        responseReport.value = true
        toResponse()
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
  let api_id = route.query.id
  if(api_id){
    state.api_id = api_id
  }
  console.log("api_id------>", api_id)
  if (api_id) {
    getHttpDetail({id: api_id}).then((response) => {
      const {data, code, msg} = response.data
      ruleForm.url = data.url
      ruleForm.method = data.method
      ruleForm.name = data.name
      ruleForm.status = data.status
      ruleForm.remarks = data.desc
      RequestHeadersRef.value.setData(eval(data.headers))
      RequestQueryRef.value.setData(eval(data.params))
      RequestBodyRef.value.setData(JSON.parse(data.raw))
      RequestExtractor.value.setData(eval(data.extract))
      RequestValidators.value.setData(eval(data.validate))
      RequestTeardown.value.setData(data.setup_script)
      RequestSetup.value.setData(data.teardown_script)
      showErrMessage(code.toString(), msg)
    })
  }
}

onMounted(() => {
  setData(ruleForm)
  initApi()
})

defineExpose({
  setData
})

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
</script>
<style lang="scss">
.page-header-back-button {
  text-decoration: none;
  outline: none;
  transition: color .3s;
  color: #000;
  cursor: pointer;
  margin-right: 16px;
  font-size: 16px;
  line-height: 1;
}

.page-header-heading-title {
  margin-right: 12px;
  margin-bottom: 0;
  color: rgba(0, 0, 0, .85);
  font-weight: 600;
  font-size: 19px;
  line-height: 32px;
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

.custom-table .cell{
  font-size: 12px;
  color: #7a8b9a;
}
</style>
