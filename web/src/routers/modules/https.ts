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
        {
            path: '/http/detail',
            component: () => import('@/views/https/api/components/detail.vue'),
            name: 'httpDetail',
            hidden: true,
            meta: { title: '接口详情', icon: 'FolderRemove'  }
        },{
            path: '/https/case',
            component: () => import('@/views/https/case/index.vue'),
            name: 'case',
            meta: { title: '接口用例', icon: 'Lightning'  }
        },        {
            path: '/case/detail',
            component: () => import('@/views/https/case/components/detail.vue'),
            name: 'caseDetail',
            hidden: true,
            meta: { title: '用例详情', icon: 'FolderRemove'  }
        },
    ]
}]

export default httpsRouter
