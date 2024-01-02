<script setup lang="ts">
import {ref} from "vue";
import SelectApi from "@/views/https/case/components/selectApi.vue";

const selectApiRef = ref()

const handleAddData = async (optType) => {
  if (optType !== 'api') {
    console.log(optType)
  } else {
    selectApiRef.value.onOpenApiList()
  }
}

const addApiStep = () => {
  selectApiRef.value.getSelectionData()
}

defineExpose({
  handleAddData,
})
</script>

<template>
  <div>
    <select-api ref="selectApiRef" @addApiStep="addApiStep"></select-api>
  </div>
</template>

<style scoped lang="scss">
</style>