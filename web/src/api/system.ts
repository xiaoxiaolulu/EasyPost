import request from './request'

export function menuList() {
  return request({
    url: '/api/system/menu',
    method: 'post'
  })
}