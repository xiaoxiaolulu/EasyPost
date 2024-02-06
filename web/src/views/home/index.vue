<template>
  <div class="home-container">
    <el-card class="box-card" style="height: 25%; width: 100%">
      <div class="pageHeaderContent">
        <div class="avatar">
            <span class="avatar-lg">
              <el-avatar :size="100" :src="AvatarLogo" shape="square" />
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
              <el-card  class="user-statistics-card" v-for="s in state.statisticsCredData" :key="s.name">
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
<!--    <el-row class="row-bg" :gutter="10">-->
<!--      <el-col :xs="24" :sm="12" :lg="8">-->
<!--        <el-card class="box-card" style="height: 100%">-->
<!--          <el-image-->
<!--              class="wechat"-->
<!--              :src="weLogo"-->
<!--              :preview-src-list="[weLogo]"-->
<!--              style="max-width: 200px"-->
<!--              :data-resid="Date.now()"-->
<!--          />-->
<!--          <div class="personal">-->
<!--            <div>-->
<!--              <el-avatar :size="50" :src="AvatarLogo" />-->
<!--            </div>-->
<!--            <div class="name"></div>-->
<!--            <div class="description"></div>-->
<!--            <div class="list">-->
<!--              <div>昵称：小狼</div>-->
<!--              <div>职业：前端</div>-->
<!--              <div>公司：小公司</div>-->
<!--              <div>年龄：~~</div>-->
<!--              <div>性别：男</div>-->
<!--              <div>现住址：中国-浙江-杭州</div>-->
<!--              <div>邮箱：1135957121@qq.com</div>-->
<!--              <div>微信：19550102670(欢迎加微信入群)</div>-->
<!--              <div>技术栈：JavaScript、HTML、CSS、Vue、Node、React</div>-->
<!--            </div>-->
<!--            <el-divider></el-divider>-->
<!--            <div style="margin-bottom: 15px"><h5>个性标签</h5></div>-->
<!--            <div>-->
<!--              <el-tag style="margin-right: 10px">怕麻烦</el-tag>-->
<!--              <el-tag style="margin-right: 10px">健身运动</el-tag>-->
<!--              <el-tag style="margin-right: 10px">睡觉</el-tag>-->
<!--              <el-tag style="margin-right: 10px">漫威</el-tag>-->
<!--              <el-tag>向往</el-tag>-->
<!--            </div>-->
<!--            <el-divider></el-divider>-->
<!--            <div style="margin-bottom: 15px"><h5>最喜欢的一句话</h5></div>-->
<!--            <div>&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45; 开心最重要</div>-->
<!--            <el-divider></el-divider>-->
<!--            <div style="margin-bottom: 15px"-->
<!--            ><h5>如果对你有帮助的话，可以麻烦点一颗 Star、Fork、Watch! 你的鼓励是我继续优化的动力~~</h5></div-->
<!--            >-->
<!--          </div>-->
<!--        </el-card>-->
<!--      </el-col>-->
<!--      <el-col :xs="24" :sm="12" :lg="16">-->
<!--        <el-row class="custom" :gutter="10">-->
<!--          <el-col :xs="24" :sm="12" :lg="8">-->
<!--            <el-card style="margin-bottom: 10px">-->
<!--              <div class="grid-content">-->
<!--                <div class="left"-->
<!--                ><el-icon style="font-size: 24px; color: white"><user /></el-icon-->
<!--                ></div>-->
<!--                <div class="right">-->
<!--                  <div-->
<!--                      class="h2"-->
<!--                      style="color: #2d8cf0"-->
<!--                  ><count-to-->
<!--                      :start-val="0"-->
<!--                      :end-val="5268"-->
<!--                      :duration="2000"-->
<!--                      :autoplay="true"-->
<!--                  ></count-to-->
<!--                  ></div>-->
<!--                  <div>用户访问量 </div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </el-card>-->
<!--          </el-col>-->
<!--          <el-col :xs="24" :sm="12" :lg="8">-->
<!--            <el-card style="margin-bottom: 10px">-->
<!--              <div class="grid-content">-->
<!--                <div class="left" style="background: #64d572"-->
<!--                ><el-icon style="font-size: 24px; color: white"><user /></el-icon-->
<!--                ></div>-->
<!--                <div class="right">-->
<!--                  <div-->
<!--                      class="h2"-->
<!--                      style="color: #64d572"-->
<!--                  ><count-to-->
<!--                      :start-val="0"-->
<!--                      :end-val="9599"-->
<!--                      :duration="2000"-->
<!--                      :autoplay="true"-->
<!--                  ></count-to-->
<!--                  ></div>-->
<!--                  <div>系统消息 </div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </el-card>-->
<!--          </el-col>-->
<!--          <el-col :xs="24" :sm="12" :lg="8">-->
<!--            <el-card style="margin-bottom: 10px">-->
<!--              <div class="grid-content">-->
<!--                <div class="left" style="background: #f25e43"-->
<!--                ><el-icon style="font-size: 24px; color: white"><user /></el-icon-->
<!--                ></div>-->
<!--                <div class="right">-->
<!--                  <div-->
<!--                      class="h2"-->
<!--                      style="color: #f25e43"-->
<!--                  ><count-to-->
<!--                      :start-val="0"-->
<!--                      :end-val="595453"-->
<!--                      :duration="2000"-->
<!--                      :autoplay="true"-->
<!--                  ></count-to-->
<!--                  ></div>-->
<!--                  <div>数量 </div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </el-card>-->
<!--          </el-col>-->
<!--        </el-row>-->
<!--        <el-card class="box-card">-->
<!--          <template #header>-->
<!--            <div class="card-header">-->
<!--              <span>系列开源产品</span>-->
<!--            </div>-->
<!--          </template>-->
<!--          <div style="display: flex">-->
<!--            <el-card-->
<!--                style="flex: 1; margin-right: 20px; cursor: pointer"-->
<!--                class="card-item"-->
<!--                @click="goTo('https://ext.dcloud.net.cn/plugin?id=7511')"-->
<!--            >-->
<!--              <div style="color: white; margin-bottom: 10px"><h3>zb-table</h3></div>-->
<!--              <div style="font-size: 12px; color: white"-->
<!--              >uniapp 表格组件-->
<!--                支持固定表头和首列、上拉加载更多、及固定多列，表格自适应内容，排序，多选checkbox、可点击删除，编辑、合计功能，兼容多端</div-->
<!--              >-->
<!--            </el-card>-->
<!--            <el-card-->
<!--                style="flex: 1; cursor: pointer"-->
<!--                class="card-item"-->
<!--                @click="goTo('https://github.com/zouzhibin/vue-admin-perfect')"-->
<!--            >-->
<!--              <div style="color: white; margin-bottom: 10px"><h3>vue-admin-perfect</h3></div>-->
<!--              <div style="font-size: 12px; color: white"-->
<!--              >系统基于vue3+vuex+ element-plus+ts后台管理系统</div-->
<!--              >-->
<!--            </el-card>-->
<!--          </div>-->
<!--        </el-card>-->
<!--        <el-card class="box-card">-->
<!--          <template #header>-->
<!--            <div class="card-header">-->
<!--              <span>每周用户活跃量</span>-->
<!--            </div>-->
<!--          </template>-->
<!--          <div>-->
<!--            <bar-charts height="300px" width="100%" id="bar1"></bar-charts>-->
<!--          </div>-->
<!--        </el-card>-->
<!--      </el-col>-->
<!--    </el-row>-->
  </div>
</template>
<script setup lang="ts">
  import { User, Top, Bottom, InfoFilled} from '@element-plus/icons-vue'
  import { ref, reactive} from 'vue'
  import AvatarLogo from '@/assets/image/avatar.png'
  import weLogo from '@/assets/image/we.png'
  import CountTo from '@/components/CountTo/index.vue'
  import BarCharts from '@/views/echarts/simple/components/bar.vue'

  const state = reactive({
    statisticsCredData: [
      {number: 21, name: '接口数量', ratio: 0, ratioDescribe: '(当月新增接口数量-上月新增接口数量)/上月新增接口数量×100%'},
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
      {number: 21, name: '任务数量', ratio: 0, ratioDescribe: '(当月新增任务数量-上月新增任务数量)/上月新增任务数量×100%'},
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
</style>
