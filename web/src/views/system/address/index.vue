<template>
  <div class="app-container">
    <div class="container">
      <div>
        <el-form :inline="true" :model="queryParams">
          <el-form-item>
            <el-button
                type="primary"
                :icon="Plus"
                @click="addAddress">
              添加地址
            </el-button>
          </el-form-item>
          <el-form-item style="float: right">
            <el-input
                :suffix-icon="Search"
                clearable
                v-model.trim="queryParams.name"
                placeholder="请输入地址名称"
                @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData"
                v-loading="tableLoading"
                element-loading-text="拼命加载中"
                style="width: 100%">
        <el-table-column prop="env" label="环境">
          <template #default="scope">
            <el-tag type="info">{{ scope.row.env.name}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="地址名称"></el-table-column>
        <el-table-column prop="host" label="服务地址">
          <template #default="scope">
            <a :href="scope.row.host" target="_blank">{{ scope.row.host }}</a>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template #default="scope">
            <el-button @click="editAddress(scope.row)" type="primary" link>编辑</el-button>
            <el-button @click="deleteAddressData(scope.row)" type="primary" link>删除</el-button>
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
    <address-dialog ref="dialog" :row-data="rowData" @queryList="queryList"/>
  </div>
</template>

<script lang="ts" setup>
import {reactive, ref} from "vue";
import {Plus, Search} from "@element-plus/icons-vue";
import {addressList, addressDelete, envList} from "@/api/setting";
import {ElMessage, ElMessageBox, ElPagination} from "element-plus";
import addressDialog from"./components/addressDialog.vue"
import {showErrMessage} from "@/utils/element";

const queryParams = reactive({
  name: '',
  page: 1
})

const loading = ref(false)

const tableData = ref(null)

const tableLoading = ref(false)

const count = ref(0)

const rowData = ref({})

const envOption = ref([])

const dialog = ref(null)

const editAddress = (row: any) => {
  row["envList"] = envOption.value
  rowData.value = row
  dialog.value.show(row)
};

const addAddress = () => {
  rowData.value["envList"] = envOption.value
  rowData.value["treeData"] = tableData.value
  dialog.value.show(rowData)
};

const queryList = () => {
  tableLoading.value = true;
  addressList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    // console.log(error.response)
    ElMessage.error("获取地址列表数据失败;请重试！")
  })
}

queryList()

const getEnvList = () => {
  envList({}).then((res) => {
    let envList= res.data.results;
    for (let i = 0; i < envList.length; i++) {
      envOption.value.push({
        "label": envList[i]["name"],
        "value": envList[i]["id"]
      })
    }
  }).catch((error) => {
    ElMessage.error("获取环境列表数据失败")
  })
}

getEnvList()

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
}

const deleteAddressData = (row: any) => {
  ElMessageBox.confirm(`确认删除地址数据 - ${row.name}?`).then(_ => {
    addressDelete({id: row.id}).then((response) => {
      const {data, code, msg} = response.data
      showErrMessage(code.toString(), msg)
      queryList();
    })
  }).catch(_ => {
    ElMessage.error("地址删除失败请重试");
  })
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
