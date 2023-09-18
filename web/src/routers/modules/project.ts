/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue";

const httpsRouter = [{
    path: '/project',
    component: Layout,
    redirect: '/tool/404',
    name: '/project',
    meta: {
        title: '项目管理',
        icon: 'ElementPlus'
    },
    children: [
        {
            path: '/project/list',
            component: () => import('@/views/project/index.vue'),
            name: 'project',
            meta: { title: '项目管理', icon: 'FolderRemove'  }
        }
    ]
}]

export default httpsRouter
