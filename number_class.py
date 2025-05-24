import math

class number:
    def __init__(self, *value: int | float) -> None:
        if not value:
            raise ValueError("number must be initialized with at least one value")
        if not all(isinstance(v, (int, float)) for v in value):
            raise TypeError("All values must be int or float")
        # 如果只有一个值，直接存储该值；否则存储为元组
        self.value: int | float | tuple[int | float, ...] = value[0] if len(value) == 1 else value
    
    def __str__(self) -> str:
        return f'value:{self.value}'
    
    def __repr__(self) -> str:
        if isinstance(self.value, (int, float)):
            return f'number({self.value})'
        values_str = ', '.join(str(v) for v in self.value)
        return f'number({values_str})'

    def __add__(self, other: "number | int | float") -> "number":
        if isinstance(other, number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return number(self.value + other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot add single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot add numbers with different lengths")
            return number(*(a + b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return number(self.value + other)
            return number(*(v + other for v in self.value))
        raise TypeError(f"Unsupported operand type for +: '{type(self).__name__}' and '{type(other).__name__}'")

    def __radd__(self, other: int | float) -> "number":
        if isinstance(other, (int, float)):
            return self + other
        raise TypeError(f"Unsupported operand type for +: '{type(other).__name__}' and '{type(self).__name__}'")

    def __sub__(self, other: "number | int | float") -> "number":
        if isinstance(other, number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return number(self.value - other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot subtract single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot subtract numbers with different lengths")
            return number(*(a - b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return number(self.value - other)
            return number(*(v - other for v in self.value))
        raise TypeError(f"Unsupported operand type for -: '{type(self).__name__}' and '{type(other).__name__}'")

    def __rsub__(self, other: int | float) -> "number":
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return number(other - self.value)
            return number(*(other - v for v in self.value))
        raise TypeError(f"Unsupported operand type for -: '{type(other).__name__}' and '{type(self).__name__}'")

    def __mul__(self, other: "number | int | float") -> "number":
        if isinstance(other, number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return number(self.value * other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot multiply single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot multiply numbers with different lengths")
            return number(*(a * b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return number(self.value * other)
            return number(*(v * other for v in self.value))
        raise TypeError(f"Unsupported operand type for *: '{type(self).__name__}' and '{type(other).__name__}'")

    def __rmul__(self, other: int | float) -> "number":
        if isinstance(other, (int, float)):
            return self * other
        raise TypeError(f"Unsupported operand type for *: '{type(other).__name__}' and '{type(self).__name__}'")

    def __truediv__(self, other: "number | int | float") -> "number":
        if isinstance(other, number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                if other.value == 0:
                    raise ZeroDivisionError("Division by zero")
                return number(self.value / other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot divide single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot divide numbers with different lengths")
            if any(v == 0 for v in other.value):
                raise ZeroDivisionError("Division by zero")
            return number(*(a / b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            if isinstance(self.value, (int, float)):
                return number(self.value / other)
            return number(*(v / other for v in self.value))
        raise TypeError(f"Unsupported operand type for /: '{type(self).__name__}' and '{type(other).__name__}'")

    def __rtruediv__(self, other: int | float) -> "number":
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                if self.value == 0:
                    raise ZeroDivisionError("Division by zero")
                return number(other / self.value)
            if any(v == 0 for v in self.value):
                raise ZeroDivisionError("Division by zero")
            return number(*(other / v for v in self.value))
        raise TypeError(f"Unsupported operand type for /: '{type(other).__name__}' and '{type(self).__name__}'")

    def __eq__(self, other: "number | int | float") -> bool:
        if isinstance(other, number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return self.value == other.value
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                return False
            if len(self.value) != len(other.value):
                return False
            return all(a == b for a, b in zip(self.value, other.value))
        if isinstance(other, (int, float)):
            return isinstance(self.value, (int, float)) and self.value == other
        return False

    def __lt__(self, other: "number | int | float") -> bool:
        if isinstance(other, number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return self.value < other.value
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot compare single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot compare numbers with different lengths")
            return tuple(self.value) < tuple(other.value)
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return self.value < other
            raise ValueError("Cannot compare multiple values with single value")
        raise TypeError(f"Cannot compare {type(self).__name__} with {type(other).__name__}")

    def __gt__(self, other: "number | int | float") -> bool:
        if isinstance(other, number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return self.value > other.value
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot compare single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot compare numbers with different lengths")
            return tuple(self.value) > tuple(other.value)
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return self.value > other
            raise ValueError("Cannot compare multiple values with single value")
        raise TypeError(f"Cannot compare {type(self).__name__} with {type(other).__name__}")

    def __le__(self, other: "number | int | float") -> bool:
        return self < other or self == other

    def __ge__(self, other: "number | int | float") -> bool:
        return self > other or self == other

    # 数学方法
    def sqrt(self) -> "number":
        """返回平方根"""
        if isinstance(self.value, (int, float)):
            if self.value < 0:
                raise ValueError("Cannot calculate square root of negative number")
            return number(math.sqrt(self.value))
        if any(v < 0 for v in self.value):
            raise ValueError("Cannot calculate square root of negative number")
        return number(*(math.sqrt(v) for v in self.value))

    def exp(self) -> "number":
        """返回e的self.value次方"""
        if isinstance(self.value, (int, float)):
            return number(math.exp(self.value))
        return number(*(math.exp(v) for v in self.value))

    def log(self, base: float = math.e) -> "number":
        """返回以base为底的对数"""
        if isinstance(self.value, (int, float)):
            if self.value <= 0:
                raise ValueError("Cannot calculate logarithm of non-positive number")
            return number(math.log(self.value, base))
        if any(v <= 0 for v in self.value):
            raise ValueError("Cannot calculate logarithm of non-positive number")
        return number(*(math.log(v, base) for v in self.value))

    def sin(self) -> "number":
        """返回正弦值"""
        if isinstance(self.value, (int, float)):
            return number(math.sin(self.value))
        return number(*(math.sin(v) for v in self.value))

    def cos(self) -> "number":
        """返回余弦值"""
        if isinstance(self.value, (int, float)):
            return number(math.cos(self.value))
        return number(*(math.cos(v) for v in self.value))

    def tan(self) -> "number":
        """返回正切值"""
        if isinstance(self.value, (int, float)):
            return number(math.tan(self.value))
        return number(*(math.tan(v) for v in self.value))

    # 实用方法
    def is_integer(self) -> bool:
        """判断是否全为整数"""
        if isinstance(self.value, (int, float)):
            return isinstance(self.value, int) or float(self.value).is_integer()
        return all(isinstance(v, int) or float(v).is_integer() for v in self.value)

    def to_int(self) -> "number":
        """转换为整数"""
        if isinstance(self.value, (int, float)):
            return number(int(self.value))
        return number(*(int(v) for v in self.value))

    def to_float(self) -> "number":
        """转换为浮点数"""
        if isinstance(self.value, (int, float)):
            return number(float(self.value))
        return number(*(float(v) for v in self.value))

    def factorial(self) -> "number":
        """计算阶乘"""
        if isinstance(self.value, (int, float)):
            if not (isinstance(self.value, int) or float(self.value).is_integer()) or self.value < 0:
                raise ValueError("Factorial is only defined for non-negative integers")
            return number(math.factorial(int(self.value)))
        if not self.is_integer() or any(v < 0 for v in self.value):
            raise ValueError("Factorial is only defined for non-negative integers")
        return number(*(math.factorial(int(v)) for v in self.value))

    def is_positive(self) -> bool:
        """判断是否全为正数"""
        if isinstance(self.value, (int, float)):
            return self.value > 0
        return all(v > 0 for v in self.value)

    def is_negative(self) -> bool:
        """判断是否全为负数"""
        if isinstance(self.value, (int, float)):
            return self.value < 0
        return all(v < 0 for v in self.value)

    def is_zero(self) -> bool:
        """判断是否全为零"""
        if isinstance(self.value, (int, float)):
            return self.value == 0
        return all(v == 0 for v in self.value)

    def isnt_zero(self) -> bool:
        """判断是否存在非零值"""
        if isinstance(self.value, (int, float)):
            return self.value != 0
        return any(v != 0 for v in self.value)
    @classmethod
    def create(cls,lst:list[str]|tuple[str]) -> "number":
        """"String列表转number"""
        return cls(*(eval(i) for i in lst))
    def ceil(self) -> "number":
        """返回向上取整"""
        if isinstance(self.value, (tuple)):
            return number(*(math.ceil(float(v)) for v in self.value))
        else:
            raise TypeError('Not a number(int or float)')
    def floor(self) -> "number":
        """返回向下取整"""
        if isinstance(self.value, (tuple)):
            return number(*(math.floor(v) for v in self.value))
        else:
            raise TypeError('Not a number(int or float)')
    def round(self) -> "number":
        """返回四舍五入"""
        if isinstance(self.value, (tuple)):
            return number(*(round(v) for v in self.value))
        else:
            raise TypeError('Not a number(int or float)')
    def is_even(self) -> tuple[bool]:
        """判断是否全为偶数"""
        if isinstance(self.value, (tuple)):
            return tuple(v % 2 == 0 for v in self.value)
        else:
            raise TypeError('Not a number(int or float)')
    def is_odd(self) -> tuple[bool]:
        """判断是否全为奇数"""
        if isinstance(self.value, (tuple)):
            return tuple(v % 2 == 1 for v in self.value)
        else:
            raise TypeError('Not a number(int or float)')
# 测试代码
if __name__ == "__main__":
    # 单值测试
    a = number(5)
    b = number(3)
    print(f"Single value tests:")
    print(f"a = {a}, b = {b}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"a > b: {a > b}")
    print(f"a == b: {a == b}")
    print(f"sqrt(a) = {a.sqrt()}")
    print(f"factorial(a) = {a.factorial()}")
    print()
    
    # 多值测试
    c = number(1, 2, 3)
    d = number(4, 5, 6)
    print(f"Multiple value tests:")
    print(f"c = {c}, d = {d}")
    print(f"c + d = {c + d}")
    print(f"c - d = {c - d}")
    print(f"c * d = {c * d}")
    print(f"c / d = {c / d}")
    print(f"c < d: {c < d}")
    print(f"c == d: {c == d}")
    print(f"sqrt(c) = {c.sqrt()}")
    print(f"exp(c) = {c.exp()}")
    print(d.__class__==number)
    a=number.create(['1+8', '2+8', '3+8'])
    print(a)
    b=number.create(['1+8.0', '2+8.85', '3+8.0'])
    print(b)
    
