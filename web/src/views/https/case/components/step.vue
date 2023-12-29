<script setup lang="ts">
import {ref} from "vue";
import SelectApi from "@/views/https/case/components/selectApi.vue";

const selectApiRef = ref()

const handleAddData = async (optType) => {
  if (optType !== 'api') {
    console.log("嘻嘻嘻嘻嘻嘻休息休")
    console.log(optType)
  } else {
    console.log("11111111")
    selectApiRef.value.onOpenApiList()
  }
}

defineExpose({
  handleAddData,
})
</script>

<template>
  <div>
    <select-api ref="selectApiRef"></select-api>
  </div>
</template>

<style scoped lang="scss">
</style>