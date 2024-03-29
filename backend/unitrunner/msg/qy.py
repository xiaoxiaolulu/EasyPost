from typing import (
    List,
)
from pydantic import (
    BaseModel,
    Field
)
from unitrunner.request.http_handler import HttpHandler


class Headers(BaseModel):
    content_type: str = 'application/json'


class Source(BaseModel):
    icon_url: str = None
    desc: str = 'EasyPost'
    desc_color: int = 0


class MainTitle(BaseModel):
    title: str = None
    desc: str = None


class ContentList(BaseModel):
    keyname: str = None
    value: str = None


class Action(BaseModel):
    type: int = 0
    url: str = None
    title: str = None


class TemplateCard(BaseModel):
    card_type: str = 'text_notice'
    source: Source
    main_title: MainTitle
    emphasis_content: MainTitle
    horizontal_content_list: List[ContentList]
    jump_list: List[Action]
    card_action: Action


class Params(BaseModel):
    msgtype: str = 'template_card'
    template_card: TemplateCard


class Webhook(BaseModel):
    url: str = None
    method: str = 'POST'
    headers: Headers
    params: Params = Field(alias='json')


class QyWeixin:

    @staticmethod
    def run(**kwargs):
        request_body = Webhook(**kwargs)
        http_request = HttpHandler(request_body.dict(by_alias=True))
        response = http_request.request().get('responseBody', None)
        status = response.get('errcode', None)
        if int(status):
            raise Exception('企业微信通知发送失败！')


if __name__ == '__main__':
    q = QyWeixin()
    q.run(url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b08dc3fd-e6ca-4a4e-8f34-7067340b0646',
          headers={'Content-Type': 'application/json'},
          json={
              "msgtype": "template_card",
              "template_card": {
                  "card_type": "text_notice",
                  "source": {
                      "icon_url": "https://image-c.weimobwmc.com/saas-wxbiz/bf25b403fb7d414f83e57865dc038812.png",
                      "desc": "EasyPost",
                      "desc_color": 0
                  },
                  "main_title": {
                      "title": "测试报告",
                      "desc": "券码Openapi自动化测试"
                  },
                  "emphasis_content": {
                      "title": "100%",
                      "desc": "通过率"
                  },
                  "horizontal_content_list": [
                      {
                          "keyname": "脚本类型",
                          "value": "接口自动化测试"
                      },
                      {
                          "keyname": "开始时间",
                          "value": "2022-11-16 18:05:35"
                      },
                      {
                          "keyname": "用例总数",
                          "value": 4
                      }, {
                          "keyname": "用例通过",
                          "value": 4
                      }, {
                          "keyname": "用例失败",
                          "value": 4
                      }, {
                          "keyname": "用例跳过",
                          "value": 4
                      },
                  ],
                  "jump_list": [
                      {
                          "type": 0,
                          "url": "http://marketingtesttool.internal.weimobqa.com/#/polling",
                          "title": "查看测试报告"
                      }
                  ],
                  "card_action": {
                      "type": 1,
                      "url": "http://marketingtesttool.internal.weimobqa.com/#/polling",
                  }
              }
          }
          )
