<template>
    <el-dialog title="新增地址"
               v-model="isShow"
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
                            v-for="item in envOption"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="地址名称" :required="true" prop="name">
                <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="服务地址" :required="true" prop="host">
                <el-input v-model="form.host"></el-input>
            </el-form-item>
        </el-form>
        <div class="pull-right">
          <el-button type="primary" @click="onSureClick(ruleFormRef)">确 认</el-button>
          <el-button @click="isShow = false">取 消</el-button>
        </div>
    </el-dialog>
</template>

<script lang="ts" setup>

import {computed, reactive, ref} from "vue";
import {ElMessage, FormInstance} from "element-plus";
import {addressCreate, envList} from "@/api/setting";
import {showErrMessage} from "@/utils/element";

const propsCxt: any = null

const emits = defineEmits(['update:modelValue', 'onChangeDialog'])

const props = defineProps({
  modelValue: {
    default: propsCxt,
    type: [Object, Boolean]
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
  env: '',
  host: '',
})

const envOption = ref([])

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

const queryList = () => {
  envList({}).then((res) => {
    let envList= res.data.results;
    for (let i = 0; i < envList.length; i++) {
      envOption.value.push({
        "label": envList[i]["name"],
        "value": envList[i]["id"]
      })
    }
  }).catch((error) => {
    // console.log(error.response)
    ElMessage.error("获取环境列表数据失败")
  })
}

queryList()
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
