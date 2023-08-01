export type contextMenuSchema = {
  disabled?: boolean
  divided?: boolean
  icon?: string
  label: string
  command?: (item: contextMenuSchema) => void
}
