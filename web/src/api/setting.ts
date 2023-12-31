import request from './request'

export function envList(params: any) {
    return request({
        url: `/api/env/list`,
        method: 'get',
        params
    })
}

export function envDelete(data: any) {
    return request({
        url: `/api/env/delete/${data.id}`,
        method: 'delete',
        data
    })
}

export function envUpdate(data: any) {
    return request({
        url: `/api/env/update/${data.id}`,
        method: 'put',
        data
    })
}

export function envCreate(data: any) {
    return request({
        url: '/api/env/create',
        method: 'post',
        data
    })
}

export function addressList(params: any) {
    return request({
        url: `/api/address/list`,
        method: 'get',
        params
    })
}

export function addressDelete(data: any) {
    return request({
        url: `/api/address/delete/${data.id}`,
        method: 'delete',
        data
    })
}

export function addressUpdate(data: any) {
    return request({
        url: `/api/address/update/${data.id}`,
        method: 'put',
        data
    })
}

export function addressCreate(data: any) {
    return request({
        url: '/api/address/create',
        method: 'post',
        data
    })
}