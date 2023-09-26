/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue";

const httpsRouter = [{
    path: '/https',
    component: Layout,
    redirect: '/https/404',
    name: 'https',
    meta: {
        title: '接口测试',
        icon: 'ElementPlus'
    },
    children: [
        {
            path: '/https/apis',
            component: () => import('@/views/https/api/index.vue'),
            name: 'apis',
            meta: { title: '接口管理', icon: 'Lightning'  }
        },
    ]
}]

export default httpsRouter
