import axios, {AxiosError} from 'axios'
import {useUserStore} from "@/store/modules/user"
import {ElMessageBox, ElMessage} from "element-plus";


// 创建axios实例 进行基本参数配置
const service = axios.create({
    // 默认请求地址，根据环境的不同可在.env 文件中进行修改
    baseURL: import.meta.env.VITE_APP_BASE_API,
    // 设置接口访问超时时间
    timeout: 3000000, // request timeout，
    // 跨域时候允许携带凭证
    // withCredentials: true
})

//  request interceptor 接口请求拦截
service.interceptors.request.use((config) => {
    /**
     * 用户登录之后获取服务端返回的token,后面每次请求都在请求头中带上token进行JWT校验
     * token 存储在本地储存中（storage）、vuex、pinia
     */
    const userStore = useUserStore();
    const token: string = userStore.token;
    // 自定义请求头
    if (token) {
        config.headers['Authorization'] = `JWT ${token}`
    }
    return config
}, (error: AxiosError) => {
    // 请求错误，这里可以用全局提示框进行提示
    return Promise.reject(error);
})

//  response interceptor 接口响应拦截
service.interceptors.response.use(
    (response) => {
        // 对响应数据做点什么
        const res = response.data;
        if (res.code && res.code !== 0) {
            // `token` 过期或者账号已在别处登录
            if (res.code === 11000) {
                ElMessageBox.confirm('登录信息已失效，是否重新登录？', '提示', {
                    confirmButtonText: '确认',
                    cancelButtonText: '取消',
                    type: 'warning',
                })
                    .then(() => {
                        window.localStorage.removeItem('userState');
                        window.sessionStorage.clear();
                        window.location.href = '/login'; // 去登录页
                        return false
                    })
                    .catch(() => {
                    });
            } else {
                ElMessage.error(res.msg);
            }
            return Promise.reject(service.interceptors.response);
        } else {
            return response;
        }
    },
    (error) => {
        // 对响应错误做点什么
        return Promise.reject(error);
    }
);
export default service