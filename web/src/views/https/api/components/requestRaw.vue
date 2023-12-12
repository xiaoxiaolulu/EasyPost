<template>
  <el-form :inline="true" label-width="50px" size="small" label-position="right" ref="requestFormRef">
    <div style="border-bottom: 1px solid #E6E6E6; display: flex; justify-content: space-between">
      <div class="request-mode">
        <el-radio-group
            size="small"
            v-model="mode"
            @change="radioChange"
        >
          <el-radio label="none">none</el-radio>
          <el-radio label="form_data">form-data</el-radio>
          <el-radio label="x_www_form_urlencoded">x-www-form-urlencoded</el-radio>
          <el-radio label="raw">raw</el-radio>
          <el-dropdown @command="handleLanguage"
                       trigger="click"
                       v-if="mode === 'raw'"
                       placement="bottom-start">
              <span class="el-button--text">
                {{ state.language }}
                <el-icon class="el-icon--right">
                  <arrowDown/>
                </el-icon>
              </span>
            <template #dropdown>
              <el-dropdown-menu style="width: 150px">
                <el-dropdown-item v-for="language in state.languageList" :key="language" :command="language">
                  {{ language }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-radio-group>
      </div>
    </div>

    <!--没有请求体-->
    <div v-if="mode === 'none'" style="text-align: center; padding-top: 10px">
      <span style="color: darkgray">该请求暂时没有正文</span>
    </div>

    <!--form-data-->
    <div v-if="mode === 'form_data'" style="text-align: center; padding-top: 10px">
      <request-data ref="RequestFromDataRef"></request-data>
    </div>

    <!--x_www_form_urlencoded-->
    <div v-if="mode === 'x_www_form_urlencoded'" style="text-align: center; padding-top: 10px">
      <request-data ref="RequestFormUrlencodedRef"></request-data>
    </div>

    <!--raw-->
    <div v-show="mode === 'json'">
      <mirror-code
          style="height: 420px"
          ref="rawRef"
          v-model="state.rawData"
          :constModelData="state.rawData"
          :editorConfig="state.editorConfig"
      >
      </mirror-code>
    </div>
  </el-form>
</template>

<script setup lang="ts">
import {reactive, ref, watch} from "vue";
import {ArrowDown} from '@element-plus/icons-vue'
import RequestData from "@/views/https/api/components/requestData.vue";
import MirrorCode from "@/components/MirrorCode/index.vue";

const emit = defineEmits(['updateContentType'])

const mode = ref('none')

const state = reactive({
  // formData
  formData: [],
  // x_www_form_urlencoded
  x_www_form_urlencoded: [],
  // raw
  rawData: "",
  language: 'json',
  languageList: ['json', 'text', 'xml', 'html'],
  //monaco
  lang: 'json',
  editorConfig: { language: 'json', theme: 'vs' }
});

const RequestFromDataRef = ref()

const RequestFormUrlencodedRef = ref()

const rawRef = ref()

const setData = (data) => {
  data = JSON.parse(data)
  mode.value = Object.keys(data)[0]
  if (!data) return
  switch (mode.value) {
    case 'form_data':
      state.formData = data.data ? data.data : []
      break
    case 'x_www_form_urlencoded':
      state.x_www_form_urlencoded = data.data ? data.data : []
    case 'json':
      state.rawData = data["json"]
      state.language = mode.value
    default:
      break
  }
}

const radioChange = (value: any) => {
  mode.value = value
  updateContentType(value === 'none' || value === 'form_data')
}

const getData = () => {
  let requestData = {
  }
  if (mode.value  === 'json') {
    requestData['json'] = state.rawData
  }
  if (mode.value === 'form_data') {
    requestData['data'] = RequestFromDataRef.value.getData()
  }
  if (mode.value === 'x_www_form_urlencoded') {
    requestData['data'] = RequestFormUrlencodedRef.value.getData()
  }
  if (mode.value === 'none') {
    requestData['data'] = null
  }
  return requestData
}

const handleLanguage = (language: any) => {
  state.language = language
  updateContentType()
}


const updateContentType = (remove = false) => {
  emit('updateContentType', mode.value, state.language, remove)
}

watch(() => state.rawData, (val) => {
      if (val) {
        updateContentType()
      } else {
        updateContentType(true)
      }
    }, {
      deep: true
    }
);

defineExpose({
  setData,
  getData
})
</script>


<style scoped lang="scss">
.request-mode {
  margin-bottom: 10px;

  :deep(.el-radio__label) {
    font-size: 13px;
  }
}
</style>