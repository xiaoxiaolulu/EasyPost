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
              <span style="padding-right: 10px;">{{ route.query.editType === 'update' ? "更新" : "新增" }}</span>
            </template>
          </CardHeader>
        </div>
      </div>
    </div>
    <div class="container">
      <el-card>
        <template #header>
          <div>
            <strong>基本信息</strong>
          </div>
        </template>
        <el-form :inline="true" autoComplete="on" :model="ruleForm" :rules="rules" ref="ruleFormRef"
                 label-width="auto"
                 label-position="right">
          <el-row>
            <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
              <el-form-item label="环境名称" prop="name" :required="true">
                <el-input
                    style="width: 500px"
                    size="default"
                    v-model="ruleForm.name"
                    placeholder="请输入请求路径"
                >
                </el-input>
              </el-form-item>
<!--              <el-form-item label="环境地址" prop="host" :required="true">-->
<!--                <el-input-->
<!--                    style="width: 500px"-->
<!--                    size="default"-->
<!--                    v-model="ruleForm.host"-->
<!--                    placeholder="请输入请求路径"-->
<!--                >-->
<!--                </el-input>-->
<!--              </el-form-item>-->
              <div style="margin-bottom: 20px">
                <el-button  size="default" type="primary" link style="margin-left:10px" id="closeSearchBtn" @click="closeSetting">
                  {{ settings }}
                  <el-icon v-if="showSetting">
                    <ArrowUp/>
                  </el-icon>
                  <el-icon v-else>
                    <ArrowDown/>
                  </el-icon>
                </el-button>
              </div>
              <el-form-item label="描述" prop="" v-show="showSetting">
                <el-input size="default"
                          type="textarea"
                          v-model.trim="ruleForm.remarks"
                          style="width: 500px;"
                          placeholder="请输入用例描述"></el-input>
              </el-form-item>
            </el-col>
            <el-col :xs="6" :sm="6" :md="6" :lg="6" :xl="6">
              <div style="padding-left: 12px">
                <el-button size="default" type="primary" @click="onSureClick(ruleFormRef)">保存</el-button>
              </div>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
      <el-card style="margin-top: 20px">
        <template #header>
          <div>
            <strong>配置信息</strong>
          </div>
        </template>
        <div>
          <el-tabs v-model="activeName" style="overflow-y: auto">
            <el-tab-pane name='AddressSetting'>
              <template #label>
                <strong>服务</strong>
              </template>
              <div>
                <address-setting ref="AddressSettingRef"></address-setting>
              </div>
            </el-tab-pane>
            <el-tab-pane name='VariablePoolSetting'>
              <template #label>
                <strong>变量池</strong>
              </template>
              <div>
                <variable-pool ref="VariablePoolRef"></variable-pool>
              </div>
            </el-tab-pane>
            <el-tab-pane name='DbSetting'>
              <template #label>
                <strong>数据库配置</strong>
              </template>
              <div>
                <database-setting ref="DatabaseSettingRef"></database-setting>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
    </div>
  </div>
</template>
<script setup lang="ts">
import CardHeader from "@/components/CardHeader/index.vue";
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, reactive, ref} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {ArrowDown, ArrowUp} from "@element-plus/icons-vue";
import VariablePool from "@/views/system/env/components/VariablePool.vue";
import DatabaseSetting from "@/views/system/env/components/DatabseSetting.vue"
import {envSaveOrUpdate, getEnvDetail} from "@/api/setting";
import {showErrMessage} from "@/utils/element";
import AddressSetting from "@/views/system/env/components/addressSetting.vue";

const route = useRoute()

const router = useRouter()

const VariablePoolRef = ref()

const DatabaseSettingRef = ref()

const AddressSettingRef = ref()

const ruleForm = reactive({
  name: '',
  server: '',
  variables: [],
  remarks: '',
  data_source: []
})

const state = reactive({
  environment_id: 0
})

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入名称环境！"}]
})

const ruleFormRef = ref<FormInstance>()

const showSetting = ref(false)

const activeName =  ref('AddressSetting')

const goBack = () => {
  router.push({name: 'env'})
}

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    ruleForm.variables = VariablePoolRef.value.getData()
    ruleForm.data_source = DatabaseSettingRef.value.getData()
    ruleForm.server = AddressSettingRef.value.getData()
    if (valid) {
      try{
        let formData = {
          id: state.environment_id,
          name: ruleForm.name,
          server: ruleForm.server,
          remarks: ruleForm.remarks,
          variables: ruleForm.variables,
          data_source: ruleForm.data_source
        }
        const ret = await envSaveOrUpdate(formData)
        const {code, data, msg} = ret.data
        state.environment_id = data.environment_id
        showErrMessage(code.toString(), msg)
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

const init = () => {
  let environment_id = route.query.id
  if(environment_id){
    state.environment_id = environment_id
  }
  console.log("api_id------>", environment_id)
  if (environment_id) {
    getEnvDetail({id: environment_id}).then((response) => {
      const {data, code, msg} = response.data
      VariablePoolRef.value.setData(data.variables)
      DatabaseSettingRef.value.changeAction(data.data_source)
      AddressSettingRef.value.setData(data.server)
      ruleForm.name = data.name
      ruleForm.remarks = data.desc
      showErrMessage(code.toString(), msg)
    })
  }
}

const settings = computed(() => {
  if (showSetting.value == false) {
    return "更多设置";
  } else {
    return "收起设置";
  }
})

const closeSetting = () => {
  showSetting.value = !showSetting.value
}

onMounted(() => {
  init()
})
</script>
<style scoped lang="scss">

</style>