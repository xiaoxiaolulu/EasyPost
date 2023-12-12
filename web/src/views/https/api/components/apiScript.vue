<template>
  <el-row>
    <el-col :span="20">
      <div style="border: 1px solid #E6E6E6">
        <mirror-code
            style="height: 500px"
            v-model="state.script_code"
            :constModelData="state.script_code"
            :editorConfig="state.editorConfig"
        >
        </mirror-code>
      </div>
    </el-col>

    <el-col :span="4">
      <div style="padding: 8px;">
        <div>代码片段</div>
        <div v-for="menu in sideMenu" :key="menu.label">
          <el-button type="primary" link @click="handlerCode(menu)">{{ menu.label }}</el-button>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script setup name="apiCode">
import {reactive, computed} from 'vue';
import MirrorCode from "@/components/MirrorCode/index.vue";

const props = defineProps({
  useType: {
    type: String,
    default: () => {
    }
  }
})

const state = reactive({
  script_code: "",
  editorConfig: { language: 'python', theme: 'vs' },
  menuList: [],
  setupMenu: [
    {label: "设置一个环境变量", content: "ep.save_env_variable('name', 'value')"},
    {label: "获取一个环境变量", content: "ep.get_env_variable('name')"},
    {label: "获取当前环境的url", content: "ep.get_pre_url()"},
    {label: "设置全局环境变量", content: "ep.save_global_variable('name', 'value')"},
    {label: "删除临时变量", content: "ep.delete_env_variable('name')"},
    {label: "删除全局变量", content: "ep.delete_global_variable('name')"},
  ],
  teardownMenu: [
    {label: "设置一个环境变量", content: "ep.save_env_variable('name', 'value')"},
    {label: "获取一个环境变量", content: "ep.get_env_variable('name')"},
    {label: "获取当前环境的url", content: "ep.get_pre_url()"},
    {label: "设置全局环境变量", content: "ep.save_global_variable('name', 'value')"},
    {label: "删除临时变量", content: "ep.delete_env_variable('name')"},
    {label: "删除全局变量", content: "ep.delete_global_variable('name')"},
  ]
});

const handlerCode = (row) => {
  state.script_code = state.script_code ? state.script_code + `\n${row.content}` : row.content
}

// init code
const setData = (script_code) => {
  state.script_code = script_code ? script_code : ""
}

// 获取code
const getData = () => {
  return state.script_code
}

const sideMenu = computed(() => {
  switch (props.useType) {
    case "setup":
      return state.setupMenu
    case "teardown":
      return state.teardownMenu
    default:
      return []
  }
})


defineExpose({
  setData,
  getData,
})

</script>

<style lang="scss" scoped>

:deep(.el-card__body) {
  padding: 8px 0 !important;
}

</style>