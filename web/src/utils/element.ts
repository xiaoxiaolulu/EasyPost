import { ElLoading, ElMessage } from 'element-plus'
import {
    Loading
} from '@element-plus/icons-vue'
let loading = null

export const openLoading = (options={})=>{
    const text = options.text||'加载中'
    loading = ElLoading.service({
        lock: true,
        text: text,
    })
}
export const closeLoading = () => {
    loading&&loading.close()
}

/**
 * @description 显示错误消息
 * opt 传入参数
 * err 错误信息
 * type 消息类型
 * duration 消息持续时间
 */
export const showErrMessage  = (code:string, msg:string) => {
    switch (code) {
        case "0":
            showMessage(msg, "success")
            break
        case "110":
            showMessage(msg, "error")
            break
        case "403":
            showMessage(msg, "waining")
            break
    }
}

export const showMessage = (msg:string, type:any= 'error') =>{
    ElMessage({
        message: msg,
        type:type,
    })
}
