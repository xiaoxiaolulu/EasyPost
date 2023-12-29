<template>
  <div class="app-container">
    <div class="header-container">
      <div class="card-head-title">
        <div class="card-description">
          <span class="el-icon-back" @click="goBack">
            <el-icon>
              <component :is="Back"/>
            </el-icon>
          </span>
          <span class="page-header-heading-title">
            {{ route.query.editType === 'update' ? "更新" : "新增" }}
          </span>
        </div>
      </div>
    </div>
    <div class="container">
      <el-row :gutter="12">
        <el-col :span="8">
          <el-card style="height:100%;min-height: 600px;overflow:scroll;">
            <template #header>
              <div>
                <span style="margin-right:8px;color: #7a8b9a"><el-icon><component :is="Odometer"/></el-icon></span>
                <span style="font-size: 18px; color: #7a8b9a">用例配置</span>
              </div>
            </template>
            <div>
              <el-form :inline="true" autoComplete="on" :model="state.form" :rules="rules" ref="ruleFormRef"
                       label-width="auto"
                       label-position="top"
                       size="small"
              >
                <el-form-item label="用例名称：" prop="name">
                  <el-input v-model.trim="state.form.name"
                            style="width: 100%;"
                            size="small"
                            placeholder="请输入用例名称"></el-input>
                </el-form-item>
                <el-form-item label="优先级：" prop="priority">
                  <el-select v-model="state.form.priority" filterable placeholder="请选择接口当前状态" size="small">
                    <el-option
                        v-for="item in priority"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="描述：" prop="">
                  <el-input v-model.trim="state.form.remarks"
                            style="width: 100%;"
                            size="small"
                            placeholder="请输入用例描述"></el-input>
                </el-form-item>
              </el-form>
              <el-button type="success" @click="" size="small">调试</el-button>
              <el-button type="primary" @click="" size="small">保存</el-button>
            </div>
          </el-card>
        </el-col>
        <el-col :span="16">
          <el-card style="height:100%;min-height: 600px;overflow:scroll;">
            <template #header>
              <div>
                <span style="font-size: 18px; color: #7a8b9a">用例步骤</span>
              </div>
            </template>
            <div>
              <div style="margin-top: 15px">
                <el-dropdown :hide-on-click="false" style="width: 100%">
                  <el-button size="small" style="width: 100%">
                    <el-icon style="margin-right: 4px"><plus /></el-icon> 添加步骤
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
              </div>
            </div>
            <step
                ref="stepControllerRef"
                use_type="case"
                style="margin-bottom: 10px"
                v-model="state.form.step_data">
            </step>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ArrowDown, ArrowUp, Back, Odometer} from "@element-plus/icons-vue";
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, reactive, ref, watch, nextTick} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {saveOrUpdate, runApi, getHttpDetail} from "@/api/http";
import {showErrMessage} from "@/utils/element";
import {getStepTypesByUse, getStepTypeInfo} from '@/utils/index'
import Step from "@/views/https/case/components/step.vue";

const route = useRoute()
const router = useRouter()

const ruleFormRef = ref<FormInstance>()

const createForm = () => {
  return {
    name: '',
    remarks: '',
    priority: '',
    step_data: []
  }
}

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
  form: createForm()
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
