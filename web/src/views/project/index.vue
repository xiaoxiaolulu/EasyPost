<template>
  <div class="app-container">
    <div class="header-body">
      <el-form :inline="true" :model="queryParams">
        <el-form-item>
          <el-button
              type="primary"
              icon="el-icon-plus"
              @click="addProject">
            创建项目
          </el-button>
        </el-form-item>
        <el-form-item style="float: right">
          <el-input
              :suffix-icon="Search"
              clearable
              v-model.trim="queryParams.name"
              placeholder="请输入项目名称"
              @keyup.enter.native="queryList">
          </el-input>
        </el-form-item>
      </el-form>
    </div>
    <div>
      <el-row>
        <el-col :span="6" v-for="(item) in tableData" :key="item.id">
          <div style="width: 95%; margin-top: 20px; margin-left: 5px; cursor: pointer">
            <el-card shadow="hover">
              <!--            <el-card shadow="hover" @click.native="editProject(item)">-->
              <div class="card-meta-avatar">
                <span class="avatar avatar-image">
                                      <img :src=item.avatar alt="">
                                    </span>
              </div>
              <div class="card-detail">
                <div class="card-title">
                  <div style="font-size: 16px; font-weight: bold; color: rgb(65, 74, 105);">
                    {{ item.name }}
                    <el-dropdown style="float: right; color: #b6c1d0">
                      <el-icon>
                        <component :is="More"/>
                      </el-icon>
                      <template #dropdown>
                        <el-dropdown-menu size="mini">
                          <el-dropdown-item @click.native="deleteProjectData(item)">
                            <template #default="scope">
                              <el-icon style="color: red">
                                <component :is="Delete"/>
                              </el-icon>
                              <span>删除项目</span>
                            </template>
                          </el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </div>
                <div class="card-description">{{ item.desc }}</div>
                <div class="card-description">负责人：
                  <span style="color:rgb(22, 119, 255)">{{ item.user.username }}</span>
                </div>
                <div class="card-description">更新时间：{{ parseTime(item.create_time) }}</div>  
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
    <el-pagination
        style="margin-top: 8px;"
        v-model:currentPage="queryParams.page"
        :page-size="20"
        layout=">, total, prev, pager, next, jumper"
        :total="count"
        @current-change="handlePageChange">
    </el-pagination>
    <add-dialog v-model="isShow"  @onChangeDialog="onChangeDialog"/>
  </div>
</template>

<script lang="ts" setup>
import {ref, reactive} from 'vue'
import {projectList, projectDelete} from "@/api/project";
import {ElMessage, ElMessageBox, ElPagination} from "element-plus";
import {useRouter} from "vue-router";
import {parseTime} from "@/utils";
import {More, Delete, Search} from "@element-plus/icons-vue";
import addDialog from './components/addDialog.vue'
import {showErrMessage} from "@/utils/element";


const isShow = ref(false);

const addProject = () => {
  isShow.value = true;
};
const onChangeDialog = (val: any) => {
  isShow.value = false;
  queryList()
};

const queryParams = reactive({
  name: '',
  page: 1
})

const router = useRouter()

const rowData = ref(null)

const tableLoading = ref(false)

const tableData = ref(null)

const count = ref(0)

const handlePageChange = (newPage: any) => {
  queryParams.page = newPage
  queryList()
}

const queryList = () => {
  tableLoading.value = true;
  projectList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.results;
    count.value = response.data.count;
  }).catch((error) => {
    // console.log(error.response)
    ElMessage.error("获取项目列表数据失败;请重试！")
  })
}

queryList()

const editProject = (row: any) => {
  rowData.value = row;
  router.push({
    name: "project/detail",
    query: {id: row.id}
  });
}

const deleteProjectData = (row: any) => {
  ElMessageBox.confirm(`确认删除项目数据 - ${row.name}?`).then(_ => {
    projectDelete({id: row.id}).then((response) => {
      const {data, code, msg} = response.data
      showErrMessage(code.toString(), msg)
      queryList();
    })
  }).catch(_ => {
    ElMessage.error("项目删除失败请重试");
  })
}

</script>

<style scoped lang="scss">

.crud-opts {
  padding: 4px 0;
  display: -webkit-flex;
  display: flex;
  align-items: center;
  margin-bottom: 10px;

  .crud-opts-right {
    margin-left: auto;
  }
}

.el-tooltip__popper {
  max-width: 20%;
}

.date-item {
  height: 28px !important;
  width: 230px !important;
}

.card-meta-avatar {
  float: left;
  padding-right: 16px
}

.avatar {
  box-sizing: border-box;
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
  border-radius: 50%;
}

.avatar-image {
  background: transparent;
  width: 48px;
  height: 48px;
  line-height: 48px;
  font-size: 18px;

  img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.card-detail {
  overflow: hidden;
}

.card-description {
  font-size: 13px;
  color: rgba(0, 0, 0, .45);
  margin-top: 15px;
  clear: both
}

:deep(:focus-visible) {
  outline: none;
}
</style>
