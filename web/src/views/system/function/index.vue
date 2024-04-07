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
                placeholder="请输入名称函数"
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
        </el-table-column>
        <el-table-column prop="name" label="函数名称"></el-table-column>
        <el-table-column prop="remarks" label="备注"></el-table-column>
        <el-table-column prop="creator.username" label="创建者">
          <template #default="scope">
            <div style="margin-inline-end:16px;display:inline">
              <img v-if="scope.row.creator.avatar" :src="scope.row.creator.avatar" class="avatar" alt="">
            </div>
            <div style="display:inline;color: rgba(0, 0, 0, 0.88);">
              <span style="color:rgb(22, 119, 255)">{{ scope.row.creator.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="update_time" label="更新时间" width="200px">
          <template #default="scope">
            <span>{{ parseTime(scope.row.update_time) }}</span>
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
import {functionList} from "@/api/setting";
import {parseTime} from "@/utils";
import {ElMessage, ElPagination} from "element-plus";
import {showErrMessage} from "@/utils/element";

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
  functionList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    console.log(error)
    ElMessage.error("获取内置函数数据失败;请重试！")
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
      name: "functionDetail",
      query: {id: row.id}
    });
  } else {
    ElMessage.error("查询内置函数异常请重试!");
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
