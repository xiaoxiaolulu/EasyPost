<template>
  <div>
    <div class="container">
      <div>
        <el-form :inline="true" :model="queryParams" ref="queryParams">
          <el-form-item>
            <el-button
                type="primary"
                icon="el-icon-plus"
                @click="addAddress">
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
        <el-table-column type="index" width="55" label="序号"></el-table-column>
        <el-table-column prop="env" label="环境">
          <template slot-scope="scope">
            <el-tag type="info">{{ scope.row.env }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="地址名称"></el-table-column>
        <el-table-column prop="host" label="服务地址">
          <template slot-scope="scope">
            <a :href="scope.row.host" target="_blank">{{ scope.row.host | ellipsis }}</a>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template slot-scope="scope">
            <el-button @click="editAddress(scope.row)" type="text">编辑</el-button>
            <el-button @click="deleteAddress(scope.row)" type="text">删除</el-button>
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
import {reactive, ref} from "vue";

const queryParams = reactive({
  name: '',
  page: 1
})

const envCollections = reactive([])

const loading = ref(false)

const tableData = reactive([])

const tableLoading = ref(false)

const count = ref(0)

const rowData = ref({})

const addDialogVisible = ref(false)

const editDialogVisible = ref(false)

const ellipsis = (value: string) => {
  if (!value) {
    return "";
  }
  if (value.length > 35) {
    return value.slice(0, 35) + "...";
  } else {
    return value;
  }
}
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
</style>
