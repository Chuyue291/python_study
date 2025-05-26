from number_class import number

def test_number_operators()  -> None:
    a = number(1,2,3,4)
    assert a.is_square_of_any_number(number(2,2,3,4),2) == (False,)*4

def test_delitem() -> None:
    # 测试基本的remove功能
    a = number(1,2,3,4)
    a.remove(index=1)
    assert a == number(1,3,4)
    
    # 测试多元素删除
    b = number(1,2,3,4,5)
    b.remove(index=[1,3])
    assert b == number(1,3,5)
    
    # 测试使用负索引
    c = number(1,2,3,4)
    c.remove([-1, 0])  # 移除最后一个和第一个元素
    assert c == number(2,3)
    
    # 测试链式调用
    d = number(1,2,3,4,5)
    result = d.remove([0,1]).remove(index=-1)
    assert result == number(3,4)
    
    # 测试参数优先级
    e = number(1,2,3,4)
    e.remove(value=0, index=1)  # index应该优先
    assert e == number(1,3,4)

def test_number_add() -> None:
    a = number(1,2,3,4)
    b = number(5,6,7,8)
    assert a.add(b,index=0) == number(5,6,7,8,1,2,3,4)

