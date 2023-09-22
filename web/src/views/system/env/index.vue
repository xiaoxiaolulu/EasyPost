<template>
  <div class="app-container">
    <div class="container">
      <div>
        <el-form :inline="true" :model="queryParams" ref="queryParams">
          <el-form-item>
            <el-button
                type="primary"
                icon="el-icon-plus"
                @click="">
              创建环境
            </el-button>
          </el-form-item>
          <el-form-item prop="name" style="float: right">
            <el-input prefix-icon="el-icon-search"
                      clearable type="name"
                      v-model.trim="queryParams.name"
                      placeholder="请输入项目名称"
                      @keyup.enter.native="queryList"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData"
                border
                v-loading="tableLoading"
                element-loading-text="拼命加载中"
                style="width: 100%">
        <el-table-column type="index" width="55" label="id"></el-table-column>
        <el-table-column prop="name" label="环境名称"></el-table-column>
        <el-table-column prop="desc" label="备注"></el-table-column>
        <el-table-column prop="user.username" label="创建者"></el-table-column>
        <el-table-column prop="create_time" label="创建日期">
          <template slot-scope="scope">
            <span>{{ parseTime(scope.row.create_time) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template slot-scope="scope">
            <el-button @click="" type="text">编辑</el-button>
            <el-button @click="" type="text">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--分页组件-->
      <el-pagination
          style="margin-top: 8px;"
          @current-change="queryList"
          :current-page.sync="queryParams.page"
          :page-size="20"
          :total="count"
          layout="->, total, prev, pager, next, jumper">
      </el-pagination>
    </div>
    <!--        <add-dialog v-model="addDialogVisible" :dialogData="rowData"></add-dialog>-->
    <!--        <edit-dialog v-model="editDialogVisible" :dialogData='rowData'></edit-dialog>-->
  </div>
</template>

<script lang="ts" setup>
import {ref, reactive} from 'vue'
import {envList, envDelete} from "@/api/setting";
import {parseTime} from "@/utils";

const queryParams = reactive({
  name: '',
  page: 1
})

const loading = ref(false)

const tableData = ref(null)

const tableLoading = ref(false)

const count = ref(null)

const rowData = ref(null)

const addDialogVisible = ref(false)

const editDialogVisible = ref(false)
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
