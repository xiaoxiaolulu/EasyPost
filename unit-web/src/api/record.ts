import request from './request'

export function recordList(params: any) {
    return request({
        url: `/api/report/list`,
        method: 'get',
        params
    })
}

export function recordDetail(params: any) {
    return request({
        url: `/api/report/detail`,
        method: 'get',
        params
    })
}


export function taskRecordList(params: any) {
    return request({
        url: `/api/plan/record/list`,
        method: 'get',
        params
    })
}
