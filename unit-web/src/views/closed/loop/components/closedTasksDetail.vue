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
        <el-table-column prop="func_name" label="功能名称">
          <template #default="scope">
            {{ellipsis(scope.row.func_name, 15, 20)}}
          </template>
        </el-table-column>
        <el-table-column prop="scene_name" label="场景名称">
          <template #default="scope">
            {{ellipsis(scope.row.scene_name, 15, 20)}}
          </template>
        </el-table-column>
        <el-table-column prop="err_step" label="异常步骤" width="290">
          <template #default="scope">
          <span style="display: inline-block">
            <el-icon style="color: red; margin-right: 5px">
              <WarningFilled />
            </el-icon>
            {{ellipsis(scope.row.err_step, 15, 30)}}
          </span>
          </template>
        </el-table-column>
        <el-table-column prop="err_type" label="异常类型" width="100">
          <template #default="scope">
            <el-tag type="danger">
              {{ scope.row.err_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cause" label="异常原因"/>
        <el-table-column prop="handler" label="处理人" width="100"/>
        <el-table-column label="操作" width="150px" align="center">
          <template #default="scope">
            <el-button type="primary" link  @click="handle(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <step  ref="stepRef" v-model="isShow"  @onChangeDialog="onChangeDialog"/>
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
import { ellipsis } from "@/utils";
import Step from "@/views/closed/loop/components/step.vue";

const tableData = reactive([])

const stepRef = ref()

const loading = ref(false)

const router = useRouter()

const route = useRoute()

const rowData = ref({})


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

const isShow = ref(false);

const handle = (row: any) => {
  rowData.value = row
  isShow.value = true;
  stepRef.value.setData(row)
};

const onChangeDialog = (val: any) => {
  isShow.value = false;
  queryList()
};

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
</style>
