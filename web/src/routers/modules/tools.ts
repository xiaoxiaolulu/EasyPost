/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout/index.vue'

const toolsRouter = [{
  path: '/tools',
  component: Layout,
  redirect: '/tools/404',
  name: 'tools',
  meta: {
    title: '测试工具',
    icon: 'ElementPlus'
  },
  children: [
    {
      path: '/tools/websocket',
      component: () => import('@/views/tools/websocket/index.vue'),
      name: 'websocket',
      meta: { title: 'websocket', icon: 'Lightning'  }
    }
  ]
}]

export default toolsRouter
