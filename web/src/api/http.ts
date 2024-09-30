import request from './request'


export function getTree(data: any) {
    return request({
        url: `/api/tree/${data.id}&${data.use_type}`,
        method: 'get',
        data
    })
}

export function updateTree(data: any) {
    return request({
        url: `/api/tree/${data.id}&${data.use_type}`,
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

export function runCase(data: any) {
    return request({
        url: '/api/case/run',
        method: 'post',
        data
    })
}

export function httpSnapshot(data: any) {
    return request({
        url: '/api/http/snapshot',
        method: 'post',
        data
    })
}

export function getCaseList(params: any) {
    return request({
        url: `/api/case/list`,
        method: 'get',
        params
    })
}


export function deleteCase(data: any) {
    return request({
        url: `/api/case/delete/${data.id}`,
        method: 'delete',
        data
    })
}

export function getCaseDetail(data: any) {
    return request({
        url: `/api/case/detail/${data.id}`,
        method: 'get',
        data
    })
}

export function getCaseStepDetail(data: any) {
    return request({
        url: `/api/case/step/detail/${data.id}`,
        method: 'get',
        data
    })
}

export function planList(params: any) {
    return request({
        url: `/api/plan/list`,
        method: 'get',
        params
    })
}

export function savePlanOrUpdate(data: any) {
    return request({
        url: `/api/plan/SaveOrUpdate/${data.id}`,
        method: 'post',
        data
    })
}


export function importApi(data: any) {
    return request({
        url: `/api/http/importApi/${data.id}`,
        method: 'post',
        headers: {'Content-Type': 'multipart/form-data'},
        data
    })
}


export function getClosedTasksList(params: any) {
    return request({
        url: `/api/http/closedTasks`,
        method: 'get',
        params
    })
}


export function getClosedTasksDetail(data: any) {
    return request({
        url: `/api/http/closedTasks/detail/${data.id}`,
        method: 'get',
        data
    })
}
