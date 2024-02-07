import request from './request'

export function recordList(params: any) {
    return request({
        url: `/api/report/list`,
        method: 'get',
        params
    })
}
