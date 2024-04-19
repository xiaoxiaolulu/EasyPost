<template>
  <div class="app-container">
    <div class="container">
      <div>
        <el-form :inline="true" :model="queryParams">
          <el-form-item>
            <el-button
                type="primary"
                :icon="Plus"
                @click="add">
              创建
            </el-button>
          </el-form-item>
          <el-form-item style="float: right">
            <el-input
                :suffix-icon="Search"
                clearable
                v-model.trim="queryParams.database"
                placeholder="请输入数据库名称"
                @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData"
                v-loading="tableLoading"
                element-loading-text="拼命加载中"
                @selection-change="handleSelectionChange"
                style="width: 100%">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="database" label="数据库名称"></el-table-column>
        <el-table-column prop="host" label="地址"></el-table-column>
        <el-table-column prop="port" label="端口"></el-table-column>
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
            <span>{{parseTime(scope.row.update_time)}}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template #default="scope">
            <el-button @click="editData(scope.row)" type="primary" link>编辑</el-button>
            <el-button @click="deleteData(scope.row)" type="primary" link>删除</el-button>
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
    <database-dialog ref="dialog" @queryList="queryList"/>
  </div>
</template>

<script lang="ts" setup>
import {reactive, ref} from "vue";
import {Plus, Search} from "@element-plus/icons-vue";
import {databaseDelete, databaseList} from "@/api/setting";
import {ElMessage, ElMessageBox, ElPagination} from "element-plus";
import databaseDialog from "./components/databaseDialog.vue"
import {showErrMessage} from "@/utils/element";
import {parseTime} from "@/utils";

const queryParams = reactive({
  database: '',
  page: 1
})

const loading = ref(false)

const tableData = ref(null)

const tableLoading = ref(false)

const count = ref(0)

const rowData = ref({})

const dialog = ref(null)

const selectionData = ref()

const editData = (row: any) => {
  rowData.value = row
  dialog.value.show(row)
};

const add = () => {
  rowData.value["treeData"] = tableData.value
  dialog.value.show(rowData)
};

const queryList = () => {
  tableLoading.value = true;
  databaseList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    // console.log(error.response)
    ElMessage.error("获取地址列表数据失败;请重试！")
  })
}

queryList()

const handleSelectionChange = (val: any) => {
  selectionData.value = val
}

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
}

const deleteData = (row: any) => {
  ElMessageBox.confirm(`确认删除数据库数据 - ${row.name}?`).then(_ => {
    databaseDelete({id: row.id}).then((response) => {
      const {data, code, msg} = response.data
      showErrMessage(code.toString(), msg)
      queryList();
    })
  }).catch(_ => {
    ElMessage.error("数据库删除失败请重试");
  })
}

const getData = () => {
  return selectionData.value
}

defineExpose({
  getData
})
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
