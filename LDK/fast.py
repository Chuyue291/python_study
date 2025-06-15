from time import time
from numpy import sum as nsum
def get_time(looping_number:int=5):
    def deco(func):
        def wrapper(*args, **kwargs):
            start = time()
            for _ in range(looping_number):
                func(*args, **kwargs)
            end = time()
            print(f"{func.__name__} took {end-start} seconds")
        return wrapper
    return deco

@get_time(1)
def inside():
    print(sum(range(int(1e7))))
@get_time(1)
def outside():
    print(nsum(range(int(1e7))))

inside();outside()