import pytest
from render import csm_seams as mod

CASES = [
    ("idx", 'm.cascade_index(5, [10, 20, 40]) == 0'),
    ("idx2", 'm.cascade_index(15, [10, 20, 40]) == 1'),
    ("ranges", 'm.split_ranges([10, 20, 40]) == [(0, 10), (10, 20), (20, 40)]'),
    ("hyst", 'm.hysteresis(1, 2, 2) == 1'),
    ("hyst2", 'm.hysteresis(1, 3, 2) == 3'),
    ("texel", 'm.texel_world_size(10, 100) == approx(0.2)'),
    ("kernel", 'm.filter_kernel(2, 4) == 16'),
    ("levels", 'm.update_levels(2) == [0, 1, 2]'),
    ("penumbra", 'm.penumbra_scale(8, 2) == approx(2.0)'),
    ("inside", 'm.inside_bounds((0, 0, 10, 10), (5, 5)) is True'),
    ("bias", 'm.depth_bias(0.01, 2) == approx(0.02)'),
    ("jitter", 'm.jitter_offset(5, 4) == approx(0.25)'),
    ("key", 'm.shadow_key("L", 2) == "L:2"'),
    ("extent", 'm.cascade_extent(2, 10) == 8'),
    ("clamp", 'm.clamp_cascade(5, 3) == 2')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
