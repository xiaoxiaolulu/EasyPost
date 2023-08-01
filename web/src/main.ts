// 引入windi css
import 'web/src/plugins/windi.css'

// 导入全局的svg图标
import 'web/src/plugins/svgIcon'

// 初始化多语言
import { setupI18n } from 'web/src/plugins/vueI18n'

// 引入状态管理
import { setupStore } from 'web/src/store'

// 全局组件
import { setupGlobCom } from 'web/src/components'

// 引入element-plus
import { setupElementPlus } from 'web/src/plugins/elementPlus'

// 引入全局样式
import 'web/src/styles/index.less'

// 引入动画
import 'web/src/plugins/animate.css'

// 路由
import { setupRouter } from './router'

// 权限
import { setupPermission } from './directives'

import { createApp } from 'vue'

import App from './App.vue'

import './permission'

// 创建实例
const setupAll = async () => {
  const app = createApp(App)

  await setupI18n(app)

  setupStore(app)

  setupGlobCom(app)

  setupElementPlus(app)

  setupRouter(app)

  setupPermission(app)

  app.mount('#app')
}

setupAll()
