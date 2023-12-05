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

export function addApi(data: any) {
    return request({
        url: '/api/http/add',
        method: 'post',
        data
    })
}

export function runApi(data: any) {
    return request({
        url: '/api/http/run',
        method: 'post',
        data
    })
}