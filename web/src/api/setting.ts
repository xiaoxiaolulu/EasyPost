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

export function envSaveOrUpdate(data: any) {
    return request({
        url: `/api/env/saveOrUpdate/${data.id}`,
        method: 'post',
        data
    })
}

export function getEnvDetail(data: any) {
    return request({
        url: `/api/env/detail/${data.id}`,
        method: 'get',
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


export function databaseList(params: any) {
    return request({
        url: `/api/database/list`,
        method: 'get',
        params
    })
}

export function databaseDelete(data: any) {
    return request({
        url: `/api/database/delete/${data.id}`,
        method: 'delete',
        data
    })
}

export function databaseUpdate(data: any) {
    return request({
        url: `/api/database/update/${data.id}`,
        method: 'put',
        data
    })
}

export function databaseCreate(data: any) {
    return request({
        url: '/api/database/create',
        method: 'post',
        data
    })
}

export function databaseDebug(data: any) {
    return request({
        url: '/api/database/isConnect',
        method: 'post',
        data
    })
}

export function functionList(params: any) {
    return request({
        url: `/api/function/list`,
        method: 'get',
        params
    })
}


export function functionDebug(data: any) {
    return request({
        url: `/api/function/debug/${data.id}`,
        method: 'post',
        data
    })
}


export function functionDetailList(data: any) {
    return request({
        url: `/api/function/detailList`,
        method: 'post',
        data
    })
}
