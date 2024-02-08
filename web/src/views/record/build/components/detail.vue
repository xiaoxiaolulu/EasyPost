<template>
  <div class="app-container">
    <el-card style="margin-bottom: 10px">
      <div class="report-seal"
           :style="{border: `solid 4px var(${reportStatus? '--el-color-success': '--el-color-danger'})`}">
        <div class="report-seal-son"
             :style="{border: `solid 2px var(${reportStatus? '--el-color-success': '--el-color-danger'})`,
           color: `var(${reportStatus? '--el-color-success': '--el-color-danger'})`
      }">
          <span class="report-seal-text">{{ reportStatus ? "通过" : "不通过" }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import {h, reactive, nextTick, watch, onMounted, computed} from "vue";

const state = reactive({
  // statisticsData
  statisticsData: {
    success: 1
  },
})

const reportStatus = computed(() => {
  return state.statisticsData?.success === 1 || state.statisticsData?.success
})

</script>

<style lang="scss">
.report-seal {
  z-index: 1;
  position: absolute;
  right: 10px;
  margin-top: -30px;
  //top: 5px;
  width: 80px;
  height: 80px;
  //border: solid 4px var(--el-color-success);
  border-radius: 100%;
  background-color: var(--el-tag--success-color);
  display: flex;
  justify-content: center;
  align-items: center;
}

.report-seal-son {
  width: 60px;
  height: 60px;
  line-height: 60px;
  //border: solid 2px var(--el-color-success);
  border-radius: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  position: relative;
  text-align: center;
  vertical-align: middle;
  transform: rotate(45deg);
  //color: var(--el-color-success);
  font-size: 16px;
  font-weight: 900;
}
</style>