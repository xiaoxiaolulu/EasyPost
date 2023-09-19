<template>
  <div class="app-container">
    <div class="header-container">
      <div class="card-head-title">
        <div class="card-description">
                    <span class="page-header-back-button el-icon-back" @click="">
                      <el-icon>
                        <component :is="Back"/>
                      </el-icon>
                    </span>
          <span class="page-header-heading-title">{{ projectName }}</span>
        </div>
      </div>
    </div>
    <div class="container">
      <el-tabs v-model="activeName" @tab-click="">
        <el-tab-pane label="项目设置" name="1">
          <div style="text-align: center; margin-bottom: 24px; row-gap: 0px;">
                                <span class="avatar project-avatar-image">
<!--                                    <myUpload-->
                                  <!--                                            v-model="show"-->
                                  <!--                                            @crop-success="cropSuccess"-->
                                  <!--                                            @crop-upload-success="cropUploadSuccess"-->
                                  <!--                                            @crop-upload-fail="cropUploadFail"-->
                                  <!--                                            :headers="headers"-->
                                  <!--                                            field="avatar"-->
                                  <!--                                            :url="imgUrl"-->
                                  <!--                                            method="PUT"-->
                                  <!--                                            langType='zh'-->
                                  <!--                                            :noRotate='false'-->
                                  <!--                                    />-->
                                  <!--                                <img v-if="AvatarType" :src="formData.avatar != null ? formData.avatar : Avatar"-->
                                  <!--                                     title="点击上传头像"-->
                                  <!--                                     class="avatar" @click="toggleShow" alt="">-->
                                  <!--                                <img v-if="!AvatarType" :src="imgDataUrl != null ? imgDataUrl : Avatar" class="avatar"-->
                                  <!--                                     @click="toggleShow" alt="">-->
                                </span>
          </div>
          <div style="padding-left: 400px">
            <el-form autoComplete="on" :model="formData" :rules="resetRules" ref="formData"
                     class="lk-form"
                     label-position="right"
                     label-width="100px"
            >
              <el-form-item label="项目名称" :required="true" prop="name">
                <el-input v-model="form.name" style="width: 350px;"></el-input>
              </el-form-item>
              <el-form-item label="项目类型" :required="true" prop="type">
                <el-select type="type" v-model="form.type" v-loading="loading"
                           element-loading-spinner="el-icon-loading" clearable filterable>
                  <el-option v-for="item in type" :value="item" :key="null" style="font-size: 12px">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="项目描述" :required="true" prop="desc">
                <el-input v-model="form.desc" style="width: 350px;"></el-input>
              </el-form-item>
            </el-form>
            <div class="pull-right">
              <el-button :loading="loading" class="el-icon-receiving" type="primary" @click="submitForm('form')">确
                认
              </el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, reactive} from 'vue'
import {Back} from "@element-plus/icons-vue";

const show = ref(false)

const AvatarType = ref(true)

const imgUrl = ref(null)

const imgDataUrl = ref(null)

const activeName = ref("1")

const type = ref([
  'Web',
  'App',
  'Pc',
  'MiniProgram'
])

const projectName = ref("3333")

let form = reactive({
  name: '',
  type: '',
  desc: ''
})


const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入项目名称！"}],
  type: [{required: true, trigger: "blur", message: "请选择项目类型！"}],
  desc: [{required: true, trigger: "blur", message: "请输入项目描述！"}]
})

const loading = ref(false)

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

.page-header-heading-title {
  margin-right: 12px;
  margin-bottom: 0;
  color: rgba(0, 0, 0, .85);
  font-weight: 600;
  font-size: 19px;
  line-height: 32px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis
}

.page-header-back-button {
  text-decoration: none;
  outline: none;
  transition: color .3s;
  color: #000;
  cursor: pointer;
  margin-right: 16px;
  font-size: 16px;
  line-height: 1;
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
