<template>
  <div>
    <el-select
        v-model="currentEnv"
        size="default"
        ref="methodRef"
        placeholder=""
        filterable
        style="width: 200px; color: #22a1c4"
    >
      <template #header>
          <el-button style="color:coral" bg size="small" link @click="addEnv">
            <el-icon><CirclePlus /></el-icon>新建环境</el-button
          >
      </template>
      <el-option v-for="item in envOption"
                 :key="item.value"
                 :label="item.label"
                 :value="item.value"
                 style="font-size: 12px">
        <span style="float: left">{{ item.label }}</span>
        <span style="float: right">
          <el-button @click="editEnv(item.value)" size="small" link>
            <el-icon><View /></el-icon>
          </el-button>
      </span>
      </el-option>
    </el-select>
  </div>
</template>
<script setup lang="ts">
import {ref} from 'vue'
import {CirclePlus, View} from "@element-plus/icons-vue";
import {useRouter} from "vue-router";
import {envList} from "@/api/setting";
import {ElMessage} from "element-plus";

const router = useRouter()

const search = ref("")

const addEnv = () => {
  router.push({
    name: "environmentDetail",
    query: {editType: 'save'}
  });
};

const editEnv = (id: any) => {
  if (id) {
    router.push({
      name: "environmentDetail",
      query: {editType: 'update', id: id}
    });
  } else {
    ElMessage.error("编辑环境配置异常请重试!");
  }
};

const currentEnv = ref()

const envOption = ref([])

const init = () => {
  envList({}).then((response) => {
    let data = response.data.results
    for (let i = 0; i < data.length; i++) {
      envOption.value.push({
        "label": data[i]["name"],
        "value": data[i]["id"],
        "params": data[i]
      })
    }
  }).catch((error) => {
  })
}

init()
</script>
<style scoped lang="scss">

</style>