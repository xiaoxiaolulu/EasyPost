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
              placeholder="请输入socket地址(ws:// 或者 wss://)"
            >
              <template #prepend>
                <el-select
                  size="default"
                  v-model="ruleForm.method"
                  disabled
                  style="width: 100px; color: #22a1c4"
                >
                  <el-option v-for="item in methodList" :value="item" :key="null" style="font-size: 12px">
                    <span>{{ item }}</span>
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
                <el-form-item label="接口名称" prop="name" :required="true">
                  <el-input v-model.trim="ruleForm.name"
                            style="width: 100%;"
                            size="small"
                            placeholder="请输入接口名称"></el-input>
                </el-form-item>
                <el-form-item label="状态" prop="status" :required="true" >
                  <el-select v-model="ruleForm.status" filterable placeholder="请选择接口当前状态" size="small" style="width: 100px;">
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
                <el-form-item label="优先级" prop="priority" :required="true" >
                  <el-select v-model="ruleForm.priority" filterable placeholder="请选择接口优先级" size="small" style="width: 100px;">
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

        <el-tabs v-model="activeName" style="overflow-y: auto">
          <el-tab-pane name='ApiRequestBody'>
            <template #label>
              <strong>发送信息</strong>
            </template>
            <div>
              <mirror-code
                style="height: 420px"
                ref="rawRef"
                v-model="state.rawData"
                :constModelData="state.rawData"
                :editorConfig="state.editorConfig"
              >
              </mirror-code>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>

      <el-card style="margin-top: 20px" v-show="responseReport" id="response">
        <template #header>
          <div style="display: flex; justify-content: space-between">
            <div>
              <strong>响应面板</strong>
            </div>
            <div style="font-size: 12px">
              <span style="padding-left: 10px">
                <span style="color:#67c23a">
                  {{connectionTxt}}
                </span>
              </span>
            </div>
          </div>
        </template>
        <div style="height: 500px; overflow-y: auto">
          <el-table :data="messageData" style="width: 100%">
            <el-table-column prop="message">
              <template #default="scope">
                <SvgIcon :icon-class="scope.row.message.type"
                         style="width: 12px; height: 12px;"/>
                <span class="content" style="">{{scope.row.message.content}}</span>
              </template>
            </el-table-column>
          </el-table>
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
import {saveOrUpdate, getHttpDetail, httpSnapshot} from "@/api/http";
import {showErrMessage} from "@/utils/element";
import MirrorCode from "@/components/MirrorCode/index.vue";
import {useSocket} from "@/store/modules/socket"
import SvgIcon from "@/components/SvgIcon/index.vue";

const { socketData, wsInit, sendSocket,} = useSocket();

const route = useRoute()

const router = useRouter()

const rawRef = ref()

const responseReport = ref(false)

const activeName =  ref('ApiRequestBody')

const methodList = ['WS']

const ruleFormRef = ref<FormInstance>()

const messageData  = ref([])

const ruleForm = reactive({
  'url': '',
  'method': 'WS',
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

const connectionStatus = ref(false)

const connectionTxt = ref()

const statusClass = ref()

const showSetting = ref(false)

const state = reactive({
  api_id: 0,
  rawData: "",
  editorConfig: { language: 'json', theme: 'vs' }
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
    document.getElementById("response").scrollIntoView({
      behavior: "smooth",
      // 定义动画过渡效果， "auto"或 "smooth" 之一。默认为 "auto"
      block: "center",
      // 定义垂直方向的对齐， "start", "center", "end", 或 "nearest"之一。默认为 "start"
      inline: "nearest"
    });
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
  url: [{required: true, trigger: "blur", message: "请输入接口地址！"}],
  priority: [{required: true, trigger: "blur", message: "请输入接口优先级！"}],
  status: [{required: true, trigger: "blur", message: "请选择接口当前状态！"}]
})

const wsSend = (url: string, data: any) => {
  try {
    wsInit(url)
    sendSocket(data)
  } catch (error) {
    console.error('Failed to send message:', error);
  }
};

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  if (!ruleForm.name || !ruleForm.url) {
    ElMessage.warning('接口名称、地址为必填项！ 🤔');
    return
  }
  formName.validate(async (valid) => {
    if (valid) {
      try{
        let apiData = {
          id: state.api_id,
          directory_id: route.query.node,
          project: route.query.project,
          name: ruleForm.name,
          url: ruleForm.url,
          method: ruleForm.method,
          priority: ruleForm.priority,
          status: ruleForm.status,
          desc: ruleForm.remarks
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
        wsSend(ruleForm.url, eval('(' + state.rawData + ')'))
        responseReport.value = true
        connectionStatus.value = true
        const connectionSvg = connectionStatus.value?"right":"mistake"
        connectionTxt.value = connectionStatus.value?"连接成功":"连接失败"
        messageData.value.push({message: {type: connectionSvg,content: connectionTxt.value}})
        messageData.value.push({message: {type: "arrowup",content: state.rawData}})
        messageData.value.push({message: {type: "arrowdown",content: socketData}})
        toResponse()
      } catch (e) {
        console.log(e)
      }
    } else {
      console.log('error submit!')
      ElMessage.error("接口调试失败请重试!")
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
      showErrMessage(code.toString(), msg)
    })
  }
}

onMounted(() => {
  initApi()
})

defineExpose({
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


watch(
  () => socketData,
  (data) => {
    console.log("ws: ", data);
  },
  {
    immediate: true,
  }
);
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
