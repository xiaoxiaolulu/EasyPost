/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue";

const recordRouter = [{
    path: '/record',
    component: Layout,
    redirect: '/tool/404',
    name: 'record',
    meta: {
        title: '测试报告',
        icon: 'ElementPlus'
    },
    children: [
        {
            path: '/record/list',
            component: () => import('@/views/record/build/index.vue'),
            name: 'recordList',
            meta: { title: '构建历史', icon: 'FolderRemove'  }
        },
        {
            path: '/record/detail',
            component: () => import('@/views/record/build/components/detail.vue'),
            name: 'recordDetail',
            hidden: true,
            meta: { title: '构建详情', icon: 'FolderRemove'  }
        },
        {
            path: '/history/list',
            component: () => import('@/views/record/history/index.vue'),
            name: 'historyList',
            meta: { title: '执行记录', icon: 'FolderRemove'  }
        }
    ]
}]

export default recordRouter
