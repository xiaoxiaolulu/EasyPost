import { watch, ref } from 'vue'
import { isString } from 'web/src/utils/is'
import { useAppStoreWithOut } from 'web/src/store/modules/app'
import { useI18n } from 'web/src/hooks/web/useI18n'

const appStore = useAppStoreWithOut()

export const useTitle = (newTitle?: string) => {
  const { t } = useI18n()
  const title = ref(
    newTitle ? `${appStore.getTitle} - ${t(newTitle as string)}` : appStore.getTitle
  )

  watch(
    title,
    (n, o) => {
      if (isString(n) && n !== o && document) {
        document.title = n
      }
    },
    { immediate: true }
  )

  return title
}
