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
              <el-button>调试</el-button>
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
                <el-form-item label="接口标签" prop="tag">
                  <!--                  <el-tag-->
                  <!--                      v-for="tag in state.form.tags"-->
                  <!--                      :key="tag"-->
                  <!--                      size="default"-->
                  <!--                      type="success"-->
                  <!--                      closable-->
                  <!--                      style="{margin-left: 0.25rem;margin-right: 0.25rem;}"-->
                  <!--                      :disable-transitions="false"-->
                  <!--                      @close="removeTag(tag)"-->
                  <!--                  >{{ tag }}-->
                  <!--                  </el-tag>-->

                  <!--                  <el-input-->
                  <!--                      v-if="state.editTag"-->
                  <!--                      ref="caseTagInputRef"-->
                  <!--                      v-model="state.tagValue"-->
                  <!--                      class="ml-1 w-20"-->
                  <!--                      size="small"-->
                  <!--                      @keyup.enter="addTag"-->
                  <!--                      @blur="addTag"-->
                  <!--                      style="width: 100px"-->
                  <!--                  />-->
                  <el-button size="small">
                    + New Tag
                  </el-button>
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
                <request-body></request-body>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestExtractor'>
              <template #label>
                <strong>Extractor</strong>
              </template>
              <div>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestSetup'>
              <template #label>
                <strong>SetupScript</strong>
              </template>
              <div>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestTeardown'>
              <template #label>
                <strong>TeardownScript</strong>
              </template>
              <div>
              </div>
            </el-tab-pane>
            <el-tab-pane name='ApiRequestValidators'>
              <template #label>
                <strong>Validator</strong>
              </template>
              <div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ArrowDown, ArrowUp, Back} from "@element-plus/icons-vue";
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, reactive, ref, watch} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import RequestBody from "@/views/https/api/components/requestBody.vue";
import RequestHeaders from "@/views/https/api/components/requestHeaders.vue";
import RequestQuery from "@/views/https/api/components/requestQuery.vue";

const route = useRoute()
const router = useRouter()

const methodRef = ref()

const methodList = ['POST', "GET", "PUT", "DELETE"]

const ruleFormRef = ref<FormInstance>()

const ruleForm = reactive({
  'url': '',
  'method': 'POST',
  'name': '',
  'status': '',
  'remarks': ''
})

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

const statusClass = ref()

const showSetting = ref(false)

const activeName =  ref('ApiRequestBody')

const RequestHeadersRef = ref()

const RequestQueryRef = ref()

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
  initialize()
  ruleForm.url += newValue
}

const initialize = () => {
  // 初始化逻辑
  if(ruleForm.url.includes('?')){
    ruleForm.url = ruleForm.url.split('?')[0]
  }
  console.log('Initialized:', ruleForm.url);
};

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      try{
        console.log("表单测试")
        // console.log(ruleForm)
        //console.log(RequestHeadersRef.value.getData())
        console.log(RequestQueryRef.value.getData())
        // console.log("表单测试")
        // const ret = await projectCreate(form)
        // const {code, data, msg} = ret.data
        // showErrMessage(code.toString(), msg)
        // formName.resetFields()
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

onMounted(() => {
  setData(ruleForm)
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
</style>
