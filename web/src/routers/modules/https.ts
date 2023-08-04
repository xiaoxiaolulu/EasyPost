/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue";

const httpsRouter = [{
    path: '/https',
    component: Layout,
    redirect: '/https/index',
    name: 'https',
    meta: {
        title: 'postman',
        icon: 'chat-square'
    },
    children: [
        {
            path: '/https/index',
            component: () => import('@/views/https/index.vue'),
            name: 'httpsRecord',
            meta: { title: '调试页面', icon: 'chat-square'  }
        }
    ]
}]

export default httpsRouter
