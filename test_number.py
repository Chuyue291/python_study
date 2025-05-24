from number_class import number

def test_number_oerators()  -> None:
    a=number(15,8,9,7.7)
    assert a.is_even() == (False,True,False,False)