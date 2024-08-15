from pydantic import BaseModel
from pydantic.fields import Field


class TestCaseResult(BaseModel):

    all: int = Field(0, description="用例总数")
    success: int = Field(0, description="用例成功数")
    fail: int = Field(0, description="用例失败数")
    error: int = Field(0, description="用例错误数")
    cases: list = Field([], description="具体步骤")
    name: str = Field("", description="用例名称")
    state: str = Field("", description="用例状态")


class TestReport(BaseModel):

    class_list: list = Field([], description="测试场景")
    all: int = Field(0, description="场景总数")
    success: int = Field(0, description="场景成功数")
    error: int = Field(0, description="用例错误数")
    fail: int = Field(0, description="用例失败数")
    runtime: str = Field("", description="运行时间")
    argtime: str = Field("", description="平均时间")
    begin_time: str = Field("", description="开始时间")
    pass_rate: str = Field("0", description="通过率")
    state: str = Field("", description="场景状态")
    tester: str = Field("", description="测试人员")
