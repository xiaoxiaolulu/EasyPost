import request from './request'

export function http(data: any) {
    return request({
        url: '/api/http/',
        method: 'post',
        data
    })
}

export function getTree(data: any) {
    return request({
        url: `/api/tree/${data.id}`,
        method: 'get',
        data
    })
}

export function updateTree(data: any) {
    return request({
        url: `/api/tree/${data.id}`,
        method: 'put',
        data
    })
}