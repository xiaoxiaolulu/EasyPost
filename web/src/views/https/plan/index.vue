<template>
  <div class="app-container">
    <div class="container">
      <div>
        <el-form :inline="true" :model="queryParams">
          <el-form-item>
            <el-button
                type="primary"
                :icon="Plus"
                @click="addPlan">
              添加计划
            </el-button>
          </el-form-item>
          <el-form-item style="float: right">
            <el-input
                :suffix-icon="Search"
                clearable
                v-model.trim="queryParams.name"
                placeholder="请输入计划名称"
                @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData"
                v-loading="tableLoading"
                element-loading-text="拼命加载中"
                style="width: 100%">
        <el-table-column type="index" width="55" label="id"></el-table-column>
        <el-table-column prop="name" label="测试计划名称"></el-table-column>
        <el-table-column prop="priority" label="优先级">
          <template #default="scope">
            <el-tag v-show="tag.id === scope.row.priority" v-for="tag in planPriority" :key="tag.id" :type="tag.type">
              {{ tag.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cron" label="cron表达式"></el-table-column>
        <el-table-column prop="state" label="状态">
          <template #default="scope">
            <div v-show="tag.id === scope.row.state" v-for="tag in planState" :key="tag.id">
              <span :class="`status-${tag.status}`"></span>
              <span>&nbsp;&nbsp;{{ tag.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="user.username" label="创建者">
          <template #default="scope">
            <div style="margin-inline-end:16px;display:inline">
              <img v-if="scope.row.user.avatar" :src="scope.row.user.avatar" class="avatar" alt="">
            </div>
            <div style="display:inline;color: rgba(0, 0, 0, 0.88);">
              <span style="color:rgb(22, 119, 255)">{{ scope.row.user.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="更新日期">
          <template #default="scope">
            <span>{{ parseTime(scope.row.update_time) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template #default="scope">
            <el-button @click="edit(scope.row)" type="primary" link>编辑</el-button>
            <el-button @click="deleteData(scope.row)" type="primary" link>删除</el-button>
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
import {Plus, Search} from "@element-plus/icons-vue";
import {ref, reactive} from 'vue'
import {useRouter} from "vue-router";
import {parseTime} from "@/utils";
import {ElMessage, ElMessageBox, ElPagination} from "element-plus";
import {showErrMessage} from "@/utils/element";
import {planList, deletePlan} from "@/api/http";

const queryParams = reactive({
  name: '',
  page: 1
})

const router = useRouter()

const loading = ref(false)

const tableData = ref(null)

const tableLoading = ref(false)

const count = ref(0)

const isShow = ref(false);

const editShow = ref(false);

const rowData = ref({})

const planPriority = reactive([
  { id: 0, type: 'primary', name: 'P0' },
  { id: 1, type: 'success', name: 'P1' },
  { id: 2, type: 'warning', name: 'P2' },
  { id: 3, type: 'danger', name: 'P3' },
  { id: 4, type: 'danger', name: 'P4' },
])

const planState =  reactive([
  { id: 0, name: '停止', status: 'discard'},
  { id: 1, name: '运行' , status: 'normal'}
])

const addPlan = () => {
  router.push({
    name: "planDetail",
    query: {editType: 'save'}
  });
};

const edit = (row: any) => {
  if (row) {
    router.push({
      name: "planDetail",
      query: {editType: 'updatePlan', planId: row.id}
    });
  } else {
    ElMessage.error("编辑计划异常请重试!");
  }
};

const onChangeDialog = (val: any) => {
  isShow.value = false;
  editShow.value = false;
  queryList()
};

const queryList = () => {
  tableLoading.value = true;
  planList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    console.log(error)
    ElMessage.error("获取计划列表数据失败;请重试！😿")
  })
}

queryList()

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
}

const deleteData = (row: any) => {
  ElMessageBox.confirm(`确认删除计划数据 - ${row.name}?`).then(_ => {
    deletePlan({id: row.id}).then((response) => {
      const {data, code, msg} = response.data
      showErrMessage(code.toString(), msg)
      queryList();
    })
  }).catch(_ => {
    ElMessage.error("计划删除失败请重试");
  })
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

.status-discard {
  position: relative;
  background-color: #d92911;
  top: -1px;
  display: inline-block;
  width: 6px;
  height: 6px;
  vertical-align: middle;
  border-radius: 50%;
  animation: fade 600ms infinite;
}

.status-normal {
  position: relative;
  background-color: #83f106;
  top: -1px;
  display: inline-block;
  width: 6px;
  height: 6px;
  vertical-align: middle;
  border-radius: 50%;
  animation: fade 600ms infinite;
}
</style>
