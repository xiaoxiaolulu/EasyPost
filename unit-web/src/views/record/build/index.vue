<template>
  <div class="app-container">
    <div class="container">
      <div>
        <el-form :inline="true" :model="queryParams">
          <el-form-item style="float: right">
            <el-input
                :suffix-icon="Search"
                clearable
                v-model.trim="queryParams.name"
                placeholder="请输入报告名称"
                @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData"
                v-loading="tableLoading"
                element-loading-text="拼命加载中"
                style="width: 100%">
        <el-table-column type="index" width="55" label="id">
          <template #default="scope">
            <span>#{{scope.row.id}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="计划名称"></el-table-column>
        <el-table-column prop="tester" label="执行者"></el-table-column>
        <el-table-column prop="all" label="总数">
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
        <el-table-column prop="begin_time" label="开始时间" width="200px">
          <template #default="scope">
            <span>{{ parseTime(scope.row.begin_time) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template #default="scope">
            <el-button @click="editHandler(scope.row)" type="primary" link>查看</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          style="margin-top: 8px;"
          v-model:currentPage="queryParams.page"
          :page-size="20"
          :pager-count="11"
          layout=">, total, prev, pager, next, jumper"
          :total="count"
          @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import {Plus, Search, Close, WarningFilled} from "@element-plus/icons-vue";
import {ref, reactive} from 'vue'
import {useRouter} from "vue-router";
import {envList, envDelete} from "@/api/setting";
import {parseTime} from "@/utils";
import {ElMessage, ElPagination} from "element-plus";
import {showErrMessage} from "@/utils/element";
import {recordList} from "@/api/record";

const queryParams = reactive({
  name: '',
  page: 1
})

const loading = ref(false)

const tableData = ref(null)

const tableLoading = ref(false)

const count = ref(0)

const router = useRouter()

const queryList = () => {
  tableLoading.value = true;
  recordList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    console.log(error)
    ElMessage.error("获取测试报告数据失败;请重试！")
  })
}

queryList()

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
}

const editHandler = (row) => {
  if (row) {
    router.push({
      name: "recordDetail",
      query: {id: row.id}
    });
  } else {
    ElMessage.error("查询测试报告异常请重试!");
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-input-number {
  .el-input__inner {
    text-align: left;
  }
}


.el-tooltip__popper {
  max-width: 20%;
}

.avatar {
  margin: 0;
  padding: 0;
  color: rgba(0, 0, 0, .85);
  font-size: 13px;
  font-variant: tabular-nums;
  line-height: 1.5715;
  list-style: none;
  font-feature-settings: "tnum", "tnum";
  position: relative;
  display: inline-block;
  overflow: hidden;
  color: #fff;
  white-space: nowrap;
  text-align: center;
  vertical-align: middle;
  background: #ccc;
  width: 32px;
  height: 32px;
  line-height: 32px;
  border-radius: 50%
}
</style>
