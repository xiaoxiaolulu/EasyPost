<script setup lang="ts">
import {ref} from "vue";
import SelectDatabase from "@/views/system/env/components/selectDatabase.vue";

const emit = defineEmits(['change'])

const selectDatabaseRef = ref()

const handleAddData = () => {
  selectDatabaseRef.value.onOpenDatabaseList()
}

const getDbSetting = () => {
  let steps = selectDatabaseRef.value.getSelectionData()
  emit('change', steps)
}

defineExpose({
  handleAddData
})
</script>

<template>
  <div>
    <select-database ref="selectDatabaseRef" @addDbSetting="getDbSetting"></select-database>
  </div>
</template>

<style scoped lang="scss">
</style>