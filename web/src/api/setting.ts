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

export function noticeList(params: any) {
    return request({
        url: `/api/notice/list`,
        method: 'get',
        params
    })
}

export function noticeDelete(data: any) {
    return request({
        url: `/api/notice/delete/${data.id}`,
        method: 'delete',
        data
    })
}

export function getNoticeDetail(data: any) {
    return request({
        url: `/api/notice/detail/${data.id}`,
        method: 'get',
        data
    })
}

export function noticeSaveOrUpdate(data: any) {
    return request({
        url: `/api/notice/saveOrUpdate/${data.id}`,
        method: 'post',
        data
    })
}