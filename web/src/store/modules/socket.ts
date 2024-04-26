import Ws from "@/utils/socket";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useSocket = defineStore("socket", () => {
  // socket 实例
  const instance = ref(null);
  // socket 消息
  const socketData = ref(null);

  /**
   * @Author: shenjilin
   * @Date: 2022-07-29 15:43:45
   * @description: 订阅websocket消息
   * @param {string} type  消息类型
   * @return {*}
   */
  const wsSubscribe = (type) => {
    instance.value.subscribe(type, (data) => {
      console.log("接收服务端消息： ", data);
      // 每次接收到消息都会更新 socketData
      socketData.value = data;
    });
  };

  /**
   * @Author: shenjilin
   * @Date: 2022-07-29 15:46:14
   * @description: 发送消息
   * @param {*} data 消息体
   * @return {*}
   */
  const sendSocket = (data) => {
    instance.value.send(JSON.stringify(data));
  };

  /**
   * @Author: shenjilin
   * @Date: 2022-07-29 15:49:03
   * @description: 销毁
   * @return {*}
   */
  const destroySocket = () => {
    if (instance.value) {
      // 销毁socket
      instance.value.destroy();
      instance.value = null;
    }
  };

  /**
   * @Author: shenjilin
   * @Date: 2022-07-29 15:55:38
   * @description: socket 初始化
   * @param {*} url
   * @return {*} socket 实例
   */
  const wsInit = async (url) => {
    if (!instance.value) {
      const ws = new Ws(url);
      instance.value = ws;
      // 订阅type = notify 的消息
      wsSubscribe("notify");
    }
    return instance.value;
  };

  return {
    socketData,
    wsInit,
    sendSocket,
    destroySocket,
  };
});
