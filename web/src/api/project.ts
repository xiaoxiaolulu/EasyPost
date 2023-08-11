import request from './request'

export function projectList(data: any) {
    return request({
        url: '/api/project/list',
        method: 'get',
        data
    })
}

export function projectCreate(data: any) {
    return request({
        url: '/api/project/create',
        method: 'post',
        data
    })
}

export function projectDelete(data: any) {
    return request({
        url: `/api/project/delete/${data.id}`,
        method: 'delete',
        data
    })
}

export function projectUpdate(data: any) {
    return request({
        url: `/api/project/update/${data.id}`,
        method: 'put',
        data
    })
}

export function projectDetail(data: any) {
    return request({
        url: `/api/project/detail/${data.id}`,
        method: 'get',
        data
    })
}

export function projectRoleDelete(data: any) {
    return request({
        url: '/api/project/role/delete',
        method: 'delete',
        data
    })
}

export function projectRoleAdd(data: any) {
    return request({
        url: '/api/project/role/add',
        method: 'post',
        data
    })
}