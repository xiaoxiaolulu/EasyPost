from pydantic import BaseModel


class TestCaseResult(BaseModel):

    all: int
    success: int
    fail: int
    error: int
    cases: list
    res: str
    name: str
    state: str


class TestReport(BaseModel):

    class_list: list
    all: int
    success: int
    error: int
    fail: int
    runtime: str
    argtime: str
    begin_time: str
    pass_rate: float
    state: str
    tester: str
