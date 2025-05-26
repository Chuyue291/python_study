from rpp import RangePlusPlus

def test_rpp():
    rpp = RangePlusPlus(1, 10, mapping=lambda x: x * 2, step=2, ascending=True, iter_type='list')
    assert str(rpp) == '[2, 6, 10, 14, 18]'
