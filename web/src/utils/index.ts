
/**
 * Parse the time to string
 * @param {(Object|string|number)} time
 * @param {string} cFormat
 * @returns {string | null}
 */
export function parseTime(time, cFormat) {
  if (arguments.length === 0) {
    return null
  }
  const format = cFormat || '{y}-{m}-{d} {h}:{i}:{s}'
  let date
  if (typeof time === 'undefined' || time === null || time === 'null') {
    return ''
  } else if (typeof time === 'object') {
    date = time
  } else {
    if ((typeof time === 'string') && (/^[0-9]+$/.test(time))) {
      time = parseInt(time)
    }
    if ((typeof time === 'number') && (time.toString().length === 10)) {
      time = time * 1000
    }
    date = new Date(time)
  }
  const formatObj = {
    y: date.getFullYear(),
    m: date.getMonth() + 1,
    d: date.getDate(),
    h: date.getHours(),
    i: date.getMinutes(),
    s: date.getSeconds(),
    a: date.getDay()
  }
  const time_str = format.replace(/{(y|m|d|h|i|s|a)+}/g, (result, key) => {
    let value = formatObj[key]
    // Note: getDay() returns 0 on Sunday
    if (key === 'a') {
      return ['日', '一', '二', '三', '四', '五', '六'][value]
    }
    if (result.length > 0 && value < 10) {
      value = '0' + value
    }
    return value || 0
  })
  return time_str
}

/**
 * @param {number} time
 * @param {string} option
 * @returns {string}
 */
export function formatTime(time, option) {
  if (('' + time).length === 10) {
    time = parseInt(time) * 1000
  } else {
    time = +time
  }
  const d = new Date(time)
  const now = Date.now()

  const diff = (now - d) / 1000

  if (diff < 30) {
    return '刚刚'
  } else if (diff < 3600) {
    // less 1 hour
    return Math.ceil(diff / 60) + '分钟前'
  } else if (diff < 3600 * 24) {
    return Math.ceil(diff / 3600) + '小时前'
  } else if (diff < 3600 * 24 * 2) {
    return '1天前'
  }
  if (option) {
    return parseTime(time, option)
  } else {
    return (
      d.getMonth() + 1 + '月' + d.getDate() + '日' + d.getHours() + '时' + d.getMinutes() + '分'
    )
  }
}

/**
 * @param {string} url
 * @returns {Object}
 */
export function getQueryObject(url) {
  url = url == null ? window.location.href : url
  const search = url.substring(url.lastIndexOf('?') + 1)
  const obj = {}
  const reg = /([^?&=]+)=([^?&=]*)/g
  search.replace(reg, (rs, $1, $2) => {
    const name = decodeURIComponent($1)
    let val = decodeURIComponent($2)
    val = String(val)
    obj[name] = val
    return rs
  })
  return obj
}

/**
 * @param {string} input value
 * @returns {number} output value
 */
export function byteLength(str) {
  // returns the byte length of an utf8 string
  let s = str.length
  for (var i = str.length - 1; i >= 0; i--) {
    const code = str.charCodeAt(i)
    if (code > 0x7f && code <= 0x7ff) s++
    else if (code > 0x7ff && code <= 0xffff) s += 2
    if (code >= 0xdc00 && code <= 0xdfff) i--
  }
  return s
}

/**
 * @param {Array} actual
 * @returns {Array}
 */
export function cleanArray(actual) {
  const newArray = []
  for (let i = 0; i < actual.length; i++) {
    if (actual[i]) {
      newArray.push(actual[i])
    }
  }
  return newArray
}

/**
 * @param {Object} json
 * @returns {Array}
 */
export function param(json) {
  if (!json) return ''
  return cleanArray(
    Object.keys(json).map((key) => {
      if (json[key] === undefined) return ''
      return encodeURIComponent(key) + '=' + encodeURIComponent(json[key])
    }),
  ).join('&')
}

/**
 * @param {string} url
 * @returns {Object}
 */
export function param2Obj(url) {
  const search = decodeURIComponent(url.split('?')[1]).replace(/\+/g, ' ')
  if (!search) {
    return {}
  }
  const obj = {}
  const searchArr = search.split('&')
  searchArr.forEach((v) => {
    const index = v.indexOf('=')
    if (index !== -1) {
      const name = v.substring(0, index)
      const val = v.substring(index + 1, v.length)
      obj[name] = val
    }
  })
  return obj
}

/**
 * @param {string} val
 * @returns {string}
 */
export function html2Text(val) {
  const div = document.createElement('div')
  div.innerHTML = val
  return div.textContent || div.innerText
}

/**
 * Merges two objects, giving the last one precedence
 * @param {Object} target
 * @param {(Object|Array)} source
 * @returns {Object}
 */
export function objectMerge(target, source) {
  if (typeof target !== 'object') {
    target = {}
  }
  if (Array.isArray(source)) {
    return source.slice()
  }
  Object.keys(source).forEach((property) => {
    const sourceProperty = source[property]
    if (typeof sourceProperty === 'object') {
      target[property] = objectMerge(target[property], sourceProperty)
    } else {
      target[property] = sourceProperty
    }
  })
  return target
}

/**
 * @param {HTMLElement} element
 * @param {string} className
 */
export function toggleClass(element, className) {
  if (!element || !className) {
    return
  }
  let classString = element.className
  const nameIndex = classString.indexOf(className)
  if (nameIndex === -1) {
    classString += '' + className
  } else {
    classString =
      classString.substr(0, nameIndex) + classString.substr(nameIndex + className.length)
  }
  element.className = classString
}

/**
 * @param {string} type
 * @returns {Date}
 */
export function getTime(type) {
  if (type === 'start') {
    return new Date().getTime() - 3600 * 1000 * 24 * 90
  } else {
    return new Date(new Date().toDateString())
  }
}

/**
 * @param {Function} func
 * @param {number} wait
 * @param {boolean} immediate
 * @return {*}
 */
export function debounce(func, wait, immediate) {
  let timeout, args, context, timestamp, result

  const later = function () {
    // 据上一次触发时间间隔
    const last = +new Date() - timestamp

    // 上次被包装函数被调用时间间隔 last 小于设定时间间隔 wait
    if (last < wait && last > 0) {
      timeout = setTimeout(later, wait - last)
    } else {
      timeout = null
      // 如果设定为immediate===true，因为开始边界已经调用过了此处无需调用
      if (!immediate) {
        result = func.apply(context, args)
        if (!timeout) context = args = null
      }
    }
  }

  return function (...args) {
    context = this
    timestamp = +new Date()
    const callNow = immediate && !timeout
    // 如果延时不存在，重新设定延时
    if (!timeout) timeout = setTimeout(later, wait)
    if (callNow) {
      result = func.apply(context, args)
      context = args = null
    }

    return result
  }
}

/**
 * This is just a simple version of deep copy
 * Has a lot of edge cases bug
 * If you want to use a perfect deep copy, use lodash's _.cloneDeep
 * @param {Object} source
 * @returns {Object}
 */
export function deepClone(source) {
  if (!source && typeof source !== 'object') {
    throw new Error('error arguments', 'deepClone')
  }
  const targetObj = source.constructor === Array ? [] : {}
  Object.keys(source).forEach((keys) => {
    if (source[keys] && typeof source[keys] === 'object') {
      targetObj[keys] = deepClone(source[keys])
    } else {
      targetObj[keys] = source[keys]
    }
  })
  return targetObj
}

/**
 * @param {Array} arr
 * @returns {Array}
 */
export function uniqueArr(arr) {
  return Array.from(new Set(arr))
}

/**
 * @returns {string}
 */
export function createUniqueString() {
  const timestamp = +new Date() + ''
  const randomNum = parseInt((1 + Math.random()) * 65536) + ''
  return (+(randomNum + timestamp)).toString(32)
}

/**
 * Check if an element has a class
 * @param {HTMLElement} elm
 * @param {string} cls
 * @returns {boolean}
 */
export function hasClass(ele, cls) {
  return !!ele.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)'))
}

/**
 * Add class to element
 * @param {HTMLElement} elm
 * @param {string} cls
 */
export function addClass(ele, cls) {
  if (!hasClass(ele, cls)) ele.className += ' ' + cls
}

/**
 * Remove class from element
 * @param {HTMLElement} elm
 * @param {string} cls
 */
export function removeClass(ele, cls) {
  if (hasClass(ele, cls)) {
    const reg = new RegExp('(\\s|^)' + cls + '(\\s|$)')
    ele.className = ele.className.replace(reg, ' ')
  }
}

export function getColor() {
  var str = '#'
  var arr = ['1', '2', '3', '4', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
  for (var i = 0; i < 6; i++) {
    var num = parseInt(Math.random() * 16)
    str += arr[num]
  }
  return str
}
// 检查给定的值是否是数组
export const isArray = function (value) {
  return objToString.call(value) === '[object Array]'
}

let funProto = Function.prototype
let objProto = Object.prototype

let getPrototypeOf = Object.getPrototypeOf

let objToString = objProto.toString
let hasOwnProperty = objProto.hasOwnProperty
let funToString = funProto.toString
// 检查给定的值是否是字符串
export const isString = function (value) {
  return objToString.call(value) === '[object String]'
}
// 检查给定的值是否是纯对象，纯对象是指通过 {} 或 new Object() 声明的对象
export const isPlainObject = function (value) {
  if (!value || objToString.call(value) !== '[object Object]') {
    return false
  }

  let prototype = getPrototypeOf(value)

  if (prototype === null) {
    return true
  }

  let constructor = hasOwnProperty.call(prototype, 'constructor') && prototype.constructor

  return (
    typeof constructor === 'function' && funToString.call(constructor) === funToString.call(Object)
  )
}

// // 深度克隆 array 数组或 json 对象，返回克隆后的副本
export const deepObjClone = function (obj) {
  let weakMap = new WeakMap()
  function clone(obj) {
    if (obj == null) {
      return obj
    }
    if (obj instanceof Date) {
      return new Date(obj)
    }
    if (obj instanceof RegExp) {
      return new RegExp(obj)
    }
    if (typeof obj !== 'object') return obj

    if (weakMap.get(obj)) {
      return weakMap.get(obj)
    }
    let copy = new obj.constructor()
    weakMap.set(obj, copy)
    for (let key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        let value = obj[key]
        copy[key] = clone(value)
      }
    }
    return copy
  }
  return clone(obj)
}


export function getTimeStateStr() {
  let timeNow = new Date();
  let hours = timeNow.getHours();
  if (hours >= 6 && hours <= 10) return `早上好`;
  if (hours >= 10 && hours <= 14) return `中午好`;
  if (hours >= 14 && hours <= 18) return `下午好`;
  if (hours >= 18 && hours <= 24) return `晚上好`;
  if (hours >= 0 && hours <= 6) return `凌晨好`;
}

export function ellipsis(value: string, length: number, step: number) {
  console.log(value.length)
  if (!value) {
    return "";
  }
  if (value.length > length) {
    return value.slice(0, step) + "...";
  } else {
    return value;
  }
}

export const stepTypes = {
  api: "引用接口",
  if: "条件控制器",
  loop: "循环控制器",
  extract: "参数提取",
  script: "自定义脚本",
  sql: "SQL控制器",
  wait: "等待控制器",
  scene: "场景断言",
  case: "引用用例",
}

export function getStepTypesByUse(use_type) {
  let stepTypeMapping
  let stepContain
  switch (use_type) {
    case "hook":
      stepContain = ["sql", "wait"]
      stepTypeMapping = objectFilter(stepTypes, stepContain)
      break
    case "case":
      stepContain = ["api", "if", "loop", "wait", "script", "sql"]
      stepTypeMapping = objectFilter(stepTypes, stepContain)
      break
    default:
      stepTypeMapping = {}
  }
  return stepTypeMapping
}

export function objectFilter(obj, field) {
  let res = Object.entries(obj).filter(([key, val]) => field.includes(key))
  return Object.fromEntries(res)
}

export function getStepTypeInfo(stepType, type) {
  let obj = {
    script: {color: "#7B4D12FF", background: "#F1EEE9FF", icon: 'iconfont icon-code'},
    wait: {color: "#67C23AFF", background: "#F2F9EEFF", icon: 'iconfont icon-time'},
    api: {color: "#61649f", background: "#f5f5fa", icon: 'iconfont icon-c158API'},
    case: {color: "#f4664a", background: "#f5f5faFF", icon: 'iconfont icon-a-case-o1'},
    loop: {color: "#02A7F0FF", background: "#F4F4F5FF", icon: 'iconfont icon-loop'},
    extract: {color: "#015478FF", background: "#E6EEF2FF", icon: ''},
    sql: {color: "#783887FF", background: "#F2ECF3FF", icon: 'iconfont icon-suffix-sql'},
    if: {color: "#E6A23C", background: "#FCF6EE", icon: 'iconfont icon-fenzhijiedian'},
    timed_task: {color: "#AE445A", background: "#AE445A", icon: 'iconfont icon-time'},
  }
  return obj[stepType][type]
}