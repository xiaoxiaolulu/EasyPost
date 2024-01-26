<script setup lang="ts">
import {ref} from "vue";
import SelectApi from "@/views/https/case/components/selectApi.vue";

const emit = defineEmits(['change'])

const selectApiRef = ref()

const handleAddData = async (optType) => {
  if (optType !== 'api') {
    console.log(optType)
  } else {
    selectApiRef.value.onOpenApiList()
  }
}

const getApiStep = () => {
  let steps = selectApiRef.value.getSelectionData()
  emit('change', steps)
}


defineExpose({
  handleAddData
})
</script>

<template>
  <div>
    <select-api ref="selectApiRef" @addApiStep="getApiStep"></select-api>
  </div>
</template>

<style scoped lang="scss">
</style>