

def assert_equal(exp, act):
    assert exp == act, f"预期结果: {exp} == 实际结果: {act}"


def assert_not_equal(exp, act):
    assert exp != act, f"预期结果: {exp} != 实际结果: {act}"


def assert_in(exp, act):
    assert exp in act, f"预期结果: {exp} in 实际结果: {act}"


def assert_not_in(exp, act):
    assert exp not in act, f"预期结果: {exp} not in 实际结果: {act}"


def assert_is(exp, act):
    assert exp is act, f"预期结果: {exp} is 实际结果: {act}"


def assert_is_not(exp, act):
    assert exp is not act, f"预期结果: {exp} is not 实际结果: {act}"


def assert_equal_count(exp, act):
    assert exp == len(act), f"预期数量: {exp} == 实际数量: {len(act)}"


def assert_greater(exp, act):
    assert exp > len(act), f"预期数量: {exp} > 实际数量: {len(act)}"


def assert_greater_equal(exp, act):
    assert exp >= len(act), f"预期数量: {exp} >= 实际数量: {len(act)}"


def assert_less_equal(exp, act):
    assert exp <= len(act), f"预期数量: {exp} <= 实际数量: {len(act)}"


def assert_less(exp, act):
    assert exp < len(act),  f"预期数量: {exp} < 实际数量: {len(act)}"
