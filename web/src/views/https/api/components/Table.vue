<template>
  <div class="m-user-table">
    <div class="header">
      <el-form :inline="true" :model="queryParams">
        <el-form-item style="float: right">
          <el-input
              :suffix-icon="Search"
              clearable
              v-model.trim="queryParams.name"
              placeholder="请输入接口名称"
              @keyup.enter.native="queryList">
          </el-input>
        </el-form-item>
      </el-form>
    </div>
    <div class="footer">
      <div class="util">
        <el-button type="primary" @click="add">
          <el-icon>
            <Plus/>
          </el-icon>
          新建接口
        </el-button>
      </div>
      <div class="table-inner">
        <el-table
            v-loading="loading"
            :data="tableData" style="width: 100%;height: 100%" border>
          <el-table-column type="index" label="序号" width="80" fixed/>
          <el-table-column prop="name" label="接口名称" align="center" width="200" fixed>
          </el-table-column>
          <el-table-column prop="method" label="请求方式" align="center" width="150">
            <template #default="scope">
              <el-tag v-show="tag.name === scope.row.method" v-for="tag in methods" :key="tag.id">
                {{ scope.row.method }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" align="center" width="180">
            <template #default="scope">
              <div v-show="tag.id === scope.row.status" v-for="tag in tags" :key="tag.id">
                <span :class="`status-${tag.status}`"></span>
                <span>&nbsp;&nbsp;{{ tag.name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="user.username" label="创建人" align="center" width="180"/>
          <el-table-column prop="create_time" label="创建时间" width="200">
            <template #default="scope">
              <span>{{ parseTime(scope.row.create_time) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="operator" label="操作" width="200px" align="center" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" icon="Edit" @click="editHandler(scope.row)">
                编辑
              </el-button>
              <el-button @click="del(scope.row)" type="danger" size="small" icon="Delete">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="pagination">
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

  </div>
</template>
<script lang="ts" setup>
import {ElMessageBox, ElMessage, FormInstance, ElPagination} from 'element-plus'
import {Search, Plus} from '@element-plus/icons-vue'
import {onMounted, reactive, ref} from 'vue'
import {useRouter} from "vue-router";
import {getHttpList} from "@/api/http";
import {parseTime} from "@/utils";


const tableData = ref([])
const dialogVisible = ref(false)
const ruleFormRef = ref<FormInstance>()
const loading = ref(true)
const currentPage1 = ref(1)
const router = useRouter()
const currentProject = ref()
const nodeId = ref()


const queryParams = reactive({
  name: '',
  page: 1,
  project: '',
  node: ''
})

const count = ref(0)

const tags =  reactive([
  { id: 0, name: '调试中', status: 'debug' },
  { id: 1, name: '已废弃', status: 'discard'},
  { id: 2, name: '正常' , status: 'normal'}
])

const methods = reactive([
  { id: 0, type: 'primary', name: 'POST' },
  { id: 1, type: 'success', name: 'GET' },
  { id: 2, type: 'warning', name: 'PUT' },
  { id: 3, type: 'danger', name: 'DELETED' }
])

const reset = (formEl: FormInstance | undefined) => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 1000)
}

const queryList = () => {
  getHttpList(queryParams).then((response) => {
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    console.log(error.response)
    ElMessage.error("获取接口列表数据失败;请重试！")
  })
}

const getList = (data) => {
  currentProject.value = data.currentProject
  nodeId.value = data.node
  queryParams.project = data.currentProject
  queryParams.node = data.node
  loading.value = true
  queryList()

  setTimeout(() => {
    loading.value = false
  }, 500)
}

const add = () => {
  let node = nodeId.value
  let project = currentProject.value
  if (node && project) {
    router.push({
      name: "httpDetail",
      query: {editType: 'save', project: project, node: node}
    });
  } else {
    ElMessage.error("项目未选择或未选择相关目录树节点, 无法添加接口!");
  }
}

const editHandler = (row) => {
  let node = nodeId.value
  let project = currentProject.value
  if (node && project) {
    router.push({
      name: "httpDetail",
      query: {editType: 'update', project: project, node: node, id: row.id}
    });
  } else {
    ElMessage.error("项目未选择或未选择相关目录树节点, 无法编辑接口!");
  }
}

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
}

const del = (row) => {
  ElMessageBox.confirm('你确定要删除当前项吗?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
    draggable: true,
  })
      .then(() => {
      })
      .catch(() => {
      })
}
const changeStatus = (row) => {
  ElMessageBox.confirm(
      `确定要${!row.status ? '禁用' : '启用'} ${row.username} 账户吗？`,
      '温馨提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      },
  )
      .then(async () => {
      })
      .catch(() => {
        row.status = !row.status
      })
}

const handleSizeChange = (val: number) => {
  console.log(`${val} items per page`)
}

const handleCurrentChange = (val: number) => {
  currentPage1.value = val
}

onMounted(() => {
  setTimeout(() => {
    loading.value = false
  }, 1000)
})

defineExpose({
  getList
})
</script>
<style lang="scss" scoped>
@import "../index";

.status-debug {
  position: relative;
  background-color: #1890ff;
  top: -1px;
  display: inline-block;
  width: 6px;
  height: 6px;
  vertical-align: middle;
  border-radius: 50%;
  animation: fade 600ms infinite;
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
