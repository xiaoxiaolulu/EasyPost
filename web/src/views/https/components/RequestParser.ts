

export const requestParser = (body: any) => {
    let req = {}
    for(let key in body) {
        if(key === "request4"){
            req["method"] = body[key]
        }
        if(key === "addr"){
            req["url"] = body[key]
        }
        if(key === "queryParams" && body[key][0].name.length != 0){
            let arrParams = [];
            let _queryParamsStr = '';
            for (let i = 0; i < body[key].length; i++) {
                try {
                    let queryParamKey = body[key][i]['name'];
                    let queryParamVal = body[key][i]['value']
                    arrParams.push(queryParamKey + '=' + queryParamVal);
                } catch (e) {
                    console.log(e)
                }
            }
            let getParams = (arrParams).join("&");
            _queryParamsStr += getParams;
            req["params"] = _queryParamsStr
        }
        if (key === "head" && body[key][0].name.length != 0) {
            let _headers = {};
            for (let i = 0; i < body[key].length; i++) {
                let headerKey = body[key][i]["name"];
                _headers[headerKey] = body[key][i]["value"];
            }
            req["headers"] = _headers
        }
        if (key === "formParams" && body[key][0].name.length != 0){
            let _requestFormData = {};
            if (body[key].length != 0) {
                for (let i = 0; i < body[key].length; i++) {
                    let requestFormDataKey = body[key][i]["name"];
                    _requestFormData[requestFormDataKey] = body[key][i]["value"];
                }
            }
            req["data"] = _requestFormData
        }
        if (key === 'codeContent' && body["codeContent"].length != 0) {
            req["json"] = JSON.parse(body[key])
        }
    }
    return req
}