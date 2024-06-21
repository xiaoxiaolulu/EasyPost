<template>
  <div class="app-container">
    <div class="header-container">
      <div class="card-head-title">
        <div class="card-description">
          <CardHeader
            style="margin: 5px 0;"
            @back="goBack"
          >
            <template #content>
              <span style="padding-right: 10px;">闭环任务处理</span>
            </template>
          </CardHeader>
        </div>
      </div>
    </div>
    <div class="container">
      <el-table
        :data="tableData"
        :header-cell-style="{ color: '#adaaaa', fontSize: '13px', fontWeight: 'bold'}"
        border
      >
        <el-table-column prop="id" label="序号" width="55" />
        <el-table-column prop="func_name" label="功能名称"/>
        <el-table-column prop="scene_name" label="场景名称"/>
        <el-table-column prop="err_step" label="异常步骤"/>
        <el-table-column prop="err_type" label="异常类型"/>
        <el-table-column prop="handler" label="异常原因"/>
        <el-table-column prop="cause" label="处理人"/>
        <el-table-column label="操作" width="150px" align="center">
          <template #default="scope">
            <el-button type="primary" link>查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, reactive} from 'vue'
import {Delete} from "@element-plus/icons-vue";
import { getClosedTasksDetail} from "@/api/http";
import {useRoute, useRouter} from "vue-router";
import {ElMessage, FormInstance} from "element-plus";
import type {UploadInstance} from 'element-plus'
import CardHeader from '@/components/CardHeader/index.vue'

const tableData = reactive([])

const loading = ref(false)

const router = useRouter()

const route = useRoute()

const queryList = () => {
  const pk = router.currentRoute.value.query.id
  getClosedTasksDetail({id: pk}).then((response) => {
   tableData.push(...response.data.data.task)
  }).catch((error) => {
    ElMessage.error("获取闭环任务详情数据失败;请重试！");
  });
};

queryList()

const goBack = () => {
  router.push({name: 'projectList'})
}

</script>

<style lang="scss">

.pull-right {
  float: right;
}

.card-head-title {
  border-radius: 4px 4px 0 0;
  min-height: 48px;
}

.card-description {
  float: left;
}

.project-avatar-image {
  background: transparent;
  width: 96px !important;
  height: 96px !important;
  line-height: 48px;
  font-size: 18px;

  img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
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
