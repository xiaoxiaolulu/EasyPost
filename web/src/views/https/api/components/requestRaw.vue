<template>
  <el-form :inline="true" label-width="50px" size="small" label-position="right" ref="requestFormRef">
    <div style="border-bottom: 1px solid #E6E6E6; display: flex; justify-content: space-between">
      <div class="request-mode">
        <el-radio-group
            size="small"
            v-model="mode"
            @change="radioChange"
        >
          <el-radio label="none">none</el-radio>
          <el-radio label="form_data">form-data</el-radio>
          <el-radio label="x_www_form_urlencoded">x-www-form-urlencoded</el-radio>
          <el-radio label="raw">raw</el-radio>
          <el-dropdown @command="handleLanguage"
                       trigger="click"
                       v-if="mode === 'raw'"
                       placement="bottom-start">
              <span class="el-button--text">
                {{ state.language }}
                <el-icon class="el-icon--right">
                  <arrowDown/>
                </el-icon>
              </span>
            <template #dropdown>
              <el-dropdown-menu style="width: 150px">
                <el-dropdown-item v-for="language in state.languageList" :key="language" :command="language">
                  {{ language }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-radio-group>
      </div>
    </div>

    <!--没有请求体-->
    <div v-if="mode === 'none'" style="text-align: center; padding-top: 10px">
      <span style="color: darkgray">该请求暂时没有正文</span>
    </div>

    <!--form-data-->
    <div v-if="mode === 'form_data'" style="text-align: center; padding-top: 10px">
      <el-table :data="state.formData" style="width: 100%" row-key="id" border size="small" :show-header="false">
        <el-table-column label="参数名" width="160px" prop="name">
          <template #default="scope">
            <el-input
                size="small"
                clearable
                placeholder="请输入参数名"
                :value="scope.row.name"
                v-model.trim="scope.row.name"
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column label="参数值" width="160px" prop="value">
          <template #default="scope">
            <el-input
                size="small"
                clearable
                placeholder="请输入参数值"
                :value="scope.row.value"
                v-model.trim="scope.row.value"
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column label="请选择类型" prop="type">
          <template #default="scope">
            <el-select
                size="small"
                clearable
                :placeholder="`请选择`"
                v-model="scope.row.type"
            >
              <el-option
                  v-for="ite in type"
                  :key="ite.value"
                  :label="ite.label"
                  :value="ite.value"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="参数描述" prop="value">
          <template #default="scope">
            <el-input
                size="small"
                clearable
                placeholder="请输入参数描述"
                :value="scope.row.description"
                v-model.trim="scope.row.description"
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="operator" label="操作" width="300px" fixed="right">
          <template #default="scope">
            <el-popover
                trigger="click"
                v-model:visible="scope.row.visible"
                placement="top"
                :width="160"
                size="small"
            >
              <p style="display: flex; align-items: center; margin-bottom: 10px">
                <el-icon color="#faad14" style="margin-right: 10px"><warning-filled /></el-icon>
                删除此行？</p
              >
              <div style="text-align: right; margin: 0">
                <el-button size="small" @click="scope.row.visible = false">取消</el-button>
                <el-button size="small" type="primary" @click="deleteFormAction(scope)"
                >确定</el-button
                >
              </div>
              <template #reference>
                <el-button icon="Delete" @click="deleteFormCurrent(scope.row)" type="danger" size="small"
                >删除</el-button
                >
              </template>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 15px">
        <el-button style="width: 100%" @click="addFormData" size="small">
          <el-icon style="margin-right: 4px"><plus /></el-icon> 添加一行数据</el-button
        >
      </div>
    </div>

    <!--x_www_form_urlencoded-->
    <div v-if="mode === 'x_www_form_urlencoded'" style="text-align: center; padding-top: 10px">
      <el-table :data="state.x_www_form_urlencoded" style="width: 100%" row-key="id" border size="small" :show-header="false">
        <el-table-column label="参数名" width="160px" prop="name">
          <template #default="scope">
            <el-input
                size="small"
                clearable
                placeholder="请输入参数名"
                :value="scope.row.name"
                v-model.trim="scope.row.name"
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column label="参数值" width="160px" prop="value">
          <template #default="scope">
            <el-input
                size="small"
                clearable
                placeholder="请输入参数值"
                :value="scope.row.value"
                v-model.trim="scope.row.value"
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column label="请选择类型" prop="type">
          <template #default="scope">
            <el-select
                size="small"
                clearable
                :placeholder="`请选择`"
                v-model="scope.row.type"
            >
              <el-option
                  v-for="ite in type"
                  :key="ite.value"
                  :label="ite.label"
                  :value="ite.value"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="参数描述" prop="value">
          <template #default="scope">
            <el-input
                size="small"
                clearable
                placeholder="请输入参数描述"
                :value="scope.row.description"
                v-model.trim="scope.row.description"
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column prop="operator" label="操作" width="300px" fixed="right">
          <template #default="scope">
            <el-popover
                trigger="click"
                v-model:visible="scope.row.visible"
                placement="top"
                :width="160"
                size="small"
            >
              <p style="display: flex; align-items: center; margin-bottom: 10px">
                <el-icon color="#faad14" style="margin-right: 10px"><warning-filled /></el-icon>
                删除此行？</p
              >
              <div style="text-align: right; margin: 0">
                <el-button size="small" @click="scope.row.visible = false">取消</el-button>
                <el-button size="small" type="primary" @click="delete3wFormAction(scope)"
                >确定</el-button
                >
              </div>
              <template #reference>
                <el-button icon="Delete" @click="delete3wFormCurrent(scope.row)" type="danger" size="small"
                >删除</el-button
                >
              </template>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 15px">
        <el-button style="width: 100%" @click="add3wFormData" size="small">
          <el-icon style="margin-right: 4px"><plus /></el-icon> 添加一行数据</el-button
        >
      </div>
    </div>

    <!--raw-->
    <div v-show="mode === 'raw'">
      <mirror-code
          style="height: 420px"
          ref="rawRef"
          v-model="state.rawData"
          :constModelData="state.rawData"
          :editorConfig="state.editorConfig"
      >
      </mirror-code>
    </div>
  </el-form>
</template>

<script setup lang="ts">
import {reactive, ref, watch} from "vue";
import {ArrowDown} from '@element-plus/icons-vue'
import MirrorCode from "@/components/MirrorCode/index.vue";

const emit = defineEmits(['updateContentType'])

const mode = ref('none')

const state = reactive({
  // formData
  formData: [],
  // x_www_form_urlencoded
  x_www_form_urlencoded: [],
  // raw
  rawData: "",
  language: 'json',
  languageList: ['json', 'text', 'xml', 'html'],
  //monaco
  lang: 'json',
  editorConfig: { language: 'json', theme: 'vs' }
});

const rawRef = ref()

const type = [
  {
    value: 'Boolean',
    label: 'Boolean',
  },
  {
    value: 'Date',
    label: 'Date',
  },
  {
    value: 'Number',
    label: 'Number',
  },
  {
    value: 'Float',
    label: 'Float',
  },
  {
    value: 'Integer',
    label: 'Integer',
  },
  {
    value: 'String',
    label: 'String',
  }
]

const addFormData = (row) => {
  let obj = {name: "", value: "", description: ""};
  state.formData.push(obj);
}

const deleteFormAction = (scope) => {
  scope.row.visible = false
  state.formData.splice(scope.$index, 1)
}

const deleteFormCurrent = (row) => {
  // pass
}

const add3wFormData = (row) => {
  let obj = {name: "", value: "", description: ""};
  state.x_www_form_urlencoded.push(obj);
}

const delete3wFormAction = (scope) => {
  scope.row.visible = false
  state.formData.splice(scope.$index, 1)
}

const delete3wFormCurrent = (row) => {
  // pass
}

const setData = (data) => {
  let modeObj = Object.keys(data)[0]
  mode.value = (modeObj == 'none' || modeObj == 'form_data' || modeObj == 'x_www_form_urlencoded')?modeObj:'raw'
  if (!data) return
    if (mode.value === 'form_data'){
      if (data) {
        for (let i = 0; i < data['form_data'].length; i++) {
          state.formData.push(data['form_data'][i])
        }
      } else {
        state.formData = []
      }
    }
    if (mode.value === 'x_www_form_urlencoded'){
      if (data){
        for (let i = 0; i < data['x_www_form_urlencoded'].length; i++) {
          state.x_www_form_urlencoded.push(data['x_www_form_urlencoded'][i])
        }
      }else{
        state.x_www_form_urlencoded = []
      }
    }
    if (mode.value === 'raw') {
      state.rawData = data[Object.keys(data)[0]]
      state.language = Object.keys(data)[0]
    }
}

const radioChange = (value: any) => {
  mode.value = value
  updateContentType(value === 'none' || value === 'form_data')
}

const getData = () => {
  let requestData = {
  }
  if (mode.value  === 'raw') {
    requestData['json'] = state.rawData
  }
  if (mode.value === 'form_data') {
    requestData['form_data'] = state.formData
  }
  if (mode.value === 'x_www_form_urlencoded') {
    requestData['x_www_form_urlencoded'] = state.x_www_form_urlencoded
  }
  if (mode.value === 'none') {
    requestData['data'] = {}
  }
  return requestData
}

const handleLanguage = (language: any) => {
  state.language = language
  updateContentType()
}


const updateContentType = (remove = false) => {
  emit('updateContentType', mode.value, state.language, remove)
}

watch(() => state.rawData, (val) => {
      if (val) {
        updateContentType()
      } else {
        updateContentType(true)
      }
    }, {
      deep: true
    }
);

defineExpose({
  setData,
  getData
})
</script>


<style scoped lang="scss">
.request-mode {
  margin-bottom: 10px;

  :deep(.el-radio__label) {
    font-size: 13px;
  }
}
</style>