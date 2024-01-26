<script setup lang="ts">
import * as monaco from "monaco-editor"
import { withDefaults, defineProps, ref, defineEmits, onMounted, onUnmounted, watch } from 'vue'
import { OPTIONS_BASE } from './registerCompletion'
import './worker'
interface IProps {
  modelValue: string
  disabled?: boolean
  editorConfig?: { language: string; theme: 'vs' | 'vs-dark' | 'hc-black' }
}
const props = withDefaults(defineProps<IProps>(), {
  modelValue: '',
  disabled: false,
  editorConfig: () => ({ language: 'json', theme: 'vs-dark' }),
})

const cusEditor = ref<HTMLElement | null>(null)
let editor: Partial<monaco.editor.IStandaloneCodeEditor> = {}
const emit = defineEmits(['update:modelValue'])
/**初始化编辑器 */
onMounted(() => {
  onDispose()
  if (cusEditor.value) {
    editor = monaco.editor.create(cusEditor.value, { ...OPTIONS_BASE, ...props.editorConfig, readOnly: props.disabled })
    editor.onDidChangeModelContent &&
    editor.onDidChangeModelContent(() => {
      const value = editor.getValue && editor.getValue() // 给父组件实时返回最新文本
      emit('update:modelValue', value)
    })
  }
})
/**销毁实例 */
const onDispose = () => {
  editor && editor.dispose && editor.dispose()
}
onUnmounted(() => {
  onDispose()
})
/**修改只读状态 */
watch(
    () => props.disabled,
    (val) => {
      editor.updateOptions && editor.updateOptions({ readOnly: val })
    }
)
/**修改配置 */
watch(
    () => props.editorConfig,
    (val) => {
      const model = editor.getModel && editor.getModel()
      if (model) {
        monaco.editor.setModelLanguage(model, val.language)
        monaco.editor.setTheme(val.theme)
      }
    },
    { deep: true }
)
/**回显数据 */
watch(
    () => props.modelValue,
    (val) => {
      if (editor) {
        const value = editor.getValue && editor.getValue()
        if (val !== value) {
          editor.setValue && editor.setValue(val || '')
        }
      }
    }
)
</script>

<template>
  <div ref="cusEditor" id="code-editor" style="width:100%;height:500px;border:1px solid #e6e6e6;"></div>
</template>

<style scoped lang="scss">
</style>