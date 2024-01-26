/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue";

const toolsRouter = [{
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
            component: () => import('@/views/tools/index.vue'),
            name: 'request',
            meta: { title: 'HTTP测试', icon: 'Lightning'  }
        }
    ]
}]

export default toolsRouter
