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
      <ReportStatistics :data="state.statisticsData"></ReportStatistics>
    </el-card>
    <el-card>
      <div>
        <el-form :inline="true" :model="queryParams">
          <el-form-item style="float: right">
            <el-input
                :suffix-icon="Search"
                clearable
                v-model.trim="queryParams.name"
                placeholder="用例名称"
                @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <div>
        <el-table :data="tableData"
                  v-loading="tableLoading"
                  element-loading-text="拼命加载中"
                  :header-cell-style="{'background-color':'#ffffff','color':'#babac0' }"
                  style="width: 100%"
        >
          <el-table-column type="expand">
            <template #default="props">
              <div v-for="(item) in props.row.steps" :key="item.id">
                <div class="opblock" :class="`opblock-${item.method.toLowerCase()}`">
                  <div class="opblock-summary">
                    <span class="opblock-summary-index">
                      第{{item.sort}}步
                    </span>
                    <span class="opblock-summary-method">
                      {{ item.method }}
                    </span>
                    <span class="opblock-summary-path">
                      {{ item.url }}
                    </span>
                    <div class="opblock-summary-description">
                      {{ item.name }}
                    </div>
                    <div style="float: right">
                      <el-button type="primary" link @click="viewDetail(item)">详情</el-button>
                    </div>
                  </div>
                </div>
              </div>
              <el-drawer
                  v-model="state.showDetailInfo"
                  size="70%"
                  append-to-body
                  direction="ltr"
                  destroy-on-close
                  :with-header="true">
                <template #header>
                        <span>
                          <strong class="pr10">报告详情</strong>
                          <el-tag type="danger" v-if="state.statisticsData.success === 0">不通过</el-tag>
                          <el-tag type="success" v-else>通过</el-tag>
                        </span>
                </template>
                <div style="height: 500px; overflow-y: auto">
                  <case-step-detail :reportData="ResponseData"></case-step-detail>
                </div>
              </el-drawer>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="用例名称"></el-table-column>
          <el-table-column prop="all" label="步骤总数">
            <template #default="scope">
              <el-tag type="info">{{scope.row.all}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="success" label="成功数">
            <template #header="{ column }">
              <span>{{ column.label }}</span>
              <el-icon style="color: #7a8b9a"><Select/></el-icon>
            </template>
            <template #default="scope">
              <el-tag type="success">{{scope.row.success}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="fail" label="失败数">
            <template #header="{ column }">
              <span>{{ column.label }}</span>
              <el-icon style="color: red"><Close /></el-icon>
            </template>
            <template #default="scope">
              <el-tag type="danger">{{scope.row.fail}}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="error" label="错误数">
            <template #header="{ column }">
              <span>{{ column.label }}</span>
              <el-icon style="color: orange"><WarningFilled /></el-icon>
            </template>
            <template #default="scope">
              <el-tag type="warning">{{scope.row.error}}</el-tag>
            </template>
          </el-table-column>
        <!--分页组件-->
          <el-pagination
              style="margin-top: 8px;"
              v-model:currentPage="queryParams.page"
              :page-size="20"
              :pager-count="11"
              layout=">, total, prev, pager, next, jumper"
              :total="count"
              @current-change="handlePageChange"
          />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import {useRoute} from "vue-router";
import {h, reactive, nextTick, watch, onMounted, computed, ref} from "vue";
import ReportStatistics from "./ReportStatistics.vue"
import {Close, Search, WarningFilled} from "@element-plus/icons-vue";
import {ElMessage, ElPagination} from "element-plus";
import {recordDetail} from "@/api/record";
import CaseStepDetail from "@/views/record/build/components/caseStepDetail.vue";

const route = useRoute()

const state = reactive({
  // statisticsData
  statisticsData: {
    avg_request_time: 66.74,
    case_count: 0,
    case_fail_count: 0,
    case_pass_rate: 100,
    case_success_count: 0,
    exec_user_id: 7,
    exec_user_name: "admin1",
    request_time_count: 0.071,
    start_time: "2024-02-06 13:55:23",
    step_count: 1,
    step_error_count: 0,
    step_fail_count: 0,
    step_pass_rate: 100,
    step_skip_count: 0,
    step_success_count: 1,
    success: 1
  },
  showDetailInfo: false
})

const queryParams = reactive({
  id: '',
  name: '',
  page: 1
})

const tableLoading = ref(false)

const tableData = ref([])

const count = ref(0)

const ResponseData = ref()

const reportStatus = computed(() => {
  return state.statisticsData?.success === 1 || state.statisticsData?.success
})

const queryList = () => {
  tableLoading.value = true;
  queryParams.id = route.query.id
  console.log(queryParams)
  recordDetail(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    // console.log(error.response)
    ElMessage.error("获取报告数据失败;请重试！")
  })
}

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
}

const viewDetail = (row) => {
  if (row) {
    console.log("测试")
    console.log(row)
    console.log("测试")
    state.showDetailInfo = true
    ResponseData.value = eval(row)
  }
}

queryList()
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

.opblock {
  border: 1px solid #000;
  border-radius: 4px;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.19);
  margin: 0 0 15px;
}

.opblock.opblock-get {
  background: rgba(73, 139, 204, 0.1);
  border-color: #4950cc;
}

.opblock.opblock-post {
  background: rgba(73, 204, 144, 0.1);
  border-color: #49cc90;
}

.opblock.opblock-put {
  background: rgba(204, 163, 73, 0.1);
  border-color: #e39f0a;
}

.opblock.opblock-delete {
  background: rgba(204, 93, 73, 0.1);
  border-color: #ea0b0b;
}

.opblock .opblock-summary {
  align-items: center;
  cursor: pointer;
  display: flex;
  padding: 5px;
}

.opblock.opblock-get .opblock-summary {
  border-color: #4950cc;
}

.opblock.opblock-post .opblock-summary {
  border-color: #49cc90;
}

.opblock.opblock-put .opblock-summary {
  border-color: #e39f0a;
}

.opblock.opblock-delete .opblock-summary {
  border-color: #ea0b0b;
}

.opblock.opblock-get .opblock-summary-method {
  background: #122de1;
}

.opblock.opblock-post .opblock-summary-method {
  background: #49cc90;
}

.opblock.opblock-put .opblock-summary-method {
  background: #e7a20c;
}

.opblock.opblock-delete .opblock-summary-method {
  background: #f30808;
}

.opblock .opblock-summary-method {
  background: #000;
  border-radius: 3px;
  color: #fff;
  font-family: sans-serif;
  font-size: 14px;
  font-weight: 700;
  min-width: 80px;
  padding: 6px 0;
  text-align: center;
  text-shadow: 0 1px 0 rgba(0, 0, 0, 0.1);
}

.opblock .opblock-summary-index {
  background: #45c0e5;
  border-radius: 3px;
  color: #fff;
  font-family: sans-serif;
  font-size: 14px;
  font-weight: 700;
  min-width: 80px;
  padding: 6px 0;
  text-align: center;
  text-shadow: 0 1px 0 rgba(0, 0, 0, 0.1);
  margin-right: 10px;
}

.opblock .opblock-summary-path {
  flex-shrink: 0;
  font-size: 12px;
}

.opblock .opblock-summary-path {
  align-items: center;
  color: #3b4151;
  display: flex;
  font-family: monospace;
  font-size: 16px;
  font-weight: 600;
  padding: 0 10px;
  word-break: break-word;
}

.opblock .opblock-summary-description {
  color: #3b4151;
  flex: 1 1 auto;
  font-family: sans-serif;
  font-size: 13px;
  word-break: break-word;
}
</style>