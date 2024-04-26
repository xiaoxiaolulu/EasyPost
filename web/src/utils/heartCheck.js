//心跳检测
export default {
  timeout: 1000 * 6, //6秒
  timeoutObj: null,
  serverTimeoutObj: null,
  reset: function () {
    this.timeoutObj && clearTimeout(this.timeoutObj);
    this.serverTimeoutObj && clearTimeout(this.serverTimeoutObj);
    return this;
  },
  start: function (socket) {
    var self = this;
    this.timeoutObj = setTimeout(function () {
      //这里发送一个心跳，后端收到后，返回一个心跳消息，
      //onmessage拿到返回的心跳就说明连接正常
      socket.send("ping");
      //如果超过一定时间还没重置，说明后端主动断开了
      self.serverTimeoutObj = setTimeout(function () {
        //如果onclose会执行reconnect，我们执行ws.close()就行了.
        //如果直接执行reconnect 会触发onclose导致重连两次
        socket.close();
      }, self.timeout);
    }, this.timeout);
  },
};
