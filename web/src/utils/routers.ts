import path from "path-browserify";

export const Layout = () => import('@/layout/index.vue');
const layoutModules = import.meta.glob('/src/layout/*.{vue,tsx}');
const viewsModules = import.meta.glob('/src/views/**/*.{vue,tsx}');
const dynamicViewsModules = { ...layoutModules, ...viewsModules }; // Concise object spread


/**
 * 通过递归过滤异步路由表
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
    const res = []
    routes.forEach(route => {
        const tmp = { ...route }
        if (hasPermission(roles, tmp)) {
            if (tmp.children) {
                tmp.children = filterAsyncRoutes(tmp.children, roles)
            }
            res.push(tmp)
        }
    })
    return res
}

/**
 * 使用 meta.role 来确定当前用户是否具有权限
 * @param roles
 * @param route
 */
export function hasPermission(roles, route) {
    if (route.meta && route.meta.roles) {
        return roles.some(role => route.meta.roles.includes(role))
    } else {
        return false
    }
}

/**
 * @description 使用递归，过滤需要缓存的路由
 * @param {Array} _route 所有路由表
 * @param {Array} _cache 缓存的路由表
 * @return void
 * */

export function filterKeepAlive(routers){
    let cacheRouter: any[] = [];
    let deep = (routers)=>{
        routers.forEach(item=>{
            if(item.meta?.keepAlive&& item.name){
                cacheRouter.push(item.name)
            }
            if(item.children&&item.children.length){
                deep(item.children)
            }
        })
    }
    deep(routers)
    return cacheRouter
}



export function handleRoutes(routers,pathUrl='') {
    routers.forEach(item=>{
        item.path = path.resolve(pathUrl,item.path)
        if(item.children&&item.children.length){
        }
    })
}

export function dynamicImport(dynamicViewsModules, component) {
    const keys = Object.keys(dynamicViewsModules);
    const matchKeys = keys.filter((key) => {
        const k = key.replace(/\/src\/views|../, '');
        return k.startsWith(`${component}`) || k.startsWith(`/${component}`);
    });
    if (matchKeys?.length === 1) {
        const matchKey = matchKeys[0];
        return dynamicViewsModules[matchKey];
    }
    if (matchKeys?.length > 1) {
        return false;
    }
}

export function dynamicComponent(asyncRoutes) {

    return asyncRoutes.map(route => {
        const tmp = { ...route, component: Layout }; // Combine component assignment
        if (tmp.children) {
            tmp.children = tmp.children.map(child => ({
                ...child,
                component: dynamicImport(dynamicViewsModules, child.component),
            }));
        }
        return tmp;
    });
}
