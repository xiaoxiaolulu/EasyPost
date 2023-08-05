import request from './request'

export function http(data: any) {
    return request({
        url: '/api/http/',
        method: 'post',
        data
    })
}
