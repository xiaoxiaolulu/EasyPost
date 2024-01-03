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

export function runApi(data: any) {
    return request({
        url: '/api/http/run',
        method: 'post',
        data
    })
}

export function saveOrUpdate(data: any) {
    return request({
        url: `/api/http/saveOrUpdate/${data.id}`,
        method: 'post',
        data
    })
}

export function getHttpList(params: any) {
    return request({
        url: `/api/http/list`,
        method: 'get',
        params
    })
}

export function getHttpDetail(data: any) {
    return request({
        url: `/api/http/detail/${data.id}`,
        method: 'get',
        data
    })
}

export function deleteHttp(data: any) {
    return request({
        url: `/api/http/delete/${data.id}`,
        method: 'delete',
        data
    })
}

export function saveCaseOrUpdate(data: any) {
    return request({
        url: `/api/case/SaveOrUpdate/${data.id}`,
        method: 'post',
        data
    })
}
