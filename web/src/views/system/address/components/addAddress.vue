<template>
    <el-dialog title="新增地址"
               v-model="isShow.show"
               :show-close="false"
               class="addressWidth">
        <el-form autoComplete="on" :model="form" :rules="rules" ref="ruleFormRef"
                 label-position="right"
                 label-width="100px">
            <el-form-item label="环境" :required="true" prop="env">
                <el-select
                        class="selectOpt" v-model="form.env" placeholder="请选择"
                        :popper-append-to-body="false"
                        style="width: 150px;"
                >
                    <el-option
                            v-for="item in isShow.envList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="地址名称" :required="true" prop="name">
                <el-input v-model="form.name" placeholder="请输入地址名称"></el-input>
            </el-form-item>
            <el-form-item label="服务地址" :required="true" prop="host">
                <el-input v-model="form.host" placeholder="请输入服务名称">></el-input>
            </el-form-item>
        </el-form>
        <div class="pull-right">
          <el-button type="primary" @click="onSureClick(ruleFormRef)">确 认</el-button>
          <el-button @click="isShow.show = false">取 消</el-button>
        </div>
    </el-dialog>
</template>

<script lang="ts" setup>

import {computed, reactive, ref} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {addressCreate} from "@/api/setting";
import {showErrMessage} from "@/utils/element";

const emits = defineEmits(['update:modelValue', 'onChangeDialog'])

const props = defineProps({
  modelValue: {
    type: [Object, Boolean],
    default:() =>{
    }
  },
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
  env: '',
  host: '',
})

const ruleFormRef = ref<FormInstance>()

const rules = reactive({
  name: [{required: true, trigger: "blur", message: "请输入环境名称！"}],
  env: [{required: true, trigger: "blur", message: "请输选择环境！"}],
  host: [{required: true, trigger: "blur", message: "请输入服务地址！"}],
})


const onSureClick = (formName: FormInstance | undefined) => {
  if (!formName) return
  formName.validate(async (valid) => {
    if (valid) {
      const ret = await addressCreate(form)
      const {code, data, msg} = ret.data
      emits('onChangeDialog', true);
      showErrMessage(code.toString(), msg)
      formName.resetFields()
    } else {
      console.log('error submit!')
      ElMessage.error("地址新增失败请重试!")
      return false
    }
  })
}
</script>

<style lang="scss">
    .addressWidth {
        width: 30%;
        height: 40%
    }

    .pull-right {
        float: right;
    }
</style>
