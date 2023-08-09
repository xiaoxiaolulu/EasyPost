/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue";

const httpsRouter = [{
    path: '/tool',
    component: Layout,
    redirect: '/tool/404',
    name: 'tool',
    meta: {
        title: '实用工具',
        icon: 'ElementPlus'
    },
    children: [
        {
            path: '/tool/request',
            component: () => import('@/views/https/index.vue'),
            name: 'request',
            meta: { title: 'HTTP测试', icon: 'Basketball'  }
        }
    ]
}]

export default httpsRouter
