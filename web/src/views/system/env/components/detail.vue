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
              <el-form-item label="环境地址" prop="name" :required="true">
                <el-input
                    style="width: 500px"
                    size="default"
                    v-model="ruleForm.name"
                    placeholder="请输入请求路径"
                >
                </el-input>
              </el-form-item>
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
                <el-button type="primary" @click="onSureClick(ruleFormRef)">保存</el-button>
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
            <el-tab-pane name='VariablePoolSetting'>
              <template #label>
                <strong>变量池</strong>
              </template>
              <div>
              </div>
            </el-tab-pane>
            <el-tab-pane name='DbSetting'>
              <template #label>
                <strong>数据库配置</strong>
              </template>
              <div>
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
import {computed, reactive, ref} from "vue";
import {FormInstance} from "element-plus";
import {ArrowDown, ArrowUp} from "@element-plus/icons-vue";

const route = useRoute()

const router = useRouter()

const ruleForm = reactive({
  name: "",
  remarks: ""
})

const rules = reactive({
})

const ruleFormRef = ref<FormInstance>()

const showSetting = ref(false)

const activeName =  ref('VariablePoolSetting')

const goBack = () => {
  router.push({name: 'env'})
}

const onSureClick = (formName: FormInstance | undefined) => {

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
</script>
<style scoped lang="scss">

</style>