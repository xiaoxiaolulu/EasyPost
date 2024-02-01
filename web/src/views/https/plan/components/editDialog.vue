<template>
  <el-dialog title="编辑环境"
             v-model="isShow"
             :show-close="false"
             center
             class="envWidth">
    <el-form autoComplete="on" :model="form" :rules="rules" ref="ruleFormRef"
             label-position="right"
             label-width="100px">
      <el-form-item label="环境名称" :required="true" prop="name">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="备注" prop="desc">
        <el-input v-model="form.desc" style="width: 350px;"
                  :rows="2"
                  type="textarea">
        </el-input>
      </el-form-item>
    </el-form>
    <div class="pull-right">
      <el-button type="primary" @click="onSureClick(ruleFormRef)">确 认</el-button>
      <el-button @click="isShow = false">取 消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import {ref, reactive, computed, watch} from 'vue'
import {ElMessage, FormInstance} from "element-plus";
import {envUpdate} from "@/api/setting";
import {showErrMessage} from "@/utils/element";

const propsCxt: any = null

const emits = defineEmits(['update:modelValue', 'onChangeDialog'])

const props = defineProps({
  modelValue: {
    default: propsCxt,
    type: [Object, Boolean]
  },
  rowData: {
    type: Object,
    default: () => {
    }
  }
})

const isShow = computed({
  get() {
    return props.modelValue;
  },
  set(val) {
    emits('update:modelValue', val);
  }
});


let form = reactive({
  name: '',
  desc: '',
})

const ruleFormRef = ref<FormInstance>()

const pk = ref()

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入项目名称！"}],
})

const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      form["id"] = pk.value
      const ret = await envUpdate(form)
      const {code, data, msg} = ret.data
      emits('onChangeDialog', true);
      showErrMessage(code.toString(), msg)
      formName.resetFields()
    } else {
      console.log('error submit!')
      ElMessage.error("环境编辑失败请重试!")
      return false
    }
  })
}

watch(() => props.rowData, () => {
  form.name = props.rowData.name
  form.desc = props.rowData.desc
  pk.value = props.rowData.id
}, {deep: true, immediate: true})

</script>

<style lang="scss">
.envWidth {
  width: 30%;
  height: 35%
}

.pull-right {
  float: right;

}
</style>
