<template>
  <div class="echarts-container">
    <el-row>
      <el-col :span="6">
        <el-row>
          <el-col :span="8">
            <div class="echarts-pie" ref="requestTime"></div>
          </el-col>
          <el-col :span="16" style="margin: auto">
            <div class="echarts-item">
              <div class="echarts-item__info">
                <strong>平均请求耗时：</strong>
                <span class="echarts-item__info__number">{{ data.avg_request_time }} sm</span>
              </div>
              <div class="echarts-item__info">
                <strong>执行总耗时：</strong>
                <span class="echarts-item__info__number">{{ data.request_time_count }} m</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="6">
        <el-row>
          <el-col :span="8">
            <div class="echarts-pie" ref="apiTestCase"></div>
          </el-col>
          <el-col :span="16" style="margin: auto">
            <div class="echarts-item">
              <div class="echarts-item__info">
                <el-row>
                  <el-col :span="12">
                    <div>
                      <strong>测试用例：</strong>
                      <span class="echarts-item__info__number">{{ data.case_count }}</span>
                    </div>

                    <div class="echarts-item__info">
                      <span>成功：</span>
                      <span class="">{{ data.case_success_count }}</span>
                    </div>

                  </el-col>
                  <el-col :span="12">

                    <div>
                      <strong>通过率：</strong>
                      <span class="echarts-item__info__number">{{
                          `${data.case_pass_rate == null ? '--' : data.case_pass_rate + '%'}`
                        }}</span>
                    </div>

                    <div class="echarts-item__info">
                      <span>失败：</span>
                      <span class="">{{ data.case_fail_count }}</span>
                    </div>

                  </el-col>
                </el-row>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="6">
        <el-row>
          <el-col :span="8">
            <div class="echarts-pie" ref="apiTestStep"></div>
          </el-col>
          <el-col :span="16" style="margin: auto">
            <div class="echarts-item">
              <div class="echarts-item__info">
                <el-row>
                  <el-col :span="12">
                    <div>
                      <strong>测试步骤：</strong>
                      <span class="echarts-item__info__number">{{ data.step_count }}</span>
                    </div>
                    <div>
                      <span>成功：</span>
                      <span class="">{{ data.step_success_count }}</span>
                    </div>
                    <div>
                      <span>跳过：</span>
                      <span class="">{{ data.step_skip_count }}</span>
                    </div>

                  </el-col>
                  <el-col :span="12">
                    <div>
                      <strong>通过率：</strong>
                      <span class="echarts-item__info__number">{{ data.step_pass_rate }}%</span>
                    </div>

                    <div>
                      <span>失败：</span>
                      <span class="">{{ data.step_fail_count }}</span>
                    </div>

                    <div>
                      <span>错误：</span>
                      <span class="">{{ data.step_error_count }}</span>
                    </div>

                  </el-col>
                </el-row>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-col>

      <el-col :span="6" style="margin: auto">
        <div class="echarts-item" style="padding: 20px">

          <div class="echarts-item__info">
            <strong>执行时间：</strong>
            <span class="">{{ data.start_time }}</span>
          </div>

          <div class="echarts-item__info">
            <strong>执行人：</strong>
            <span class="">{{ data.exec_user_name }}</span>
          </div>
        </div>

      </el-col>

    </el-row>
  </div>
</template>

<script setup name="ReportStatistics">
import * as ECharts from 'echarts'
import {nextTick, onMounted, onUnmounted, reactive, ref, watch} from "vue";


const props = defineProps({
  data: {
    type: Object
  },
  start_time: {
    type: String
  },
  exec_user_name: {
    type: String
  },
})


const requestTime = ref()
const apiTestCase = ref()
const apiTestStep = ref()
const state = reactive({
  requestTimeECharts: null,
  stepECharts: null,
  caseECharts: null,
})

const initRequestTime = () => {
  if (!state.requestTimeECharts) {
    state.requestTimeECharts = ECharts.init(requestTime.value)
  }
  state.requestTimeECharts.setOption(getOption(100))
}

const initApiTestCase = () => {
  if (!state.caseECharts) {
    state.caseECharts = ECharts.init(apiTestCase.value)
  }
  state.caseECharts.setOption(getOption(props.data?.case_pass_rate))
}

const initApiTestStep = () => {
  if (!state.stepECharts) {
    state.stepECharts = ECharts.init(apiTestStep.value)
  }
  state.stepECharts.setOption(getOption(props.data?.step_pass_rate))
}

const initEcharts = () => {
  initRequestTime()
  initApiTestCase()
  initApiTestStep()
}

const getOption = (value) => {
  return {
    // tooltip: {
    //
    //   trigger: 'item',
    //   formatter: '{a} <br/>{b} : {c} ({d}%)'
    // },
    // legend: {
    //   top: '0%',
    //   left: 'right',
    //   data: ['成功', '失败']
    // },
    graphic: {
      type: "text",
      left: "center",
      top: "45%",
      style: {
        text: value == null ? '--' : value + '%',
        textAlign: "center",
        // fill: "#333",
        fontSize: 12,
        fontWeight: 500
      }
    },
    series: [
      {
        name: '用例结果',
        type: 'pie',
        radius: ['70%', '60%'],
        avoidLabelOverlap: false,
        hoverAnimation: false,
        itemStyle: {
          borderRadius: 5,
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center',
          // normal: {
          //   show: false,
          //   position: 'center',
          // }
        },
        emphasis: {
          label: {
            show: false,
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          {
            name: `${100 - value} %`,
            itemStyle: {color: '#e5e6f1'},
            value: 100 - value,
          },
          {
            name: `${value} %`,
            itemStyle: {color: '#7d92bd'},
            value: value,
          },

          // {
          //   name: '失败',
          //   itemStyle: {color: '#ee6666'},
          //   value: 2,
          // },
        ]
      }
    ]
  }
}

window.onresize = () => {
  state.requestTimeECharts?.resize();
  state.stepECharts?.resize();
  state.caseECharts?.resize();
}
onMounted(() => {
  watch(() => props.data,
      () => {
        nextTick(() => {
          initEcharts();
        })
      }, {
        deep: true
      })
});
onUnmounted(() => {
  if (state.requestTimeECharts) {
    state.requestTimeECharts?.dispose();
    state.requestTimeECharts = null
  }
  if (state.stepECharts) {
    state.stepECharts?.dispose();
    state.stepECharts = null
  }
  if (state.caseECharts) {
    state.caseECharts?.dispose();
    state.caseECharts = null
  }

});

onMounted(() => {
  nextTick(() => {
    initEcharts()
  })
})


</script>

<style lang="scss" scoped>
.echarts-container {
  .echarts-pie {
    height: 120px;
  }

  .el-col-12 {
    margin: auto;
  }

  .echarts-item {
    width: 100%;

    .echarts-item__info {
      width: 100%;
      line-height: 30px;
      //display: flex;

      .echarts-item__info__number {
        color: #67c23a;
      }
    }
  }
}
</style>