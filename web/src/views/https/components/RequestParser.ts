export const requestParser = (body: any) => {
    let req = {}
    for (let key in body) {
        switch (key) {
            case "request4":
                req["method"] = body[key]
                break
            case "addr":
                req["url"] = body[key]
                break
            case "queryParams":
                if (body[key][0].name.length != 0) {
                    req["params"] = body[key].map((param: any) => `${param.name}=${param.value}`).join("&")
                }
                break
            case "head":
                if (body[key][0].name.length != 0) {
                    req["headers"] = body[key].reduce((headers: any, header: any) => ({
                        ...headers,
                        [header.name]: header.value
                    }), {})
                }
                break
            case "formParams":
                if (body[key][0].name.length != 0) {
                    req["data"] = body[key].reduce((formData: any, formParam: any) => ({
                        ...formData,
                        [formParam.name]: formParam.value
                    }), {})
                }
                break
            case 'codeContent':
                if (body["codeContent"].length != 0) {
                    req["json"] = JSON.parse(body[key])
                }
                break
        }
    }
    return req
}
