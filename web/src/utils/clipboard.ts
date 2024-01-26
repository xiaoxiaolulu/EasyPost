import Clipboard from 'clipboard'
import { ElMessage  } from 'element-plus'


function clipboardSuccess() {
    ElMessage({
        message: '复制成功',
        type: 'success',
        duration: 1500
    })
}

function clipboardError() {
    ElMessage({
        message: '复制失败',
        type: 'error'
    })
}

export default function handleClipboard(text, event) {
    const clipboard:any = new Clipboard(event.target, {
        text: () => text
    })
    clipboard.on('success', () => {
        clipboardSuccess()
        clipboard.destroy()
    })
    clipboard.on('error', () => {
        clipboardError()
        clipboard.destroy()
    })
    clipboard.onClick(event)
}
