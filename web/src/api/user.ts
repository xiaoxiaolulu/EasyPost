import request from './request'

export function login(data: any) {
    return request({
        url: '/api/user/login/',
        method: 'post',
        data
    })
}

export function userList(data: any) {
    return request({
        url: '/api/user/list',
        method: 'get',
        data
    })
}
