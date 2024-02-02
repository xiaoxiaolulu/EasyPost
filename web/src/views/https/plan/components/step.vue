<script setup lang="ts">
import {ref} from "vue";
import SelectCase from "@/views/https/plan/components/selectCase.vue";

const emit = defineEmits(['change'])

const selectCaseRef = ref()

const handleAddData = async (optType) => {
  if (optType !== 'api') {
    console.log(optType)
  } else {
    selectCaseRef.value.onOpenCaseList()
  }
}

const getCase = () => {
  let steps = selectCaseRef.value.getSelectionData()
  emit('change', steps)
}

defineExpose({
  handleAddData
})
</script>

<template>
  <div>
    <select-case ref="selectCaseRef" @addCase="getCase"></select-case>
  </div>
</template>

<style scoped lang="scss">
</style>