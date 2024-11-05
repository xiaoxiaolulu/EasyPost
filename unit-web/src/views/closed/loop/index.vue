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
              placeholder="请输入通知名称"
              @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-table
        border
        :data="tableData"
        v-loading="tableLoading"
        element-loading-text="拼命加载中"
        style="width: 100%">
        <el-table-column prop="id" label="序号" width="55" />
        <el-table-column prop="name" label="名称" width="250"></el-table-column>
        <el-table-column prop="test_type" label="测试类型" align="center" width="150">
          <template #default="scope">
            <el-tag v-show="tag.status === scope.row.test_type" v-for="tag in testType" :key="tag.id" :type="tag.type">
              <el-icon>
                <component :is="tag.icon"/>
              </el-icon>
              {{ tag.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user.username" label="提测人" width="150">
          <template #default="scope">
            <div style="margin-inline-end:16px;display:inline">
              <img v-if="scope.row.user.avatar" :src="scope.row.user.avatar" class="avatar" alt="">
            </div>
            <div style="display:inline;color: rgba(0, 0, 0, 0.88);">
              <span style="color:rgb(22, 119, 255)">{{ scope.row.user.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="update_time" label="执行时间" width="200px">
          <template #default="scope">
            <span>{{ parseTime(scope.row.update_time) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="runnability" label="用例(失败/总计)">
        </el-table-column>
        <el-table-column prop="state" label="处理状态">
          <template #default="scope">
            <el-tag v-show="tag.status === scope.row.state" v-for="tag in stateType" :key="tag.id" :type="tag.type">
              {{ tag.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template #default="scope">
            <el-button @click="editData(scope.row)" type="primary" link>查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
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
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import { Search } from "@element-plus/icons-vue";
import {getClosedTasksList } from "@/api/http";
import { ElMessage, ElPagination } from "element-plus";
import { parseTime } from "@/utils";
import { useRouter } from "vue-router";

const queryParams = reactive({
  name: "",
  page: 1
});

const testType = reactive([
  { id: 1, type: 'success', status: 'UI', name: 'UI自动化', icon: 'Cpu'},
  { id: 2, type: 'danger', status: 'API', name: 'API自动化', icon: 'Guide'},
])

const stateType = reactive([
  { id: 1, type: 'success', status: 1, name: '待处理'},
  { id: 2, type: 'danger', status: 0, name: '已处理'},
])

const loading = ref(false);

const tableData = ref(null);

const tableLoading = ref(false);

const count = ref(0);

const rowData = ref({});

const router = useRouter()

const editData = (row: any) => {
  rowData.value = row;
  router.push({
    name: "closedTasksDetail",
    query: {editType: 'detail', id: row.id}
  });
};


const queryList = () => {
  tableLoading.value = true;
  getClosedTasksList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    console.log("测试")
    console.log(tableData)
    console.log("测试")
    count.value = response.data.count;
  }).catch((error) => {
    ElMessage.error("获取闭环任务列表数据失败;请重试！");
  });
};

queryList();

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage;
  queryList();
};
</script>

<style lang="scss" scoped>
::v-deep {
  .el-input-number {
    .el-input__inner {
      text-align: left;
    }
  }
}

.el-tooltip__popper {
  max-width: 20%;
}

a {
  color: #1890ff;
  text-decoration: none;
  background-color: transparent;
  outline: none;
  cursor: pointer;
  transition: color .3s;
  -webkit-text-decoration-skip: objects;
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
