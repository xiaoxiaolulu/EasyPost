/** When your routing table is too long, you can split it into small modules**/

import Layout from "@/layout/index.vue";

const projectRouter = [{
    path: '/project',
    component: Layout,
    redirect: '/tool/404',
    name: 'project',
    meta: {
        title: '项目管理',
        icon: 'ElementPlus'
    },
    children: [
        {
            path: '/project/list',
            component: () => import('@/views/project/index.vue'),
            name: 'projectList',
            meta: { title: '项目管理', icon: 'FolderRemove'  }
        },
        {
            path: '/project/detail',
            component: () => import('@/views/project/components/editProject.vue'),
            name: 'projectDetail',
            hidden: true,
            meta: { title: '项目详情', icon: 'FolderRemove'  }
        }
    ]
}]

export default projectRouter
