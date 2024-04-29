/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout/index.vue'

const systemRouter = [{
    path: '/system',
    component: Layout,
    redirect: '/system/user',
    name: 'system',
    meta: {
        title: '测试配置',
        icon: 'Setting',
    },
    children: [
        {
            path: '/system/environment',
            component: () => import('@/views/system/env/index.vue'),
            name: 'env',
            meta: { title: '环境管理' , icon: 'Eleme'}
        },
        {
            path: '/environment/detail',
            component: () => import('@/views/system/env/components/detail.vue'),
            name: 'environmentDetail',
            hidden: true,
            meta: { title: '环境管理详情' , icon: 'AddLocation'}
        },
        {
            path: '/system/database',
            component: () => import('@/views/system/database/index.vue'),
            name: 'database',
            meta: { title: '数据库管理' , icon: 'AddLocation'}
        },
        {
            path: '/system/datastructure',
            component: () => import('@/views/system/datastructure/index.vue'),
            name: 'datastructure',
            meta: { title: '数据结构' , icon: 'AddLocation'}
        },
        {
            path: '/function/detail',
            component: () => import('@/views/system/function/components/detail.vue'),
            name: 'functionDetail',
            hidden: true,
            meta: { title: '内置函数详情' , icon: 'AddLocation'}
        },
        {
            path: '/system/function',
            component: () => import('@/views/system/function/index.vue'),
            name: 'function',
            meta: { title: '内置函数' , icon: 'AddLocation'}
        },
        {
            path: '/system/notice',
            component: () => import('@/views/system/notice/index.vue'),
            name: 'notice',
            meta: { title: '通知设置' , icon: 'AddLocation'}
        },
        {
            path: '/system/user',
            component: () => import('@/views/system/user/index.vue'),
            name: 'user',
            meta: { title: '用户管理' , icon: 'MenuIcon'}
        },
        {
            path: '/system/dept',
            component: () => import('@/views/system/dept/index.vue'),
            name: 'dept',
            meta: { title: '部门管理' , icon: 'MenuIcon'}
        },
        {
            path: '/system/role',
            component: () => import('@/views/system/role/index.vue'),
            name: 'role',
            meta: { title: '角色管理', icon: 'MenuIcon' }
        },
        {
            path: '/system/menu',
            component: () => import('@/views/system/menu/index.vue'),
            name: 'menu',
            meta: { title: '菜单管理',  icon: 'MenuIcon'}
        },
        {
            path: '/system/dictionary',
            component: () => import('@/views/system/dictionary/index.vue'),
            name: 'dictionary',
            meta: { title: '字典管理',  icon: 'MenuIcon'}
        },
    ]
}]

export default systemRouter
