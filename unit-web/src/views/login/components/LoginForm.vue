<template>
  <el-form ref="ruleFormRef"
           :model="ruleForm"
           :rules="rules"
           label-width="0px"
           class="ant-form">
    <el-tabs v-model="activeName" :stretch="true">
      <el-tab-pane label="账号登录" name="first">
        <el-form-item label="" prop="username">
          <el-input
              placeholder="请输入用户名"
              autoComplete="on"
              style="position: relative"
              v-model="ruleForm.username"
              @keyup.enter.native="submitForm(ruleFormRef)"
          >
            <template #prefix>
              <el-icon class="el-input__icon"><UserFilled /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="" prop="password">
          <el-input
              placeholder="请输入密码"
              autoComplete="on"
              @keyup.enter.native="submitForm(ruleFormRef)"
              v-model="ruleForm.password"
              :type="passwordType"
          >
            <template #prefix>
              <el-icon class="el-input__icon"><GoodsFilled /></el-icon>
            </template>
            <template #suffix>
              <div class="show-pwd" @click="showPwd">
                <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"/>
              </div>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item style="width: 100%">
          <el-button
              :loading="loading"
              class="login-btn"
              type="primary"
              @click="submitForm(ruleFormRef)"
          >登录</el-button
          >
        </el-form-item>
      </el-tab-pane>
    </el-tabs>
  </el-form>
</template>
<script lang="ts" setup>
import {ref, reactive} from 'vue'
import type {FormInstance} from 'element-plus'
import {ElNotification} from "element-plus";
import {useRouter} from 'vue-router'
import {useUserStore} from "@/store/modules/user"
import {getTimeStateStr} from '@/utils/index'

const router = useRouter()
const UserStore = useUserStore()
const ruleFormRef = ref<FormInstance>()
const passwordType = ref('password')
const loading = ref(false)
const activeName = ref('first')

const rules = reactive({
  password: [{required: true, message: "请输入用户名", trigger: "blur"}],
  username: [{required: true, message: "请输入密码", trigger: "blur"}],
})

// 表单数据
const ruleForm = reactive({
  username: 'admin',
  password: '123456',
})

// 显示密码图标
const showPwd = () => {
  passwordType.value = passwordType.value === 'password' ? '' : 'password'
}

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      loading.value = true
      // 登录
      setTimeout(async () => {
        await UserStore.login(ruleForm)
        await router.push({
          path: '/',
        })
        ElNotification({
          title: getTimeStateStr(),
          message: "欢迎登录 EasyPost",
          type: "success",
          duration: 3000
        });
        loading.value = true
      }, 1000)
    } else {
      console.log('error submit!')
      return false
    }
  })
}
</script>

<style lang="scss" scoped>
@import "../index.scss";

.ant-form {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  color: rgba(0, 0, 0, .85);
  font-size: 13px;
  font-variant: tabular-nums;
  line-height: 1.5715;
  list-style: none;
  font-feature-settings: "tnum", "tnum";
}

</style>
