import {defineStore} from 'pinia'
import { constantRoutes, notFoundRouter } from "@/routers"
import { hasPermission, filterAsyncRoutes, dynamicImport, dynamicComponent } from "@/utils/routers";
import {filterKeepAlive} from "@/utils/routers";
import { useUserStore } from "@/store/modules/user";
export const usePermissionStore = defineStore({
    // id: 必须的，在所有 Store 中唯一
    id:'permissionState',
    // state: 返回对象的函数
    state: ()=>({
        // 路由
        routes:[],
        // 动态路由
        addRoutes:[],
        // 缓存路由
        cacheRoutes:{},

        asyncRoutes: [],
    }),
    getters: {
        permission_routes:state=> {
            return state.routes
        },
        keepAliveRoutes: state=>{
            return filterKeepAlive(state.asyncRoutes)
        }
    },


    // 可以同步 也可以异步
    actions:{
        // 生成路由
        async generateRoutes(roles){
            return new Promise(resolve => {
                const UserStore = useUserStore()
                this.asyncRoutes = UserStore.menus
                let accessedRoutes = dynamicComponent(this.asyncRoutes)
                // 在这判断是否有权限，哪些角色拥有哪些权限
                // if (roles&&roles.length&&!roles.includes('admin')) {
                //     accessedRoutes = filterAsyncRoutes(accessedRoutes, roles)
                // } else {
                //     accessedRoutes = asyncRoutes || []
                // }
                accessedRoutes = accessedRoutes.concat(notFoundRouter)
                this.routes = constantRoutes.concat(accessedRoutes)
                this.addRoutes = accessedRoutes
                resolve(accessedRoutes)
            })
        },
        // 清楚路由
        clearRoutes(){
            this.routes = []
            this.addRoutes = []
            this.cacheRoutes = []
        },
        getCacheRoutes(){
            this.cacheRoutes = filterKeepAlive(this.asyncRoutes)
            return this.cacheRoutes
        }
    },

})



