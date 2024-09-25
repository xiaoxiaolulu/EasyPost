<script setup lang="ts">
import { computed, ref } from "vue";
  import {reactive} from 'vue';
  import MirrorCode from "@/components/MirrorCode/index.vue";

  const activeName =  ref('ApiResponseBody')

  const state = reactive({
    runLog: "",
    status_code: "",
    content_length: "",
    content_type: "",
    response_time: "",
    content_type: "",
    responseBody: "",
    validateExtractor: [],
    dataExtractor: [],
    headers: "",
    errMessage: "",
    editorConfig: { language: 'python', theme: 'vs' },
  })

  // init
  const setData = (data) => {
    if (data){
      state.runLog = data['logData'].join('')
      state.status_code = data['statusCode']
      state.content_length = data['contentLength']
      state.content_type = data['contentType']
      state.response_time = data['runTime']
      state.responseBody = data['responseBody']
      state.headers = JSON.parse(data['requestsHeader'])
      state.validateExtractor = data['validateExtractor']
      state.dataExtractor = data['dataExtractor']
      state.errMessage = data['errorMsg']
    }
  }

  const getValidatorsResultStatus = computed(() => {
    if (!state.validateExtractor) {
      return null
    }
    if (state.validateExtractor.length === 0) {
      return null
    }
    let failList = state.validateExtractor.filter((e) => {
      return e.state !== '1'
    })
    return failList.length === 0
  })


const getDataExtractorResultStatus = computed(() => {
  if (!state.dataExtractor) {
    return null
  }
  if (state.dataExtractor.length === 0) {
    return null
  }
  let failList = state.dataExtractor.filter((e) => {
    return e.state !== '1'
  })
  return failList.length === 0
})


  defineExpose({
    setData
  })
</script>

<template>
  <div>
    <el-tabs v-model="activeName" style="overflow-y: auto">

      <!--响应体-->
      <el-tab-pane name='ApiResponseBody'>
        <template #label>
          <strong>实时响应</strong>
        </template>
        <div class="response">
          <div class="response-info">
            <el-tag type="success"
                    class="response-info__item"
                    effect="dark">
              {{ state.status_code === 200 ? state.status_code + ' OK' : state.status_code }}
            </el-tag>
            <el-tag type="success"
                    effect="plain"
                    class="response-info__item">
              响应时间：{{ state.response_time }} ms
            </el-tag>
            <el-tag type="primary"
                    effect="plain"
                    class="response-info__item">
              ContentLength：{{ state.content_length }}
            </el-tag>
            <el-tag type="info"
                    effect="plain"
                    class="response-info__item">
              ContentType：{{ state.content_type }}
            </el-tag>
          </div>
        </div>
        <div>
          <mirror-code
              style="height: 500px"
              v-model="state.responseBody"
              :constModelData="state.responseBody"
              :editorConfig="state.editorConfig"
          >
          </mirror-code>
        </div>
      </el-tab-pane>

      <!--请求信息-->
      <el-tab-pane name='ApiResponseHeaders'>
        <template #label>
          <strong>请求头</strong>
        </template>
        <div>
          <div v-for="(value, key) in state.headers" :key="key">
            <span style="font-size: 12px">
            <span style="font-weight: 600">{{ key}}: </span><span>{{ value }}</span>
            </span>
          </div>
        </div>
      </el-tab-pane>

      <!--运行日志-->
      <el-tab-pane name='ApiResponseLog'>
        <template #label>
          <strong>运行日志</strong>
        </template>
        <div>
          <mirror-code
              style="height: 500px"
              v-model="state.runLog"
              :constModelData="state.runLog"
              :editorConfig="state.editorConfig"
          >
          </mirror-code>
        </div>
      </el-tab-pane>

      <!--结果断言-->
      <el-tab-pane name='ApiValidateExtractor' v-show="state.validateExtractor">
        <template #label>
          <strong>结果断言</strong>
          <el-icon v-show="getValidatorsResultStatus !== null">
            <CircleCheck v-if="getValidatorsResultStatus" style="color: #0cbb52"></CircleCheck>
            <CircleClose v-else style="color: red"></CircleClose>
          </el-icon>
        </template>
        <div>
          <el-table :data="state.validateExtractor"
                    :header-cell-style="{ color: '#adaaaa', fontSize: '13px', fontWeight: 'bold'}"
          >
            <el-table-column prop="expect" label="断言表达式" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="methods" label="断言方式" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="actual" label="期望值" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="expected" label="实际结果" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="result" label="断言结果" show-overflow-tooltip="">
              <template #default="{ row }">
                <el-tag :type="row.result === '【✔】'? 'success': 'danger'">{{ row.result }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!--参数提取-->
      <el-tab-pane name='ApiDataExtractor' v-show="state.dataExtractor">
        <template #label>
          <strong>参数提取</strong>
          <el-icon v-show="getDataExtractorResultStatus !== null">
            <CircleCheck v-if="getDataExtractorResultStatus" style="color: #0cbb52"></CircleCheck>
            <CircleClose v-else style="color: red"></CircleClose>
          </el-icon>
        </template>
        <div>
          <el-table :data="state.dataExtractor"
                    :header-cell-style="{ color: '#adaaaa', fontSize: '13px', fontWeight: 'bold'}"
          >
            <el-table-column prop="varsName" label="变量名" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="type" label="提取类型" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="expression" label="提取表达式" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="resultVal" label="提取值" show-overflow-tooltip=""></el-table-column>
            <el-table-column prop="result" label="提取结果" show-overflow-tooltip="">
              <template #default="{ row }">
                <el-tag :type="row.result === '【✔】'? 'success': 'danger'">{{ row.result }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!--错误信息-->
      <el-tab-pane name='ApiErrorMessage'>
        <template #label>
          <strong>错误信息</strong>
          <el-icon v-if="state.errMessage !== ''">
            <CircleClose style="color: red"></CircleClose>
          </el-icon>
        </template>
        <div>
          <pre>{{ state.errMessage }}</pre>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped lang="scss">
.response {
  .response-info {
    margin-bottom: 15px;

    .response-info__item {
      margin-right: 8px;
    }
  }
}
</style>