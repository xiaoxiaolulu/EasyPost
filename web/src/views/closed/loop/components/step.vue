<template>
  <el-dialog title="场景详情"
             v-model="isShow"
             :show-close="false"
             class="stepWidth">
    <el-card style="height: 100%">
      <template #header><h4 class="suite-filename">场景：{{ state.scene_name }}</h4></template>
      <ul style="list-style-type: none">
        <li v-for="(item, index) in state.steps" :key="index">
          <span style="display: inline-block">
              <i class="material-icons md-18 test-icon test-pass">
                <el-icon :style="{'color': item.color}">
                  <component :is="item.status" />
                </el-icon>
              </i>
              <i class="test-title">{{ item.step }}
              </i>
          </span>
        </li>
        <div class="test-body-wrap">
          <div class="test-body">
            <pre class="test-code-snippet hljs">{{ state.err_msg }}</pre>
          </div>
        </div>
        <div class="test-context">
          <div class="test-context-item">
            <a :href="state.err_png" class="test-image-link" rel="noopener noreferrer" target="_blank">
              <img :src="state.err_png" class="test-image"></a>
          </div>
        </div>
      </ul>
    </el-card>
    <!--    <div class="pull-right">-->
    <!--      <el-button type="primary" @click="onSureClick(ruleFormRef)">确 认</el-button>-->
    <!--      <el-button @click="isShow = false">取 消</el-button>-->
    <!--    </div>-->
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive, computed } from "vue";
import { FormInstance } from "element-plus";
import { ElMessage } from "element-plus";
import { showErrMessage } from "@/utils/element";

const propsCxt: any = null;

const props = defineProps({
  modelValue: {
    default: propsCxt,
    type: [Object, Boolean]
  }
});

const emits = defineEmits(["update:modelValue", "onChangeDialog"]);


const iconName = computed(() => {
  // switch (status.value) {
  //   case 'success':
  //     return 'el-icon-check';
  //   case 'warning':
  //     return 'el-icon-warning';
  //   case 'error':
  //     return 'el-icon-close';
  //   default:
  //     return ''; // 或者默认图标
  // }
});
let form = reactive({
  name: "",
  type: "",
  desc: "",
  private: ""
});

const ruleFormRef = ref<FormInstance>();

const rules = reactive({
  name: [{ required: true, trigger: "blur", message: "请输入项目名称！" }],
  type: [{ required: true, trigger: "blur", message: "请选择项目类型！" }],
  desc: [{ required: true, trigger: "blur", message: "请输入项目描述！" }]
});

const isShow = computed({
  get() {
    return props.modelValue;
  },
  set(val) {
    emits("update:modelValue", val);
  }
});

const state = ref({
  steps: []
});

const setData = (rowdata) => {
  state.value = rowdata ? rowdata : "";
  console.log("测试");
  console.log(state.value);
  state.value.steps = eval(rowdata.steps);
  console.log("xxx");
  console.log(rowdata.err_msg);
};

// const onSureClick = (formName: FormInstance | undefined) => {
//   if (!formName) return
//   formName.validate(async (valid) => {
//     if (valid) {
//       const ret = await projectCreate(form)
//       const {code, data, msg} = ret.data
//       emits('onChangeDialog', true);
//       showErrMessage(code.toString(), msg)
//       formName.resetFields()
//     } else {
//       console.log('error submit!')
//       ElMessage.error("项目新增失败请重试!")
//       return false
//     }
//   })
// }
defineExpose({
  setData
});
</script>

<style lang="scss">
.stepWidth {
  width: 80%;
  height: 80%
}

.pull-right {
  float: right;
}

.material-icons {
  display: inline-block;
  font-family: Material Icons;
  font-weight: 400;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-feature-settings: "liga";
  font-feature-settings: "liga";
}

.material-icons.md-18 {
  font-size: 18px;
}

.test-icon {
  -webkit-align-self: flex-start;
  align-self: flex-start;
  padding: 3px;
  border-radius: 50%;
  color: #fff;
  margin-right: 16px;
}

.test-icon.test-pass {
  color: #c8e6c9;
  color: var(--green100);
  background-color: #4caf50;
  background-color: var(--green500);
}

.suite-filename {
  color: rgba(0, 0, 0, .54);
  color: var(--black54);
  font-family: var(--font-family--regular);
  margin: 6px 0 0;
}

.test-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  -webkit-flex-grow: 1;
  flex-grow: 1;
  font-family: var(--font-family--regular);
  font-size: 13px;
  line-height: 24px;
  margin: 0;
  padding-right: 12px;
  text-align: left;
}

.test-body-wrap {
  border-left: 3px solid transparent;
  transition: border-color .2s ease-out;
}

.test-body {
  background-color: #fafafa;
  border: 1px solid #eceff1;
  border: 1px solid var(--grey50);
  border-radius: 4px;
}

.test-code-snippet {
  font-size: 13px;
  margin: 0;
  border-radius: 0;
}

.hljs {
  overflow-x: auto;
  padding: .5em;
  color: #383a42;
  background: #fafafa;
}

.test-context {
  background-color: #fff;
  border-top: 1px solid #eceff1;
  border-top: 1px solid var(--grey50);
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  height: 200px;
  width: 200px;
}

.test-context-item {
  padding-top: 11px;
}

.test-image-link {
  display: inline-block;
  font-size: 11px;
  padding: 0 1em 1em;
}

.test-image {
  display: block;
  max-width: 100%;
  height: auto;
}
</style>
