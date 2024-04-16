<template>
  <div class="app-container">
    <el-card>
      <div>
        <el-form :inline="true" :model="queryParams">
          <el-form-item style="float: right">
            <el-input
                :suffix-icon="Search"
                clearable
                v-model.trim="queryParams.name"
                placeholder="用例名称"
                @keyup.enter.native="queryList">
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <div>
        <el-table
            ref="revRef"
            :data="tableData"
            v-loading="tableLoading"
            element-loading-text="拼命加载中"
            :header-cell-style="{'background-color':'#ffffff','color':'#babac0' }"
            style="width: 100%"
        >
          <el-table-column type="expand">
            <template #default="props">
              <el-button
                  style="float: right;"
                  size="small" type="primary" round :loading="loading"
                  @click="debugFunc(props.row)" :icon="VideoPlay"
              >
                运行
              </el-button>
              <div v-for="(value, key) in props.row" :key="key">
                <div v-if="key.toString() === 'args_info'">
                  <div v-for="(index, args) in value" :key="index">
                    <el-form autoComplete="on" label-position="right" label-width="100px">
                      <el-form-item :prop="args" :label="args">
                        <el-input  style="width: 200px" size="small" v-model="state.funcArgs[args]" :placeholder=args>
                        </el-input>
                      </el-form-item>
                    </el-form>
                  </div>
                </div>
              </div>
              <div style="border: 1px solid #E6E6E6; margin-top: 35px">
                <mirror-code
                    style="height: 300px"
                    v-model="state.script_code"
                    :constModelData="state.script_code"
                    :editorConfig="state.editorConfig"
                >
                </mirror-code>
               </div>
            </template>
          </el-table-column>
          <el-table-column prop="func_name" label="函数名称"></el-table-column>
          <el-table-column prop="func_args" label="函数参数"></el-table-column>
          <el-table-column prop="func_doc" label="函数说明"></el-table-column>
          <el-table-column label="操作" width="150px" align="center">
            <template #default="scope">
              <el-button @click="debugHandler(scope.row)" type="primary" link>调试</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import {useRoute, useRouter} from "vue-router";
import {reactive, ref} from "vue";
import {Search, VideoPlay} from "@element-plus/icons-vue";
import {ElMessage, ElMessageBox} from "element-plus";
import {functionDetailList, functionDebug} from "@/api/setting";
import {showErrMessage} from "@/utils/element";
import MirrorCode from "@/components/MirrorCode/index.vue";

const revRef = ref()

const route = useRoute()

const router = useRouter()

const state = reactive({
  funcArgs: {},
  script_code: "",
  editorConfig: { language: 'python', theme: 'vs' },
})

const queryParams = reactive({
  id: '',
  name: ''
})

const loading = ref(false)

const tableLoading = ref(false)

const tableData = ref([])

const queryList = () => {
  tableLoading.value = true;
  queryParams.id = <string>route.query.id
  functionDetailList(queryParams).then((response) => {
    tableLoading.value = false;
    tableData.value = response.data.data;
  }).catch((error) => {
    ElMessage.error("获取内置函数数据失败;请重试！")
  })
}

const debugHandler = (row: any) => {
  revRef.value.toggleRowExpansion(row);
}

const debugFunc = (row: any) => {
  ElMessageBox.confirm(`确认运行该函数 - ${row.func_name}?`).then(_ => {
    functionDebug({
      id: router.currentRoute.value.query.id,
      func_name: row.func_name,
      args_info: state.funcArgs,
    }).then((response) => {
      const {data, code, msg} = response.data
      state.script_code = data.ret
      showErrMessage(code.toString(), msg)
    })
  }).catch(_ => {
    ElMessage.error("函数运行失败请重试");
  })
}

queryList()
</script>

<style lang="scss">
</style>