<template>
  <div class="app-container">
    <div class="header-container">
      <div class="card-head-title">
        <div class="card-description">
                    <span class="page-header-back-button el-icon-back" @click="goProjectList">
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
          <div style="text-align: center; margin-bottom: 24px; row-gap: 0;">
            <span class="avatar project-avatar-image">
              <el-upload
                  ref="uploadRefs"
                  :auto-upload="false"
                  :on-change="handleChange"
                  :show-file-list="false"
                  v-model:file-list="form.fileList"
              >
                <img v-if="imgDataUrl" :src="imgDataUrl" class="avatar" alt="">
                <el-icon v-else><Plus/></el-icon>
              </el-upload>
            </span>
          </div>
          <div style="padding-left: 400px">
            <el-form autoComplete="on" :model="form" :rules="rules" ref="ruleFormRef"
                     class="lk-form"
                     label-position="right"
                     label-width="100px"
            >
              <el-form-item label="项目名称" :required="true" prop="name">
                <el-input v-model="form.name" style="width: 350px;" placeholder="请输入项目名称"></el-input>
              </el-form-item>
              <el-form-item label="项目类型" :required="true" prop="type">
                <el-select type="type" v-model="form.type" v-loading="loading"
                           element-loading-spinner="el-icon-loading" clearable filterable>
                  <el-option v-for="item in type" :value="item" :key="null" style="font-size: 12px">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="项目描述" prop="desc">
                <el-input v-model="form.desc" style="width: 350px;"
                          :rows="2"
                          type="textarea"
                          placeholder="请输入项目描述">
                </el-input>
              </el-form-item>
              <el-form-item label="是否私有" :required="true" prop="private">
                <el-switch v-model="form.private"
                           :active-value="0"
                           :inactive-value="1">
                </el-switch>
              </el-form-item>
            </el-form>
            <div class="pull-right">
              <el-button :loading="loading" :icon="Collection" type="primary" @click="submitForm(ruleFormRef)">确
                认
              </el-button>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="成员列表" name="2">
          <div>
            <el-form :inline="true">
              <el-form-item>
                <el-button
                    :icon="Plus"
                    size="default"
                    type="primary"
                    icon="el-icon-plus"
                    @click="dialogVisible = true">
                  添加成员
                </el-button>
              </el-form-item>
            </el-form>
          </div>
          <div>
            <el-table :data="filterTableData" style="width: 100%">
              <el-table-column label="" prop="user.username">
                <template #default="scope">
                  <div style="margin-inline-end:16px;display:inline">
                    <img v-if="scope.row.user.avatar" :src="scope.row.user.avatar" class="avatar" alt="">
                  </div>
                  <div style="display:inline;color: rgba(0, 0, 0, 0.88);">
                    <span>{{ scope.row.user.username }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="" prop="rode_id">
                <template #default="scope">
                  <el-tag :type="scope.row.rode_id=='0'?'':'success'"
                  >{{ scope.row.rode_id == '0' ? '负责人' : '组员' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column align="right">
                <template #header>
                  <el-input v-model="search" size="small" placeholder="搜索用户名"/>
                </template>
                <template #default="scope">
                  <el-button v-show="scope.row.rode_id=='1'"
                             size="small"
                             type="danger"
                             :icon="Delete"
                             @click="handleDelete(scope.$index, scope.row)"
                  >
                  </el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <el-dialog
        v-model="dialogVisible"
        title="添加成员"
        width="30%"
    >
      <el-form autoComplete="on" :model="memberForm"
               label-position="right"
               label-width="100px">
        <el-form-item label="用户" :required="true" prop="user_id">
          <el-select
              class="selectOpt" v-model="memberForm.user_id" placeholder="请选择"
              :popper-append-to-body="false"
              style="width: 150px;"
          >
            <el-option
                v-for="item in userListData"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleAdd">
              确认
            </el-button>
          </span>
        </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import {ref, reactive, onMounted, watch, computed} from 'vue'
import {Back, Delete} from "@element-plus/icons-vue";
import {projectDetail, projectUpdate, projectRoleDelete, projectRoleAdd} from "@/api/project";
import {userList} from "@/api/user";
import {Collection, Plus} from "@element-plus/icons-vue";
import {useRouter} from "vue-router";
import {showErrMessage} from "@/utils/element";
import {ElMessage, ElMessageBox, FormInstance} from "element-plus";
import type {UploadInstance} from 'element-plus'

const search = ref('')

const dialogVisible = ref(false)

const tableData = reactive([])

const activeName = ref("1")

const type = ref([
  'Web',
  'App',
  'Pc',
  'MiniProgram'
])

const projectName = ref("")

const ruleFormRef = ref<FormInstance>()

const uploadRefs = ref<UploadInstance>()

const imgDataUrl = ref("")

const userListData = ref([])

let form = reactive<any>({
  name: '',
  avatar: '',
  type: '',
  desc: '',
  private: 1,
  fileList: []
})

const memberForm = reactive({
  user_id: ''
})

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入项目名称！"}],
  type: [{required: true, trigger: "blur", message: "请选择项目类型！"}],
  private: [{required: true, trigger: "blur", message: "请选择项目是否私有！"}]
})

const loading = ref(false)

const router = useRouter()

const goProjectList = () => {
  router.push({
    name: "projectList",
  })
}

onMounted(() => {
  const pk = router.currentRoute.value.query.id
  projectDetail({id: pk}).then(res => {
    const {code, data, msg} = res.data
    projectName.value = data.name
    form.name = data.name;
    form.type = data.type;
    form.desc = data.desc;
    form.private = data.private
    form.avatar = imgDataUrl.value = data.avatar
    tableData.push(...data.roles)
  }).catch(res => {
    console.log(res);
  });

  userList({}).then(res => {
    let ret = res.data.results
    for (let i = 0; i < ret.length; i++) {
      userListData.value.push({
        "label": ret[i]["username"],
        "value": ret[i]["id"]
      })
    }
  }).catch(res => {
    console.log(res)
  })
})

const submitForm = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      form["id"] = router.currentRoute.value.query.id
      form.avatar = form.fileList[0] != null ? form.fileList[0].raw : URL.revokeObjectURL(form.avatar)
      const ret = await projectUpdate(form)
      const {code, data, msg} = ret.data
      showErrMessage(code.toString(), msg)
    } else {
      console.log('error submit!')
      ElMessage.error("项目更新失败请重试!")
      return false
    }
  })
}

const handleChange = (rawFile: any) => {
  if (rawFile.raw.type !== 'image/jpeg') {
    ElMessage.error('Avatar picture must be JPG format!')
    return false
  } else if (rawFile.raw.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  imgDataUrl.value = URL.createObjectURL(rawFile.raw!)
  return true
}

const handleDelete = (index: number, row: any) => {
  ElMessageBox.confirm(`确认删除成员权限 - ${row.user.username}?`).then(_ => {
    projectRoleDelete({
      "project_id": row.project,
      "user_id": row.user.id
    }).then((response) => {
      const {data, code, msg} = response.data
      tableData.splice(index, 1)
      showErrMessage(code.toString(), msg)
    })
  }).catch(_ => {
    ElMessage.error("删除成员权限失败请重试");
  })
}

const handleAdd = () => {
  const pk = router.currentRoute.value.query.id
  projectRoleAdd({
    "project_id": pk,
    "user_id": memberForm.user_id,
    "roles": 1
  }).then((response) => {
    const {data, code, msg} = response.data
    if(data){
      tableData.push(data)
    }
    showErrMessage(code.toString(), msg)
    dialogVisible.value = false
  }).catch(_ => {
    ElMessage.error("添加成员权限失败请重试");
  })
}

const filterTableData = computed(() =>
    tableData.filter(
        (data) =>
            !search.value ||
            data.user.username.toLowerCase().includes(search.value.toLowerCase())
    )
)

watch(tableData, (newName, oldName) => {
  console.log(`tableData ${newName} -> ${oldName}`)
})
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
