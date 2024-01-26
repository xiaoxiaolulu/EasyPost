import * as monaco from "monaco-editor"

export const OPTIONS_BASE: monaco.editor.IStandaloneEditorConstructionOptions = {
    value: '', // 初始显示文字
    lineNumbers: 'on', // 是否展示行号 'off' | 'on
    automaticLayout: true, //自动布局
    minimap: {
        enabled: true,
    },
    tabSize: 2,
    fontSize: 16,
    roundedSelection: false,
    cursorStyle: 'line', //光标样式
    glyphMargin: true, //字形边缘
    useTabStops: false,
    quickSuggestionsDelay: 100, //代码提示延时
    selectOnLineNumbers: true, // 显示行号
}
