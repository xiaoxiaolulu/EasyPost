import {createRouter, createWebHashHistory} from 'vue-router'
import type {RouteRecordRaw} from 'vue-router'
import type {App} from 'vue'
import {Layout} from 'web/src/utils/routerHelper'
import {useI18n} from 'web/src/hooks/web/useI18n'

const {t} = useI18n()

export const constantRouterMap: AppRouteRecordRaw[] = [
    {
        path: '/',
        component: Layout,
        redirect: '/dashboard/workplace',
        name: 'Root',
        meta: {
            hidden: true
        }
    },
    {
        path: '/redirect',
        component: Layout,
        name: 'Redirect',
        children: [
            {
                path: '/redirect/:path(.*)',
                name: 'Redirect',
                component: () => import('web/src/views/Redirect/Redirect.vue'),
                meta: {}
            }
        ],
        meta: {
            hidden: true,
            noTagsView: true
        }
    },
    {
        path: '/login',
        component: () => import('web/src/views/Login/Login.vue'),
        name: 'Login',
        meta: {
            hidden: true,
            title: t('router.login'),
            noTagsView: true
        }
    },
    {
        path: '/404',
        component: () => import('web/src/views/Error/404.vue'),
        name: 'NoFind',
        meta: {
            hidden: true,
            title: '404',
            noTagsView: true
        }
    }
]

export const asyncRouterMap: AppRouteRecordRaw[] = [
    {
        path: '/dashboard',
        component: Layout,
        redirect: '/dashboard/workplace',
        name: 'Dashboard',
        meta: {
            title: t('router.dashboard'),
            icon: 'ant-design:dashboard-filled',
            alwaysShow: true
        },
        children: [
            {
                path: 'workplace',
                component: () => import('web/src/views/Dashboard/Workplace.vue'),
                name: 'Workplace',
                meta: {
                    title: t('router.workplace'),
                    noCache: true
                }
            }, {
                path: 'analysis',
                component: () => import('web/src/views/Dashboard/Analysis.vue'),
                name: 'Analysis',
                meta: {
                    title: t('router.analysis'),
                    noCache: true,
                    affix: true
                }
            }
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    strict: true,
    routes: constantRouterMap as RouteRecordRaw[],
    scrollBehavior: () => ({left: 0, top: 0})
})

export const resetRouter = (): void => {
    const resetWhiteNameList = ['Redirect', 'Login', 'NoFind', 'Root']
    router.getRoutes().forEach((route) => {
        const {name} = route
        if (name && !resetWhiteNameList.includes(name as string)) {
            router.hasRoute(name) && router.removeRoute(name)
        }
    })
}

export const setupRouter = (app: App<Element>) => {
    app.use(router)
}

export default router
