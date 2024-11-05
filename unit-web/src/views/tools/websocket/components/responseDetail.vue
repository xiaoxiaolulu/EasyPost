<script setup lang="ts">
import {watch, onMounted} from "vue";
import {reactive} from 'vue';
import SvgIcon from "@/components/SvgIcon/index.vue";

const props = defineProps({
  reportData: {
    type: Object,
    default: () => {
    }
  }
})

const state = reactive({
  messageData: [],
})

const initData = () => {
  let data
  if (props.reportData) {
    data = props.reportData
    state.messageData = data['messageData']
  }
}

watch(
  () => props.reportData,
  () => {
    initData()
  },
  {deep: true}
);

onMounted(() => {
  initData()
})
</script>
<template>
  <div style="height: 100%; overflow-y: auto">
    <el-table :data="state.messageData" style="width: 100%">
      <el-table-column prop="message">
        <template #default="scope">
          <SvgIcon :icon-class="scope.row.message.type"
                   style="width: 12px; height: 12px;"/>
          <span class="content" style="">{{scope.row.message.content}}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped lang="scss">
</style>