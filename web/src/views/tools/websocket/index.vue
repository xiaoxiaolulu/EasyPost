<template>
  <div class="app-container">
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
              <el-button :type="connectionstatus" @click="connection(ruleFormRef)">{{connectionCon}}</el-button>
              <el-button type="warning" @click="debug(ruleFormRef)">调试</el-button>
            </div>
          </el-col>
        </el-row>
<!--        <div class="api-body">-->
<!--          <el-row>-->
<!--            <el-form :inline="true" autoComplete="on" :model="ruleForm" :rules="rules" ref="ruleFormRef"-->
<!--                     label-width="auto"-->
<!--                     label-position="right">-->
<!--              <el-col style="margin-bottom: 20px">-->
<!--                <el-button  size="default" type="primary" link style="margin-left:10px" id="closeSearchBtn" @click="closeSetting">-->
<!--                  {{ settings }}-->
<!--                  <el-icon v-if="showSetting">-->
<!--                    <ArrowUp/>-->
<!--                  </el-icon>-->
<!--                  <el-icon v-else>-->
<!--                    <ArrowDown/>-->
<!--                  </el-icon>-->
<!--                </el-button>-->
<!--              </el-col>-->
<!--              <el-col>-->
<!--                <el-form-item label="描述" prop="" v-show="showSetting">-->
<!--                  <el-input size="default"-->
<!--                            v-model.trim="ruleForm.loop"-->
<!--                            style="width: 500px;"-->
<!--                            placeholder="请输入用例描述"></el-input>-->
<!--                </el-form-item>-->
<!--              </el-col>-->
<!--            </el-form>-->
<!--          </el-row>-->
<!--        </div>-->
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

      <el-drawer
        v-model="state.showDetailInfo"
        size="70%"
        append-to-body
        direction="ltr"
        destroy-on-close
        :with-header="true">
        <template #header>
          <span>
            <strong class="pr10">消息</strong>
          </span>
        </template>
        <div style="height: 500px; overflow-y: auto">
          <response-detail :reportData="ResponseData"></response-detail>
        </div>
      </el-drawer>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ArrowDown, ArrowUp} from "@element-plus/icons-vue";
import {computed, onMounted, reactive, ref, watch} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import MirrorCode from "@/components/MirrorCode/index.vue";
import {useSocket} from "@/store/modules/socket"
import ResponseDetail from "@/views/tools/websocket/components/responseDetail.vue";

const {socketData, wsInit, sendSocket, destroySocket} = useSocket();

const rawRef = ref()

const activeName =  ref('ApiRequestBody')

const methodList = ['WS']

const ruleFormRef = ref<FormInstance>()

const messageData  = ref([])

const connectionstatus = ref("success")

const connectionCon = ref("连接")

const ResponseData = ref()

const ruleForm = reactive({
  'url': '',
  'method': 'WS'
})

const showSetting = ref(false)

const state = reactive({
  api_id: 0,
  rawData: "",
  status: false,
  editorConfig: { language: 'json', theme: 'vs' },
  showDetailInfo: false
})

const settings = computed(() => {
  if (showSetting.value == false) {
    return "更多设置";
  } else {
    return "收起设置";
  }
})

const closeSetting = () => {
  showSetting.value = !showSetting.value
}

const rules = reactive({
  url: [{required: true, trigger: "blur", message: "请输入接口地址！"}]
})

const wsSend = (data: any) => {
  try {
    sendSocket(data)
  } catch (error) {
    console.error('Failed to send message:', error);
  }
};

const reconnect = (url: string, status: boolean) => {
  try{
    console.log(status)
    if (status){
      destroySocket()
    } else {
      wsInit(url)
    }
    state.status = !state.status
    const connectionSvg = state.status?"right":"mistake"
    const connectionTxt = state.status?"连接成功":"断开连接"
    connectionstatus.value = state.status?"danger":"success"
    connectionCon.value = state.status?"断开连接":"连接"
    messageData.value.push({message: {type: connectionSvg,content: connectionTxt}})
    ResponseData.value = {messageData: messageData.value}
  }catch (error) {
    console.error(error);
  }
}

const connection = () => {
  if (!ruleForm.url){
    ElMessage.warning('接口地址为必填项！ 🤔');
    return
  }
  try{
    reconnect(ruleForm.url, state.status)
  } catch (e) {
    console.log(e)
  }
}

const receive = () => {
  console.log(socketData)
  if (socketData){
    messageData.value.push({message: {type: "arrowup",content: state.rawData}})
    messageData.value.push({message: {type: "arrowdown",content: socketData}})
    ResponseData.value = {messageData: messageData.value}
  }
}

const toResponse = () => {
  setTimeout(
    function(){
      state.showDetailInfo = true
    }, 5000
  )
}

const debug = () => {
  if (!ruleForm.url || !state.rawData){
    ElMessage.warning('接口地址、参数为必填项！ 🤔');
    return
  }
  try{
    console.log(state.status)
    if (state.status == true) {
      wsSend(eval('(' + state.rawData + ')'))
      receive()
      toResponse()
    }
  } catch (e) {
    console.log(e)
  }
}

onMounted(() => {
})

defineExpose({
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

.custom-table .cell{
  font-size: 12px;
  color: #7a8b9a;
}

.api-body {
  margin-top: 20px;
}
</style>
