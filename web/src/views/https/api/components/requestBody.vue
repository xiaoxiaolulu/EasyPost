<template>
  <el-form :inline="true" label-width="50px" size="small" label-position="right" ref="requestFormRef">
    <div style="border-bottom: 1px solid #E6E6E6; display: flex; justify-content: space-between">
      <div class="request-mode">
        <el-radio-group
            size="small"
            v-model="mode"
        >
          <el-radio label="none">none</el-radio>
          <el-radio label="form_data">form-data</el-radio>
          <el-radio label="x_www_form_urlencoded">x-www-form-urlencoded</el-radio>
          <el-radio label="raw">raw</el-radio>
        </el-radio-group>
      </div>
    </div>

    <!--没有请求体-->
    <div v-if="mode === 'none'" style="text-align: center; padding-top: 10px">
      <span style="color: darkgray">该请求暂时没有正文</span>
    </div>

    <!--form-data-->
    <div v-if="mode === 'form_data'" style="text-align: center; padding-top: 10px">
      <span style="color: darkgray">hahahha</span>
    </div>

    <!--x_www_form_urlencoded-->
    <div v-if="mode === 'x_www_form_urlencoded'" style="text-align: center; padding-top: 10px">
      <span style="color: darkgray">4444444</span>
    </div>
  </el-form>
</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import {deepObjClone} from "@/utils";

const mode = ref('none')

const state = reactive({
  // formData
  formData: [],
  // x_www_form_urlencoded
  x_www_form_urlencoded: [],
});

const setData = (data) => {
  if (!data) return
  switch (mode.value) {
    case 'form_data':
      state.formData = data.data ? data.data : []
      break
    case 'x_www_form_urlencoded':
      state.x_www_form_urlencoded = data.data ? data.data : []
    default:
      break
  }
}

const getData = () => {
  let requestData = {
    'mode': '',
    'data': []
  }
  requestData.mode = mode.value
  if (mode.value === 'form_data') {
    requestData.data = state.formData.filter((e) => e.key !== "" || e.value !== "")
  }
  if (mode.value === 'x_www_form_urlencoded') {
    requestData.data = state.x_www_form_urlencoded.filter((e) => e.key !== "" || e.value !== "")
  }
  if (mode.value === 'none') {
    requestData.data = null
  }
  return requestData
}

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