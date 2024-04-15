<template>
  <div class="home-container">
    <div style="height: 100%; width: 100%">
      <el-card class="box-card">
        <div class="pageHeaderContent">
          <div class="avatar">
            <span class="avatar-lg">
              <el-avatar :size="100" :src="AvatarLogo" shape="square"/>
            </span>
          </div>
          <div class="content">
            <div class="contentTitle name">
              Null!
              <el-tag style="margin-right: 10px">超级管理员</el-tag>
              <el-tag style="margin-right: 10px">测试组</el-tag>
            </div>
            <div class="description">登录时间：2024-02-06 14:26:43</div>
            <div class="description">访问Ip：localhost:8080</div>
          </div>
          <div class="extraContent">
            <div class="statItem">
              <div class="statistic user-statistics">
                <el-card class="user-statistics-card" v-for="s in state.statisticsCredData" :key="s.name">
                  <div class="statistics-number"><span>{{ s.number }}</span></div>
                  <div class="statistics-comparison" :style="{color: s.ratio >= 0? '#0cbb52': '#ff6462'}">
                    <el-icon class="statistics-comparison__text">
                      <Top v-if="s.ratio >= 0"/>
                      <Bottom v-else></Bottom>
                    </el-icon>
                    <span class="statistics-comparison__text" style="margin-right: 5px">{{ s.ratio }}</span>
                    <el-tooltip :content="s.ratioDescribe" placement="top">
                      <el-icon class="statistics-comparison__text">
                        <InfoFilled></InfoFilled>
                      </el-icon>
                    </el-tooltip>
                  </div>
                  <div class="font12">{{ s.name }}</div>
                </el-card>
              </div>
            </div>
          </div>
        </div>
      </el-card>
      <div style="margin-top: 10px">
        <el-row :gutter="10">
          <el-col :span="8">
            <el-card style="height: 100%">
              <template #header><strong>Swagger配置</strong></template>
              <el-space :size="20" :spacer="spacer">
                <div v-for="(card, index) in swagger" :key="index">
                  <div class="span-container">
                    <span><strong style="font-size: 20px; color: #1f2d3d">{{ card.state }}</strong></span>
                    <span>{{ card.content }}</span>
                  </div>
                </div>
              </el-space>
              <apexchart style="margin-top: 5px" type="polarArea" :options="chartOptions" :series="series"></apexchart>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card style="height: 100%">
              <template #header><strong>APIs</strong></template>
              <el-space :size="100" :spacer="spacer">
                <div v-for="(card, index) in apis" :key="index">
                  <div class="span-container">
                    <span><strong style="font-size: 20px; color: #1f2d3d">{{ card.state }}</strong></span>
                    <span>{{ card.content }}</span>
                    <span style="margin-top: 50px">{{ card.label }}:<strong style="color: #181616">{{
                        card.count
                      }}</strong></span>
                  </div>
                </div>
              </el-space>
              <el-card style="margin-top: 10px">
                <div class="span-container">
                  <div v-for="(card, index) in summary" :key="index">
                  <span>{{ card.label }}:{{ card.state }}
                    <strong :class="`opblock-${card.style}`">{{ card.type }}:{{ card.count }}</strong>
                  </span>
                  </div>
                </div>
              </el-card>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card style="height: 100%">
              <template #header><strong>Jobs</strong></template>
              <el-space :size="100" :spacer="spacer">
                <div v-for="(card, index) in jobs" :key="index">
                  <div class="span-container">
                    <span><strong style="font-size: 20px; color: #1f2d3d">{{ card.state }}</strong></span>
                    <span>{{ card.content }}</span>
                    <span>{{ card.status }}: {{ card.number }}</span>
                  </div>
                </div>
              </el-space>
              <el-card style="margin-top: 60px">
                <div class="span-container">
                  <div v-for="(card, index) in summary" :key="index">
                  <span>{{ card.label }}:{{ card.state }}
                    <strong :class="`opblock-${card.style}`">{{ card.type }}:{{ card.count }}</strong>
                  </span>
                  </div>
                </div>
              </el-card>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

  </div>
</template>
<script setup lang="ts">
import {User, Top, Bottom, InfoFilled, Warning} from '@element-plus/icons-vue'
import {ref, reactive, h} from 'vue'
import AvatarLogo from '@/assets/image/avatar.png'
import {ElDivider} from 'element-plus'
import weLogo from '@/assets/image/we.png'
import CountTo from '@/components/CountTo/index.vue'
import BarCharts from '@/views/echarts/simple/components/bar.vue'
import {c} from "unimport/dist/types-43c63a16";

const spacer = h(ElDivider, {direction: 'vertical'})

const swagger = ref([
  {id: 1, content: 'Swagger', state: "40"},
  {id: 2, content: 'SwaggerApis', state: "20333"},
  {id: 3, content: 'Api录入覆盖率', state: "21.05%"}
])

const apis = ref([
  {id: 1, content: 'Api测试覆盖', state: "25%", count: 111, label: "API总数"},
  {id: 2, content: '用例通过率', state: "46%", count: 222, label: "用例总数"}
])

const summary = ref([
  {id: 1, label: 'API七日新增总', state: "0", type: "RestApi", count: 111, style: "green"},
  {id: 2, label: 'API七日调试', state: "12", type: "OpenApi", count: 111, style: "blue"},
  {id: 2, label: 'API七日导入(未维护)', state: "41", type: "DubboAPI", count: 111, style: "orange"},
  {id: 2, label: 'API七日导入(已维护)', state: "46", type: "API已锁定", count: 222, style: "red"}
])

const jobs = ref([
  {id: 1, content: '任务成功', state: "25%", status: "成功", number: 333},
  {id: 2, content: '任务失败', state: "46%", status: "失败", number: 444}
])
const series = ref([14, 11, 12])
const chartOptions = ref(
    {
      chart: {
        type: 'polarArea',
      },
      stroke: {
        colors: ['#fff']
      },
      labels: ['middle', 'coupon', 'user'],
      fill: {
        opacity: 0.8
      },
      responsive: [{
        breakpoint: 480,
        options: {
          chart: {
            width: 200
          },
          legend: {
            position: 'bottom'
          }
        }
      }]
    },
)

const state = reactive({
  statisticsCredData: [
    {
      number: 21,
      name: '接口数量',
      ratio: 0,
      ratioDescribe: '(当月新增接口数量-上月新增接口数量)/上月新增接口数量×100%'
    },
    {
      number: 21,
      name: '接口用例数量',
      ratio: 0,
      ratioDescribe: '(当月新增接口用例数量-上月新增接口用例数量)/上月新增接口用例数量×100%'
    },
    {
      number: 21,
      name: 'UI用例数量',
      ratio: 0,
      ratioDescribe: '(当月新增UI用例数量-上月新增UI用例数量)/上月新增UI用例数量×100%'
    },
    {
      number: 21,
      name: '任务数量',
      ratio: 0,
      ratioDescribe: '(当月新增任务数量-上月新增任务数量)/上月新增任务数量×100%'
    },
  ],
  global: {
    homeChartOne: null,
    homeChartTwo: null,
    homeCharThree: null,
    dispose: [null, '', undefined],
  },
  homeOne: [
    {
      num1: '125,12',
      num2: '-12.32',
      num3: '订单统计信息',
      num4: 'fa fa-meetup',
      color1: '#FF6462',
      color2: '--next-color-primary-lighter',
      color3: '--el-color-primary',
    },
    {
      num1: '653,33',
      num2: '+42.32',
      num3: '月度计划信息',
      num4: 'iconfont icon-ditu',
      color1: '#6690F9',
      color2: '--next-color-success-lighter',
      color3: '--el-color-success',
    },
    {
      num1: '125,65',
      num2: '+17.32',
      num3: '年度计划信息',
      num4: 'iconfont icon-zaosheng',
      color1: '#6690F9',
      color2: '--next-color-warning-lighter',
      color3: '--el-color-warning',
    },
    {
      num1: '520,43',
      num2: '-10.01',
      num3: '访问统计信息',
      num4: 'fa fa-github-alt',
      color1: '#FF6462',
      color2: '--next-color-danger-lighter',
      color3: '--el-color-danger',
    },
  ],
  homeThree: [
    {
      icon: 'iconfont icon-yangan',
      label: '浅粉红',
      value: '2.1%OBS/M',
      iconColor: '#F72B3F',
    },
    {
      icon: 'iconfont icon-wendu',
      label: '深红(猩红)',
      value: '30℃',
      iconColor: '#91BFF8',
    },
    {
      icon: 'iconfont icon-shidu',
      label: '淡紫红',
      value: '57%RH',
      iconColor: '#88D565',
    },
    {
      icon: 'iconfont icon-shidu',
      label: '弱紫罗兰红',
      value: '107w',
      iconColor: '#88D565',
    },
    {
      icon: 'iconfont icon-zaosheng',
      label: '中紫罗兰红',
      value: '57DB',
      iconColor: '#FBD4A0',
    },
    {
      icon: 'iconfont icon-zaosheng',
      label: '紫罗兰',
      value: '57PV',
      iconColor: '#FBD4A0',
    },
    {
      icon: 'iconfont icon-zaosheng',
      label: '暗紫罗兰',
      value: '517Cpd',
      iconColor: '#FBD4A0',
    },
    {
      icon: 'iconfont icon-zaosheng',
      label: '幽灵白',
      value: '12kg',
      iconColor: '#FBD4A0',
    },
    {
      icon: 'iconfont icon-zaosheng',
      label: '海军蓝',
      value: '64fm',
      iconColor: '#FBD4A0',
    },
  ],
  myCharts: [],
  charts: {
    theme: '',
    bgColor: '',
    color: '#303133',
  },
});
const goTo = (url) => {
  window.open(url, '_blank')
}
</script>

<style scoped lang="scss">
@import "./index";

.span-container span {
  display: block;
  align-items: center;
  font-size: 12px;
  color: var(--el-text-color-regular);
  margin-top: 5px;
}

.opblock-green {
  float: right;
  color: #0dd40d;
}

.opblock-blue {
  float: right;
  color: deepskyblue;
}

.opblock-orange {
  float: right;
  color: orange;
}

.opblock-red {
  float: right;
  color: red;
}
</style>
