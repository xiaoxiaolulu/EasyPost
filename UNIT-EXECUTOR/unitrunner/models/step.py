import typing
from pydantic import (
    BaseModel,
    Field
)
from unitrunner.models import (
    Name,
    MethodEnum,
    Url,
    Headers
)


class TStepBase(BaseModel):
    """步骤基类"""

    sort: int = Field(0, description="排序")
    case_id: typing.Union[str, int] = Field(None, description="用例id")
    name: Name = Field("", description="步骤名称")


class ExtractData(BaseModel):
    """提取模型"""

    rename: str = Field("", description="提取变量命名")
    name: str = Field("", description="提取变量名称")
    path: str = Field("", description="提取路径")
    extract_type: str = Field("", description="提取类型 jmespath jsonpath")


class ValidatorData(BaseModel):
    """验证模式"""
    actual: typing.Any = Field(None, description="校验值")
    comparator: str = Field(None, description="比较器")
    expect: typing.Any = Field(None, description="预期值")


class Interface(BaseModel):
    url: Url = Field(..., description="请求url")
    name: Name = Field("", description="接口名称")
    method: typing.Union[str, MethodEnum] = Field(..., description="请求方法")


class Raw(BaseModel):
    params: typing.Dict[str, str] = Field(None, description="参数")
    re_json: typing.Union[typing.Dict, typing.List, str] = Field(None, description="json数据", alias='json')
    data: typing.Union[str, typing.Dict[str, typing.Any]] = Field(None, description="data数据")


class TRequest(BaseModel):

    """api 请求模型"""
    title: Name = Field("", description="接口名称")
    interface: Interface = Field(..., description="接口配置")
    headers: Headers = Field({}, description="请求头")
    request: Raw = Field({}, description="请求参数")
    setup_script: str = Field(None, description="前置脚本")
    teardown_script: str = Field(None, description="前置脚本")
    extract: typing.List[ExtractData] = Field([], description="提取")
    validators: typing.List[ValidatorData] = Field([], description="断言")


class TStep(TStepBase):
    """步骤模型"""
    request: TRequest = Field(None, description="请求信息")
    children: typing.List['TStep'] = Field([], description="子步骤")


class TestCase(BaseModel):
    """用例模型"""

    name: Name = Field("", description="用例名称")
    cases: typing.List[typing.Union[TStep]] = Field(..., description="用例步骤")
