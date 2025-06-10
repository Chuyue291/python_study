def a(lst:list):
    for i in lst:
        if isinstance(i,list):
            yield from a(i)
        else:
            yield i

print(list(a([7,[9,8]])))