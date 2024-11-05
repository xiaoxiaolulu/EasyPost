<template>
  <el-dialog title="新增项目"
             v-model="isShow"
             :show-close="false"
             center class="proWidth">
    <el-form autoComplete="on" :model="form" :rules="rules" ref="ruleFormRef"
             label-position="right"
             label-width="100px">
      <el-form-item label="项目名称" :required="true" prop="name">
        <el-input v-model="form.name" placeholder="请输入项目名称"></el-input>
      </el-form-item>
      <el-form-item label="项目类型" :required="true" prop="type">
        <el-select type="type" v-model="form.type"
                   element-loading-spinner="el-icon-loading" clearable filterable>
          <el-option v-for="item in type" :value="item" :key="null" style="font-size: 12px">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="项目描述" :required="true" prop="desc">
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
      <el-button type="primary" @click="onSureClick(ruleFormRef)">确 认</el-button>
      <el-button @click="isShow = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import {ref, reactive, computed} from 'vue'
import {projectCreate} from "@/api/project";
import {FormInstance} from "element-plus";
import {ElMessage} from "element-plus";
import {showErrMessage} from "@/utils/element";

const propsCxt: any = null

const props = defineProps({
  modelValue: {
    default: propsCxt,
    type: [Object, Boolean]
  }
})

const emits = defineEmits(['update:modelValue', 'onChangeDialog'])

const type = ref([
  'Web',
  'App',
  'Pc',
  'MiniProgram'
])

let form = reactive({
  name: '',
  type: '',
  desc: '',
  private: ''
})

const ruleFormRef = ref<FormInstance>()

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入项目名称！"}],
  type: [{required: true, trigger: "blur", message: "请选择项目类型！"}],
  desc: [{required: true, trigger: "blur", message: "请输入项目描述！"}]
})

const isShow = computed({
  get() {
    return props.modelValue;
  },
  set(val) {
    emits('update:modelValue', val);
  }
});

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      const ret = await projectCreate(form)
      const {code, data, msg} = ret.data
      emits('onChangeDialog', true);
      showErrMessage(code.toString(), msg)
      formName.resetFields()
    } else {
      console.log('error submit!')
      ElMessage.error("项目新增失败请重试!")
      return false
    }
  })
}
</script>

<style lang="scss">
.proWidth {
  width: 30%;
  height: 50%
}

.pull-right {
  float: right;
}
</style>
