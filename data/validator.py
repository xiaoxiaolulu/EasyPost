

def equal(exp, act):
    assert exp == act, f"预期结果: {exp} == 实际结果: {act}"


def not_equal(exp, act):
    assert exp != act, f"预期结果: {exp} != 实际结果: {act}"


def contains(exp, act):
    assert exp in act, f"预期结果: {exp} in 实际结果: {act}"


def not_contains(exp, act):
    assert exp not in act, f"预期结果: {exp} not in 实际结果: {act}"


def length_eq(exp, act):
    assert exp == len(act), f"预期数量: {exp} == 实际数量: {len(act)}"


def length_gt(exp, act):
    assert exp > len(act), f"预期数量: {exp} > 实际数量: {len(act)}"


def length_ge(exp, act):
    assert exp >= len(act), "预期数量: {exp} >= 实际数量: {len(act)}"


def length_le(exp, act):
    assert exp <= len(act), f"预期数量: {exp} <= 实际数量: {len(act)}"


def length_lt(exp, act):
    assert exp < len(act),  f"预期数量: {exp} < 实际数量: {len(act)}"
