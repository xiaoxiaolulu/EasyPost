<template>
  <div class="app-container">
    <div class="header-container">
      <div class="card-head-title">
        <div class="card-description">
          <span style="display: inline-block" class="el-icon-back" @click="goBack">
                      <el-icon>
                        <component :is="Back"/>
                      </el-icon>
                    </span>
<!--          <span style="display: inline-block" class="page-header-heading-title">-->
<!--            {{ route.query.editType === 'update' ? "更新" : "新增" }}-->
<!--          </span>-->
          <span style="display: inline-block; float: right">
            <el-dropdown :hide-on-click="false" style="margin-right: 10px">
              <el-button type="warning" size="small">
              添加步骤
              <el-icon class="el-icon--right">
                <arrowDown/>
              </el-icon>
            </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item v-for="(value, key)  in state.optTypes"
                                      :key="key"
                                      style="margin: 5px 0"
                                      :style="{ color: getStepTypeInfo(key,'color')}"
                                      @click="handleAddData(key)">
                      <i :class="getStepTypeInfo(key,'icon')" class="fab-icons"
                         :style="{color:getStepTypeInfo(key,'color')}"></i>
                      {{ value }}
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
            </el-dropdown>
            <el-button type="success" @click="" size="small">调试</el-button>
            <el-button type="primary" @click="" class="title-button" size="small">保存</el-button>
          </span>
        </div>
      </div>
    </div>
    <div class="container">
    </div>
  </div>
</template>

<script setup lang="ts">
import {ArrowDown, ArrowUp, Back} from "@element-plus/icons-vue";
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, reactive, ref, watch, nextTick} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {saveOrUpdate, runApi, getHttpDetail} from "@/api/http";
import {showErrMessage} from "@/utils/element";
import {getStepTypesByUse, getStepTypeInfo} from '@/utils/index'

const route = useRoute()
const router = useRouter()

const ruleFormRef = ref<FormInstance>()

const ruleForm = reactive({
})

const priority = ref([{
  value: 0,
  label: "P0"
}, {
  value: 1,
  label: "P1"
}, {
  value: 2,
  label: "P2"
}, {
  value: 3,
  label: "P3"
}, {
  value: 4,
  label: "P4"
}])


const stepControllerRef = ref()

const state = reactive({
  optTypes: getStepTypesByUse("case"),
})

const handleAddData = (optType) => {
  stepControllerRef.value.handleAddData(optType)
}

const goBack = () => {
  router.push({
    name: "apis",
  })
}

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入接口名称！"}],
})

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      try{
      } catch (e) {
        console.log(e)
      }

    } else {
      console.log('error submit!')
      ElMessage.error("新增接口失败请重试!")
      return false
    }
  })
}

onMounted(() => {
})

defineExpose({
})

</script>
<style lang="scss">
.page-header-back-button {
  text-decoration: none;
  outline: none;
  transition: color .3s;
  color: #000;
  cursor: pointer;
  margin-right: 16px;
  font-size: 15px;
  line-height: 1;
}

.page-header-heading-title {
  margin-right: 12px;
  margin-bottom: 0;
  color: rgba(0, 0, 0, .85);
  font-weight: 600;
  font-size: 14px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis
}


.method-color-get {
  color: #61affe
}

.method-color-post {
  color: #49cc90
}

.method-color-delete {
  color: #f93e3d
}

.method-color-put {
  color: #fca130
}

.method-color-na {
  color: #f56c6c
}

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

.api-body {
  margin-top: 20px;
}

.custom-table .cell{
  font-size: 12px;
  color: #7a8b9a;
}
</style>
