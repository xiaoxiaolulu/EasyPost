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

  </el-form>
</template>

<script setup lang="ts">
import {ref} from "vue";

const mode = ref('none')
</script>


<style scoped lang="scss">
.request-mode {
  margin-bottom: 10px;

  :deep(.el-radio__label) {
    font-size: 13px;
  }
}
</style>