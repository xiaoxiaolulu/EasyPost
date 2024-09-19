<script setup lang="ts">
  import {ref} from "vue";
  import {reactive} from 'vue';
  import MirrorCode from "@/components/MirrorCode/index.vue";

  const activeName =  ref('ApiResponseBody')

  const state = reactive({
    runLog: "",
    status_code: "",
    response_time: "",
    content_type: "",
    responseBody: "",
    headers: "",
    editorConfig: { language: 'python', theme: 'vs' },
  })

  // init
  const setData = (data) => {
    if (data){
      state.runLog = data['logData'].join('')
      state.status_code = data['statusCode']
      state.response_time = data['runTime']
      state.responseBody = data['responseBody']
      state.headers = JSON.parse(data['requestsHeader'])
    }
  }

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