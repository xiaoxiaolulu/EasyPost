import { h } from 'vue'
import type { VNode } from 'vue'
import { Icon } from 'web/src/components/Icon'
import { IconTypes } from 'web/src/types/icon'

export const useIcon = (props: IconTypes): VNode => {
  return h(Icon, props)
}
