<template>
  <div class="app-container">
    <div class="container">
      <div>
        <el-form :inline="true" :model="queryParams">
          <el-form-item style="float: right">
            <el-input
              :suffix-icon="Search"
              clearable
              v-model.trim="queryParams.id"
              placeholder="请输入任务id"
              @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData"
                v-loading="tableLoading"
                element-loading-text="拼命加载中"
                style="width: 100%">
        <el-table-column type="index" width="55" label="序号"></el-table-column>
        <el-table-column label="任务id">
          <template #default="scope">
            <span>{{scope.row.id}}</span>
          </template>
        </el-table-column>
        <el-table-column width="80" prop="status" label="状态"></el-table-column>
        <el-table-column width="200px" prop="error_msg" label="错误信息"></el-table-column>
        <el-table-column width="150px" prop="trigger" label="执行器"></el-table-column>
        <el-table-column prop="desc" label="任务描述"></el-table-column>
        <el-table-column prop="run_time" label="运行时间" width="200px">
          <template #default="scope">
            <span>{{ parseTime(scope.row.run_time) }}</span>
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
import {Search} from "@element-plus/icons-vue";
import {ref, reactive} from 'vue'
import {useRouter} from "vue-router";
import {parseTime} from "@/utils";
import {ElMessage, ElPagination} from "element-plus";
import {taskRecordList} from "@/api/record";

const queryParams = reactive({
  id: '',
  page: 1
})

const tableData = ref(null)

const tableLoading = ref(false)

const count = ref(0)

const queryList = () => {
  tableLoading.value = true;
  taskRecordList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    console.log(error)
    ElMessage.error("获取历史任务执行信息失败;请重试！")
  })
}

queryList()

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
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
</style>
