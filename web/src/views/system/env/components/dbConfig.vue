<script setup lang="ts">
import {ref} from "vue";
import SelectDatabase from "@/views/system/env/components/selectDatabase.vue";

const emit = defineEmits(['change'])

const selectDatabaseRef = ref()

const handleAddData = async () => {
  selectDatabaseRef.value.onOpenDatabaseList()
}

const getDatabaseStep = () => {
  let steps = selectDatabaseRef.value.getSelectionData()
  emit('change', steps)
}

defineExpose({
  handleAddData
})
</script>

<template>
  <div>
    <select-database ref="selectDatabaseRef" @getDatabaseStep="getDatabaseStep"></select-database>
  </div>
</template>

<style scoped lang="scss">
</style>