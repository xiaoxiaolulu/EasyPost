import request from './request'

export function login(data) {
    return request({
        url: '/api/login/',
        method: 'post',
        data
    })
}
