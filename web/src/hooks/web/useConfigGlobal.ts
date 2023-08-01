import { ConfigGlobalTypes } from 'web/src/types/configGlobal'
import { inject } from 'vue'

export const useConfigGlobal = () => {
  const configGlobal = inject('configGlobal', {}) as ConfigGlobalTypes

  return {
    configGlobal
  }
}
