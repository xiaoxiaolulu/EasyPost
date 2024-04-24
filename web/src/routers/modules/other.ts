/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout/index.vue'

const othersRouter = [{
  path: '/other',
  component: Layout,
  redirect: '/other/clipboard',
  name: 'other',
  meta: {
    title: '常用组件',
    icon: 'management'
  },
  children: [
    {
      path: '/other/clipboard',
      component: () => import('@/views/other/clipboard/index.vue'),
      name: 'clipboard',
      meta: { title: '剪贴板',  roles:['other'] ,icon: 'MenuIcon',}
    },
    {
      path: '/other/iconfont',
      component: () => import('@/views/other/iconfont/index.vue'),
      name: 'iconfont',
      meta: { title: '阿里图标库', icon: 'MenuIcon' }
    },
  ]
}]

export default othersRouter
