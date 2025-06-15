

import math
from collections.abc import Callable
class Number(object):
    """
    Number 类型:统一处理数值计算的核心类

    主要特性:
    1. 统一的单值/多值操作接口
    2. 完整的数学运算符支持(+,-,*,/)
    3. 内置数值类型兼容性
    4. 丰富的数学函数库(sqrt, exp, log等)
    5. 支持数组式访问和比较
    6. 强大的数据分析功能
    """
    # 类主体
    __version__='1.9.8'
    def __init__(self, *value: int | float,show_mode:str='__visual__') -> None:
        """构造新的Number实例
        
        参数:
            *value: 一个或多个数值,支持以下形式:
                  - 单个数值: 创建单值对象
                  - 多个数值: 创建多值对象
            show_mode: 显示模式设置
                      - '__visual__': 带值标签显示(默认),如"value:1"
                      - '__value__': 仅显示数值,如"1"
        
        异常:
            ValueError: 未提供任何数值
            TypeError: 提供的值不是整数或浮点数
        """
        if not value:
            raise ValueError("Number must be initialized with at least one value")
        if not all(isinstance(v, (int, float)) for v in value):
            raise TypeError("All values must be int or float")
        # 如果只有一个值,直接存储该值；否则存储为元组
        self.value: int | float | tuple[int | float, ...] = value[0] if len(value) == 1 else value
        self.SM=show_mode
    
    def __str__(self) -> str:
        """返回对象的字符串表示
        
        Returns:
            str: 根据show_mode的不同返回不同格式:
                - '__visual__': 'value:值' 
                - '__value__': 仅值
                - 其他: 'NONE'
        """
        if self.SM=='__visual__':
            return f'value:{self.value}'
        elif self.SM=='__value__':
            return str(self.value)
        else:
            return 'NONE'

    def __repr__(self) -> str:
        """返回对象的详细字符串表示
        
        Returns:
            str: 构造器格式的字符串, 如:
                - 单值:Number(值)
                - 多值:Number(值1, 值2, ...)
        """
        if isinstance(self.value, (int, float)):
            return f'Number({self.value})'
        values_str = ', '.join(str(v) for v in self.value)
        return f'Number({values_str})'
    def __add__(self, other: "Number | int | float") -> 'Number' :
        """实现加法运算

        规则:
        1. Number + Number:
           - 单值+单值:直接相加
           - 多值+多值:对应位置相加(要求长度相同)
           - 单值+多值:不支持
        2. Number + int/float:
           - 单值:直接相加
           - 多值:每个元素都加上这个数

        Args:
            other: 另一个Number对象或数值

        Returns:
            新的Number对象,包含运算结果

        Raises:
            ValueError: 当试图将单值与多值相加,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相加时
        """
        if isinstance(other, Number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return Number(self.value + other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot add single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot add Numbers with different lengths")
            return Number(*(a + b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return Number(self.value + other)
            return Number(*(v + other for v in self.value))
        raise TypeError(f"Unsupported operand type for +: '{type(self).__name__}' and '{type(other).__name__}'")
    def __radd__(self, other: int | float) -> 'Number':

        """实现反向加法运算(当左操作数不是Number类型时被调用)

        用于支持 int/float + Number 的情况

        Args:
            other: 数值类型(int或float)

        Returns:
            新的Number对象,包含运算结果

        Raises:
            TypeError: 当左操作数不是int或float类型时
        """
        if isinstance(other, (int, float)):
            return self + other
        raise TypeError(f"Unsupported operand type for +: '{type(other).__name__}' and '{type(self).__name__}'")
    def __sub__(self, other: "Number | int | float") -> 'Number':
        """实现减法运算

        规则:
        1. Number - Number:
           - 单值-单值:直接相减
           - 多值-多值:对应位置相减(要求长度相同)
           - 单值-多值:不支持
        2. Number - int/float:
           - 单值:直接相减
           - 多值:每个元素都减去这个数

        Args:
            other: 另一个Number对象或数值

        Returns:
            新的Number对象,包含运算结果

        Raises:
            ValueError: 当试图将单值与多值相减,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相减时
        """
        if isinstance(other, Number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return Number(self.value - other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot subtract single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot subtract Numbers with different lengths")
            return Number(*(a - b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return Number(self.value - other)
            return Number(*(v - other for v in self.value))
        raise TypeError(f"Unsupported operand type for -: '{type(self).__name__}' and '{type(other).__name__}'")
    def __rsub__(self, other: int | float) -> 'Number':
        """实现反向减法运算(当左操作数不是Number类型时被调用)

        用于支持 int/float - Number 的情况

        规则:
        1. int/float - 单值: 直接相减
        2. int/float - 多值: 用这个数减去每个元素

        Args:
            other: 数值类型(int或float)

        Returns:
            新的Number对象,包含运算结果

        Raises:
            TypeError: 当左操作数不是int或float类型时
        """
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return Number(other - self.value)
            return Number(*(other - v for v in self.value))
        raise TypeError(f"Unsupported operand type for -: '{type(other).__name__}' and '{type(self).__name__}'")
    def __mul__(self, other: "Number | int | float") -> 'Number':
        """实现乘法运算

        规则:
        1. Number * Number:
           - 单值*单值:直接相乘
           - 多值*多值:对应位置相乘(要求长度相同)
           - 单值*多值:不支持
        2. Number * int/float:
           - 单值:直接相乘
           - 多值:每个元素都乘以这个数

        Args:
            other: 另一个Number对象或数值

        Returns:
            新的Number对象,包含运算结果

        Raises:
            ValueError: 当试图将单值与多值相乘,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相乘时
        """
        if isinstance(other, Number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return Number(self.value * other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot multiply single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot multiply Numbers with different lengths")
            return Number(*(a * b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return Number(self.value * other)
            return Number(*(v * other for v in self.value))
        raise TypeError(f"Unsupported operand type for *: '{type(self).__name__}' and '{type(other).__name__}'")
    def __rmul__(self, other: int | float) -> 'Number':
        """实现反向乘法运算(当左操作数不是Number类型时被调用)

        用于支持 int/float * Number 的情况
        由于乘法满足交换律,直接调用__mul__方法即可

        Args:
            other: 数值类型(int或float)

        Returns:
            新的Number对象,包含运算结果

        Raises:
            TypeError: 当左操作数不是int或float类型时
        """
        if isinstance(other, (int, float)):
            return self * other
        raise TypeError(f"Unsupported operand type for *: '{type(other).__name__}' and '{type(self).__name__}'")
    def __truediv__(self, other: "Number | int | float") ->'Number':
        """实现除法运算

        规则:
        1. Number / Number:
           - 单值/单值:直接相除
           - 多值/多值:对应位置相除(要求长度相同)
           - 单值/多值:不支持
        2. Number / int/float:
           - 单值:直接相除
           - 多值:每个元素都除以这个数

        Args:
            other: 另一个Number对象或数值

        Returns:
            新的Number对象,包含运算结果

        Raises:
            ValueError: 当试图将单值与多值相除,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相除时
            ZeroDivisionError: 当除数为零时
        """
        if isinstance(other, Number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                if other.value == 0:
                    raise ZeroDivisionError("Division by zero")
                return Number(self.value / other.value)
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot divide single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot divide Numbers with different lengths")
            if any(v == 0 for v in other.value):
                raise ZeroDivisionError("Division by zero")
            return Number(*(a / b for a, b in zip(self.value, other.value)))
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            if isinstance(self.value, (int, float)):
                return Number(self.value / other)
            return Number(*(v / other for v in self.value))
        raise TypeError(f"Unsupported operand type for /: '{type(self).__name__}' and '{type(other).__name__}'")
    def __rtruediv__(self, other: int | float) -> 'Number':
        """实现反向除法运算(当左操作数不是Number类型时被调用)

        用于支持 int/float / Number 的情况

        规则:
        1. int/float / 单值: 直接相除
        2. int/float / 多值: 用这个数除以每个元素

        Args:
            other: 数值类型(int或float)

        Returns:
            新的Number对象,包含运算结果

        Raises:
            TypeError: 当左操作数不是int或float类型时
            ZeroDivisionError: 当Number对象中包含零值时
        """
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                if self.value == 0:
                    raise ZeroDivisionError("Division by zero")
                return Number(other / self.value)
            if any(v == 0 for v in self.value):
                raise ZeroDivisionError("Division by zero")
            return Number(*(other / v for v in self.value))
        raise TypeError(f"Unsupported operand type for /: '{type(other).__name__}' and '{type(self).__name__}'")
    def __eq__(self, other: "Number | int | float") -> bool:
        """实现相等性比较

        规则:
        1. Number == Number:
           - 单值==单值:直接比较
           - 多值==多值:要求长度相同且对应位置的值都相等
           - 单值==多值:永远返回False
        2. Number == int/float:
           - 单值:直接比较
           - 多值:永远返回False

        Args:
            other: 另一个Number对象或数值

        Returns:
            bool: 是否相等
        """
        if isinstance(other, Number):
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
    def __lt__(self, other: "Number | int | float") -> bool:
        """实现小于比较

        规则:
        1. Number < Number:
           - 单值<单值:直接比较
           - 多值<多值:要求长度相同,按照元组比较规则进行比较
           - 单值<多值:不支持,抛出异常
        2. Number < int/float:
           - 单值:直接比较
           - 多值:不支持,抛出异常

        Args:
            other: 另一个Number对象或数值

        Returns:
            bool: 是否小于

        Raises:
            ValueError: 当试图比较单值和多值,或多值间长度不同时
            TypeError: 当使用不支持的类型进行比较时
        """
        if isinstance(other, Number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return self.value < other.value
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot compare single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot compare Numbers with different lengths")
            return tuple(self.value) < tuple(other.value)
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return self.value < other
            raise ValueError("Cannot compare multiple values with single value")
        raise TypeError(f"Cannot compare {type(self).__name__} with {type(other).__name__}")
    def __gt__(self, other: "Number | int | float") -> bool:
        """实现大于比较

        规则:
        1. Number > Number:
           - 单值>单值:直接比较
           - 多值>多值:要求长度相同,按照元组比较规则进行比较
           - 单值>多值:不支持,抛出异常
        2. Number > int/float:
           - 单值:直接比较
           - 多值:不支持,抛出异常

        Args:
            other: 另一个Number对象或数值

        Returns:
            bool: 是否大于

        Raises:
            ValueError: 当试图比较单值和多值,或多值间长度不同时
            TypeError: 当使用不支持的类型进行比较时
        """
        if isinstance(other, Number):
            if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
                return self.value > other.value
            if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
                raise ValueError("Cannot compare single value with multiple values")
            if len(self.value) != len(other.value):
                raise ValueError("Cannot compare Numbers with different lengths")
            return tuple(self.value) > tuple(other.value)
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return self.value > other
            raise ValueError("Cannot compare multiple values with single value")
        raise TypeError(f"Cannot compare {type(self).__name__} with {type(other).__name__}")
    def __le__(self, other: "Number | int | float") -> bool:
        """实现小于等于比较

        通过组合__lt__和__eq__的结果实现
        继承了这两个方法的所有规则和限制

        Args:
            other: 另一个Number对象或数值

        Returns:
            bool: 是否小于等于
        """
        return self < other or self == other

    def __ge__(self, other: "Number | int | float") -> bool:
        """实现大于等于比较

        通过组合__gt__和__eq__的结果实现
        继承了这两个方法的所有规则和限制

        Args:
            other: 另一个Number对象或数值

        Returns:
            bool: 是否大于等于
        """
        return self > other or self == other
    def __getitem__(self, index: int) -> int | float:
        """获取指定索引位置的值

        通过此方法实现下标访问语法(如: obj[0]),只适用于多值Number对象。
        对单值Number对象使用此方法会引发TypeError异常。

        Args:
            index: 要访问的索引位置

        Returns:
            int | float: 指定位置的数值

        Raises:
            TypeError: 当对单值Number对象使用索引操作时
            IndexError: 当索引超出范围时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot index single value")
        return self.value[index]

    def __setitem__(self, index: int, value: int | float) -> None:
        """设置指定索引位置的值

        通过此方法实现下标赋值语法(如: obj[0] = 1),只适用于多值Number对象。
        對單值Number對象使用此方法會引發TypeError異常。
        修改后的结果会被转换为tuple以保持不可变性。

        Args:
            index: 要设置的索引位置
            value: 要设置的新值,必须是int或float类型

        Raises:
            TypeError: 当对单值Number对象使用索引操作时,或value不是数值类型时
            IndexError: 当索引超出范围时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot index single value")
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be int or float")
        value_list = list(self.value)
        value_list[index] = value
        self.value = tuple(value_list)

    def __delitem__(self, index: int) -> None:
        """删除指定索引位置的值

        通过此方法实现del语句(如: del obj[0]),只适用于多值Number对象。
        对单值Number对象使用此方法会引发TypeError异常。
        删除后的结果会被转换为tuple以保持不可变性。

        Args:
            index: 要删除的索引位置

        Raises:
            TypeError: 当对单值Number对象使用索引操作时
            IndexError: 当索引超出范围时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot index single value")
        value_list = list(self.value)
        del value_list[index]
        self.value = tuple(value_list)

    # 数学方法
    def sqrt(self) -> 'Number':
        """返回平方根

        计算每个数值的平方根。对于单值Number对象直接计算,对于多值Number对象分别计算每个值的平方根。

        Returns:
            Number: 包含平方根结果的Number对象

        Raises:
            ValueError: 当试图计算负数的平方根时
        """
        if isinstance(self.value, (int, float)):
            if self.value < 0:
                raise ValueError("Cannot calculate square root of negative Number")
            return Number(math.sqrt(self.value))
        if any(v < 0 for v in self.value):
            raise ValueError("Cannot calculate square root of negative Number")
        return Number(*(math.sqrt(v) for v in self.value))

    def exp(self) -> 'Number':
        """返回e的self.value次方

        计算以自然对数e为底的指数函数值。对于单值Number对象直接计算,对于多值Number对象分别计算每个值。

        Returns:
            Number: 包含指数运算结果的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(math.exp(self.value))
        return Number(*(math.exp(v) for v in self.value))

    def log(self, base: float = math.e) -> 'Number':
        """返回以base为底的对数

        计算对数值。默认使用自然对数e作为底数,也可以指定其他正数作为底数。
        对于单值Number对象直接计算,对于多值Number对象分别计算每个值的对数。

        Args:
            base: 对数的底数,默认为自然对数e

        Returns:
            Number: 包含对数运算结果的Number对象

        Raises:
            ValueError: 当试图计算非正数的对数时
        """
        if isinstance(self.value, (int, float)):
            if self.value <= 0:
                raise ValueError("Cannot calculate logarithm of non-positive Number")
            return Number(math.log(self.value, base))
        if any(v <= 0 for v in self.value):
            raise ValueError("Cannot calculate logarithm of non-positive Number")
        return Number(*(math.log(v, base) for v in self.value))

    def sin(self) -> "Number":
        """返回正弦值

        计算正弦值。对于单值Number对象直接计算,对于多值Number对象分别计算每个值的正弦。
        输入值应为弧度制。

        Returns:
            Number: 包含正弦值的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(math.sin(self.value))
        return Number(*(math.sin(v) for v in self.value))

    def cos(self) -> "Number":
        """返回余弦值

        计算余弦值。对于单值Number对象直接计算,对于多值Number对象分别计算每个值的余弦。
        输入值应为弧度制。

        Returns:
            Number: 包含余弦值的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(math.cos(self.value))
        return Number(*(math.cos(v) for v in self.value))

    def tan(self) -> "Number":
        """返回正切值

        计算正切值。对于单值Number对象直接计算,对于多值Number对象分别计算每个值的正切。
        输入值应为弧度制。

        Returns:
            Number: 包含正切值的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(math.tan(self.value))
        return Number(*(math.tan(v) for v in self.value))

    # 实用方法
    def is_integer(self) -> bool:
        """判断是否全为整数

        检查Number对象中的所有值是否都是整数。对浮点数,会检查是否可以精确表示为整数
        (如1.0是整数,1.1不是)。

        Returns:
            bool: 如果所有值都是整数返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return isinstance(self.value, int) or float(self.value).is_integer()
        return all(isinstance(v, int) or float(v).is_integer() for v in self.value)

    def to_int(self) -> "Number":
        """转换为整数

        将所有值转换为整数类型。对浮点数会进行截断操作(向零取整)。

        Returns:
            Number: 包含转换后整数值的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(int(self.value))
        return Number(*(int(v) for v in self.value))

    def to_float(self) -> "Number":
        """转换为浮点数

        将所有值转换为浮点数类型。整数会被转换为等值的浮点数。

        Returns:
            Number: 包含转换后浮点数值的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(float(self.value))
        return Number(*(float(v) for v in self.value))

    def factorial(self) -> "Number":
        """计算阶乘

        计算每个值的阶乘。只对非负整数有定义。

        Returns:
            Number: 包含阶乘计算结果的Number对象

        Raises:
            ValueError: 当值为负数或非整数时
        """
        if isinstance(self.value, (int, float)):
            if not (isinstance(self.value, int) or float(self.value).is_integer()) or self.value < 0:
                raise ValueError("Factorial is only defined for non-negative integers")
            return Number(math.factorial(int(self.value)))
        if not self.is_integer() or any(v < 0 for v in self.value):
            raise ValueError("Factorial is only defined for non-negative integers")
        return Number(*(math.factorial(int(v)) for v in self.value))

    def is_positive(self) -> bool:
        """判断是否全为正数

        检查Number对象中的所有值是否都大于0。

        Returns:
            bool: 如果所有值都大于0返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return self.value > 0
        return all(v > 0 for v in self.value)

    def is_negative(self) -> bool:
        """判断是否全为负数

        检查Number对象中的所有值是否都小于0。

        Returns:
            bool: 如果所有值都小于0返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return self.value < 0
        return all(v < 0 for v in self.value)

    def is_zero(self) -> bool:
        """判断是否全为零

        检查Number对象中的所有值是否都等于0。

        Returns:
            bool: 如果所有值都等于0返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return self.value == 0
        return all(v == 0 for v in self.value)
    def __hash__(self) -> int:
        """实现哈希函数,使Number对象可以用作字典键或集合元素

        规则:
        - 只有单值Number对象可以被哈希
        - 多值Number对象不可哈希,会引发TypeError

        Returns:
            int: 哈希值

        Raises:
            TypeError: 当尝试对多值Number对象进行哈希操作时
        """
        if isinstance(self.value, (int, float)):
            return hash(self.value)
        raise TypeError("unhashable type: 'Number' with multiple values")

    def __len__(self) -> int:
        """返回Number对象包含的值的数量

        Returns:
            int: 单值Number对象返回1,多值Number对象返回其包含的值的数量
        """
        if isinstance(self.value, (int, float)):
            return 1
        return len(self.value)

    def __neg__(self) -> 'Number':
        """实现一元负号操作

        Returns:
            Number: 包含所有值的相反数的新Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(-self.value)
        return Number(*(-v for v in self.value))

    def __pos__(self) -> 'Number':
        """实现一元正号操作(保持值不变)

        Returns:
            Number: 包含相同值的新Number对象
        """
        return Number(*self.value) if isinstance(self.value, tuple) else Number(self.value)

    def __abs__(self) -> 'Number':
        """返回绝对值

        Returns:
            Number: 包含所有值的绝对值的新Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(abs(self.value))
        return Number(*(abs(v) for v in self.value))

    def __pow__(self, power: "Number | int | float") -> 'Number':
        """实现幂运算

        Args:
            power: 指数值,可以是Number对象或数值类型

        Returns:
            Number: 包含幂运算结果的新Number对象

        Raises:
            ValueError: 当Number对象为多值而指数为单值,或反之时
            TypeError: 当使用不支持的类型作为指数时
        """
        if isinstance(power, Number):
            if isinstance(self.value, (int, float)) and isinstance(power.value, (int, float)):
                return Number(self.value ** power.value)
            if isinstance(self.value, (int, float)) or isinstance(power.value, (int, float)):
                raise ValueError("Cannot use single value with multiple values in power operation")
            if len(self.value) != len(power.value):
                raise ValueError("Cannot use Numbers with different lengths in power operation")
            return Number(*(a ** b for a, b in zip(self.value, power.value)))
        if isinstance(power, (int, float)):
            if isinstance(self.value, (int, float)):
                return Number(self.value ** power)
            return Number(*(v ** power for v in self.value))
        raise TypeError(f"Unsupported operand type for **: '{type(self).__name__}' and '{type(power).__name__}'")

    def __rpow__(self, other: int | float) -> 'Number':
        """实现反向幂运算

        Args:
            other: 底数,必须是数值类型

        Returns:
            Number: 包含幂运算结果的新Number对象

        Raises:
            TypeError: 当底数不是数值类型时
            ValueError: 当Number对象包含多个值时
        """
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return Number(other ** self.value)
            raise ValueError("Cannot use multiple values as exponent with single base")
        raise TypeError(f"Unsupported operand type for **: '{type(other).__name__}' and '{type(self).__name__}'")

    def delitem(self, *indices: int) -> None:
        """删除多个指定索引位置的值

        Args:
            *indices: 要删除的索引位置列表

        Raises:
            TypeError: 当对单值Number对象使用此方法时
            IndexError: 当索引超出范围时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot delete items from single value")
        value_list = list(self.value)
        # 从大到小排序索引,以避免删除元素后索引位置变化导致的问题
        for index in sorted(indices, reverse=True):
            del value_list[index]
        self.value = tuple(value_list) if value_list else 0

    def append(self, value: int | float) -> None:
        """添加一个值到Number对象末尾

        Args:
            value: 要添加的数值

        Raises:
            TypeError: 当value不是数值类型时
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be int or float")
        if isinstance(self.value, (int, float)):
            self.value = (self.value, value)
        else:
            value_list = list(self.value)
            value_list.append(value)
            self.value = tuple(value_list)

    def extend(self, values: "list | tuple | Number") -> None:
        """扩展Number对象,添加多个值

        Args:
            values: 要添加的值,可以是列表、元组或另一个Number对象

        Raises:
            TypeError: 当values中包含非数值类型元素时
        """
        if isinstance(values, Number):
            if isinstance(values.value, (int, float)):
                self.append(values.value)
            else:
                self.extend(values.value)
        else:
            if not all(isinstance(v, (int, float)) for v in values):
                raise TypeError("All values must be int or float")
            if isinstance(self.value, (int, float)):
                self.value = (self.value, *values)
            else:
                value_list = list(self.value)
                value_list.extend(values)
                self.value = tuple(value_list)



    def item_round(self, ndigits: int = 0) -> "Number":
        """对所有值进行四舍五入

        Args:
            ndigits: 保留的小数位数,默认为0

        Returns:
            Number: 包含四舍五入后值的新Number对象

        """
        if isinstance(self.value, (int, float)):
            return Number(round(self.value, ndigits))
        return Number(*(round(v, ndigits) for v in self.value))

    def sum(self) -> int | float:
        """计算所有值的总和

        Returns:
            int | float: 单值直接返回,多值返回所有值的和
        """
        if isinstance(self.value, (int, float)):
            return self.value
        return sum(self.value)

    def mean(self) -> float:
        """计算算术平均值

        Returns:
            float: 所有值的算术平均值
        """
        if isinstance(self.value, (int, float)):
            return float(self.value)
        return sum(self.value) / len(self.value)

    def max(self) -> int | float:
        """返回最大值

        Returns:
            int | float: 所有值中的最大值
        """
        if isinstance(self.value, (int, float)):
            return self.value
        return max(self.value)

    def min(self) -> int | float:
        """返回最小值

        Returns:
            int | float: 所有值中的最小值
        """
        if isinstance(self.value, (int, float)):
            return self.value
        return min(self.value)
    def gcd(self, other: "Number") -> "Number":
        """计算最大公约数

        如果是多值Number对象,则对应位置的数字计算最大公约数。
        要求所有数字都是整数。

        Args:
            other: 另一个Number对象

        Returns:
            Number: 包含最大公约数的Number对象

        Raises:
            TypeError: 当参数类型不正确时
            ValueError: 当值不是整数时
        """
        def _gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return abs(a)

        if not isinstance(other, Number):
            raise TypeError("Argument must be a Number object")

        if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
            if not (float(self.value).is_integer() and float(other.value).is_integer()):
                raise ValueError("Values must be integers")
            return Number(_gcd(int(self.value), int(other.value)))

        if len(self) != len(other):
            raise ValueError("Cannot calculate GCD of Numbers with different lengths")

        if not all(float(v).is_integer() for v in self.value + other.value):
            raise ValueError("All values must be integers")

        return Number(*[_gcd(int(a), int(b)) for a, b in zip(self.value, other.value)])

    def lcm(self, other: "Number") -> "Number":
        """计算最小公倍数

        如果是多值Number对象,则对应位置的数字计算最小公倍数。
        要求所有数字都是整数。

        Args:
            other: 另一个Number对象

        Returns:
            Number: 包含最小公倍数的Number对象

        Raises:
            TypeError: 当参数类型不正确时
            ValueError: 当值不是整数时
            ZeroDivisionError: 当任一数为0时
        """
        def _lcm(a: int, b: int) -> int:
            if a == 0 or b == 0:
                raise ZeroDivisionError("Cannot calculate LCM with zero")
            return abs(a * b) // math.gcd(a, b)

        if not isinstance(other, Number):
            raise TypeError("Argument must be a Number object")

        if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
            if not (float(self.value).is_integer() and float(other.value).is_integer()):
                raise ValueError("Values must be integers")
            return Number(_lcm(int(self.value), int(other.value)))

        if len(self) != len(other):
            raise ValueError("Cannot calculate LCM of Numbers with different lengths")

        if not all(float(v).is_integer() for v in self.value + other.value):
            raise ValueError("All values must be integers")

        return Number(*[_lcm(int(a), int(b)) for a, b in zip(self.value, other.value)])

    def abs(self) -> "Number":
        """返回绝对值

        Returns:
            Number: 包含绝对值的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(abs(self.value))
        return Number(*(abs(v) for v in self.value))

    def power(self, n: int) -> "Number":
        """计算幂

        计算每个数的n次方。

        Args:
            n: 指数,必须是整数

        Returns:
            Number: 包含幂运算结果的Number对象

        Raises:
            TypeError: 当n不是整数时
        """
        if not isinstance(n, int):
            raise TypeError("Exponent must be an integer")

        if isinstance(self.value, (int, float)):
            return Number(pow(self.value, n))
        return Number(*(pow(v, n) for v in self.value))

    def average(self) -> float:
        """计算平均值

        Returns:
            float: 所有元素的平均值
        """
        if isinstance(self.value, (int, float)):
            return float(self.value)
        return sum(self.value) / len(self.value)


    def count(self, value: int | float) -> int:
        """计算指定值出现的次数

        Args:
            value: 要计数的值

        Returns:
            int: 值出现的次数
        """
        if isinstance(self.value, (int, float)):
            return 1 if self.value == value else 0
        return sum(1 for v in self.value if v == value)

    def median(self) -> float:
        """计算中位数

        如果元素个数为奇数,返回中间的数;
        如果元素个数为偶数,返回中间两个数的平均值.

        Returns:
            float: 中位数

        Raises:
            TypeError: 当对象为单值Number时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot calculate median of single value")
        sorted_values = sorted(self.value)
        n = len(sorted_values)
        if n % 2 == 0:
            return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        return float(sorted_values[n//2])

    def mode(self) -> "Number":
        """计算众数(出现次数最多的值)

        如果有多个众数,全部返回。

        Returns:
            Number: 包含众数的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(self.value)

        from collections import Counter
        counts = Counter(self.value)
        max_freq = max(counts.values())
        modes = tuple(num for num, freq in counts.items() if freq == max_freq)
        return Number(*modes)

    def variance(self) -> float:
        """计算方差

        Returns:
            float: 方差

        Raises:
            TypeError: 当对象为单值Number时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot calculate variance of single value")

        avg = self.average()
        return sum((x - avg) ** 2 for x in self.value) / len(self.value)

    def std_dev(self) -> float:
        """计算标准差

        Returns:
            float: 标准差

        Raises:
            TypeError: 当对象为单值Number时
        """
        return math.sqrt(self.variance())

    def normalize(self) -> "Number":
        """归一化处理

        将所有值缩放到[0,1]区间。
        如果所有值相同,则返回全0序列。

        Returns:
            Number: 归一化后的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(1.0)

        min_val = min(self.value)
        max_val = max(self.value)
        if min_val == max_val:
            return Number(*(0.0 for _ in self.value))
        return Number(*((x - min_val) / (max_val - min_val) for x in self.value))

    def unique(self) -> "Number":
        """返回去重后的值

        保持原有顺序。

        Returns:
            Number: 去重后的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(self.value)
        seen = []
        for x in self.value:
            if x not in seen:
                seen.append(x)
        return Number(*seen)


    def product(self) -> int | float:
        """计算所有元素的乘积

        Returns:
            int | float: 所有元素的乘积
        """
        if isinstance(self.value, (int, float)):
            return self.value

        result = 1
        for v in self.value:
            result *= v
        return result

    def cumulative_product(self) -> "Number":
        """计算累积乘积

        返回一个新的Number对象,其中每个位置包含到该位置为止所有数的乘积。

        Returns:
            Number: 累积乘积的Number对象
        """
        if isinstance(self.value, (int, float)):
            return Number(self.value)

        result = []
        product = 1
        for x in self.value:
            product *= x
            result.append(product)
        return Number(*result)

    def item_filter(self, predicate: callable) -> "Number":
        """筛选满足条件的元素

        Args:
            predicate: 接受一个数值并返回布尔值的函数

        Returns:
            Number: 包含所有满足条件的元素的新Number对象
        """
        if isinstance(self.value, (int, float)):
            if predicate(self.value):
                return Number(self.value)
            # 如果单值不满足条件,返回空值会有问题,所以返回0
            return Number(0)

        filtered = [v for v in self.value if predicate(v)]
        if not filtered:
            return Number(0)  # 如果没有满足条件的元素,返回0
        return Number(*filtered)



    def reduce(self, func: callable, initial=None) -> int | float:
        """使用指定函数对序列进行归约操作

        Args:
            func: 接受两个参数并返回一个值的函数
            initial: 初始值,如果不指定则使用序列第一个元素

        Returns:
            归约操作的结果

        Raises:
            ValueError: 当对象为空且没有提供初始值时
        """
        if isinstance(self.value, (int, float)):
            if initial is None:
                return self.value
            return func(initial, self.value)

        from functools import reduce
        return reduce(func, self.value, initial)

    def zip_with(self, other: "Number", func: callable) -> "Number":
        """将两个Number对象的元素通过指定函数组合

        Args:
            other: 另一个Number对象
            func: 接受两个参数并返回一个值的函数

        Returns:
            Number: 组合结果的新Number对象

        Raises:
            ValueError: 当两个对象长度不同时
            TypeError: 当参数类型不正确时
        """
        if not isinstance(other, Number):
            raise TypeError("First argument must be a Number object")

        if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
            return Number(func(self.value, other.value))

        if isinstance(self.value, (int, float)) or isinstance(other.value, (int, float)):
            raise ValueError("Cannot zip single value with multiple values")

        if len(self.value) != len(other.value):
            raise ValueError("Cannot zip Numbers with different lengths")

        return Number(*(func(a, b) for a, b in zip(self.value, other.value)))

    def slice(self, start: int = None, stop: int = None, step: int = None) -> "Number":
        """返回指定切片的新Number对象

        Args:
            start: 起始索引,默认为0
            stop: 结束索引(不含),默认为长度
            step: 步长,默认为1

        Returns:
            Number: 包含切片元素的新Number对象

        Raises:
            TypeError: 当对单值Number使用此方法时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot slice single value")

        sliced = self.value[slice(start, stop, step)]
        if not sliced:  # 如果切片为空
            return Number(0)
        if len(sliced) == 1:  # 如果只有一个元素
            return Number(sliced[0])
        return Number(*sliced)

    def distinct_count(self) -> int:
        """计算不同值的数量

        Returns:
            int: 不同值的数量
        """
        if isinstance(self.value, (int, float)):
            return 1
        return len(set(self.value))

    def to_list(self) -> list:
        """转换为Python列表

        Returns:
            list: 包含所有值的Python列表
        """
        if isinstance(self.value, (int, float)):
            return [self.value]
        return list(self.value)

    def to_tuple(self) -> tuple:
        """转换为Python元组

        Returns:
            tuple: 包含所有值的Python元组
        """
        if isinstance(self.value, (int, float)):
            return (self.value,)
        return self.value

    def to_set(self) -> set:
        """转换为Python集合

        Returns:
            set: 包含所有不同值的Python集合
        """
        if isinstance(self.value, (int, float)):
            return {self.value}
        return set(self.value)

    def to_dict(self, keys=None) -> dict:
        """转换为Python字典

        Args:
            keys: 可选的键列表,如果提供,则使用这些键作为字典键
                 如果不提供,则使用索引作为键

        Returns:
            dict: 字典表示形式

        Raises:
            ValueError: 当keys的长度与值的数量不匹配时
        """
        if keys is None:
            if isinstance(self.value, (int, float)):
                return {0: self.value}
            return {i: v for i, v in enumerate(self.value)}

        if isinstance(self.value, (int, float)):
            if len(keys) != 1:
                raise ValueError("Number of keys must match number of values")
            return {keys[0]: self.value}

        if len(keys) != len(self.value):
            raise ValueError("Number of keys must match number of values")
        return {k: v for k, v in zip(keys, self.value)}

    def item_map(self, func) -> 'Number':
        """对Number对象中的每个元素应用函数

        Args:
            func: 接受一个数值并返回一个数值的函数

        Returns:
            Number: 包含映射后结果的新Number对象

        Raises:
            TypeError: 当func不是可调用对象时
        """
        if not callable(func):
            raise TypeError('func must be a function object')
            
        if isinstance(self.value, (int, float)):
            return Number(*(func(self.value)))
        else:
            return Number(*(func(v) for v in self.value))
    
    def __or__(self, other:'Number') -> 'Number':
        """位或运算符(|)的重载，对两个 Number 对象的对应元素执行或操作"""
        return self.zip_with(other, lambda a, b: a | b)
    
    def __and__(self, other:'Number') -> 'Number':
        """位与运算符(&)的重载，对两个 Number 对象的对应元素执行与操作"""
        return self.zip_with(other, lambda a, b: a & b)

    def __xor__(self, other:'Number') -> 'Number':
        """位异或运算符(^)的重载，对两个 Number 对象的对应元素执行异或操作"""
        return self.zip_with(other, lambda a, b: a ^ b)

    def __invert__(self) -> 'Number':
        """位反运算符(~)的重载，对 Number 对象的每个元素执行取反操作"""
        return self.item_map(lambda x: ~x)

    def __lshift__(self, other:'Number') -> 'Number':
        """左移运算符(<<)的重载，对两个 Number 对象的对应元素执行左移操作"""
        return self.zip_with(other, lambda a, b: a << b)

    def __rshift__(self, other:'Number') -> 'Number':
        """右移运算符(>>)的重载，对两个 Number 对象的对应元素执行右移操作"""
        return self.zip_with(other, lambda a, b: a >> b)

    def __iadd__(self, other:'Number') -> 'Number':
        """复合加法赋值运算符(+=)的重载，执行原地加法操作"""
        return self.zip_with(other, lambda a, b: a + b)

    def __isub__(self, other:'Number') -> 'Number':
        """复合减法赋值运算符(-=)的重载，执行原地减法操作"""
        return self.zip_with(other, lambda a, b: a - b)

    def __imul__(self, other:'Number') -> 'Number':
        """复合乘法赋值运算符(*=)的重载，执行原地乘法操作"""
        return self.zip_with(other, lambda a, b: a * b)

    def __itruediv__(self, other:'Number') -> 'Number':
        """复合除法赋值运算符(/=)的重载，执行原地除法操作"""
        return self.zip_with(other, lambda a, b: a / b)

    def __ifloordiv__(self, other:'Number') -> 'Number':
        """复合整除赋值运算符(//=)的重载，执行原地整除操作"""
        return self.zip_with(other, lambda a, b: a // b)

    def __imod__(self, other:'Number') -> 'Number':
        """复合取模赋值运算符(%=)的重载，执行原地取模操作"""
        return self.zip_with(other, lambda a, b: a % b)

    def __ipow__(self, other:'Number') -> 'Number':
        """复合幂运算赋值运算符(**=)的重载，执行原地幂运算"""
        return self.zip_with(other, lambda a, b: a ** b)

    def __ior__(self, other:'Number') -> 'Number':
        """复合位或赋值运算符(|=)的重载，执行原地位或操作"""
        return self.zip_with(other, lambda a, b: a | b)

    def __ixor__(self, other:'Number') -> 'Number':
        """复合位异或赋值运算符(^=)的重载，执行原地位异或操作"""
        return self.zip_with(other, lambda a, b: a ^ b)

    def __iand__(self, other:'Number') -> 'Number':
        """复合位与赋值运算符(&=)的重载，执行原地位与操作"""
        return self.zip_with(other, lambda a, b: a & b)

    def __ilshift__(self, other:'Number') -> 'Number':
        """复合左移赋值运算符(<<=)的重载，执行原地左移操作"""
        return self.zip_with(other, lambda a, b: a << b)

    def __irshift__(self, other:'Number') -> 'Number':
        """复合右移赋值运算符(>>=)的重载，执行原地右移操作"""
        return self.zip_with(other, lambda a, b: a >> b)

    def __rshift__(self, other) -> 'Number':
        """右移运算符的重载，对两个 Number 对象的对应元素执行右移操作"""
        return self.zip_with(other, lambda a, b: b >> a)



    def bin(self) -> str | list:
        """返回Number对象的二进制表示形式
        
        Returns:
            str | list: 如果是单值返回该值的二进制字符串表示，
                    如果是多值返回包含每个值的二进制字符串表示的列表
        """
        if isinstance(self.value, (int, float)):
            return bin(int(self.value))
        return [bin(int(v)) for v in self.value]

    def hex(self) -> str | list:
        """返回Number对象的十六进制表示形式
        
        Returns:
            str | list: 如果是单值返回该值的十六进制字符串表示，
                    如果是多值返回包含每个值的十六进制字符串表示的列表
        """
        if isinstance(self.value, (int, float)):
            return hex(int(self.value))
        return [hex(int(v)) for v in self.value]

    def oct(self) -> str | list:
        """返回Number对象的八进制表示形式
        
        Returns:
            str | list: 如果是单值返回该值的八进制字符串表示，
                    如果是多值返回包含每个值的八进制字符串表示的列表
        """
        if isinstance(self.value, (int, float)):
            return oct(int(self.value))
        return [oct(int(v)) for v in self.value]

    def moving_average(self, window_size: int) -> 'Number':
        """计算移动平均值

        使用指定大小的滑动窗口计算移动平均值。对单值返回其本身,
        对多值返回一个新的Number对象,其长度比原序列少window_size-1。

        Args:
            window_size (int): 窗口大小,必须为正整数且不大于序列长度

        Returns:
            Number: 包含移动平均值的新Number对象

        Raises:
            ValueError: 当window_size小于1或大于序列长度时
            TypeError: 当对单值Number使用此方法时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot calculate moving average of single value")

        if not isinstance(window_size, int) or window_size < 1:
            raise ValueError("Window size must be a positive integer")

        if window_size > len(self.value):
            raise ValueError("Window size cannot be larger than sequence length")

        if window_size == 1:
            return self

        # 计算移动平均
        result = []
        for i in range(len(self.value) - window_size + 1):
            window = self.value[i:i + window_size]
            avg = sum(window) / window_size
            result.append(avg)

        return Number(*result)

    def cumulative_stats(self) -> dict[str, 'Number']:
        """计算累积统计量

        计算序列的累积统计量,包括：
        - 累积和
        - 累积均值
        - 累积最大值
        - 累积最小值

        Returns:
            dict[str, Number]: 包含各种累积统计量的字典：
                - 'sum': 累积和
                - 'mean': 累积均值
                - 'max': 累积最大值
                - 'min': 累积最小值

        Raises:
            TypeError: 当对单值Number使用此方法时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot calculate cumulative stats of single value")

        cum_sum = []
        cum_mean = []
        cum_max = []
        cum_min = []

        current_sum = 0
        for i, v in enumerate(self.value, 1):
            current_sum += v
            cum_sum.append(current_sum)
            cum_mean.append(current_sum / i)
            cum_max.append(max(self.value[:i]))
            cum_min.append(min(self.value[:i]))

        return {
            'sum': Number(*cum_sum),
            'mean': Number(*cum_mean),
            'max': Number(*cum_max),
            'min': Number(*cum_min)
        }



    @classmethod
    def linspace(cls,start: float, stop: float, num: int = 50) -> 'Number':
        """生成等距序列

        在指定的区间[start, stop]内生成num个等距的数。
        这是一个类方法,不需要实例化即可调用。

        Args:
            start (float): 序列的起始值
            stop (float): 序列的结束值
            num (int): 要生成的数的个数,默认为50

        Returns:
            Number: 包含等距序列的Number对象

        Raises:
            ValueError: 当num小于1时
        """
        if num < 1:
            raise ValueError("Number of points must be at least 1")

        if num == 1:
            return Number(start)

        step = (stop - start) / (num - 1)
        return cls(*(start + i * step for i in range(num)))

    # 一些静态方法
    @staticmethod
    def add(numbers_a:list[int|float],numbers_b:list[int|float]) -> list[int|float]:
        """对两个列表中的对应元素执行加法操作

        Args:
            numbers_a (list[int|float]): 第一个列表
            numbers_b (list[int|float]): 第二个列表

        Returns:
            list[int|float]: 包含对应元素加法结果的列表
        """
        return [a + b for a, b in zip(numbers_a, numbers_b)]

    @staticmethod
    def sub(numbers_a:list[int|float],numbers_b:list[int|float]) -> list[int|float]:
        """对两个列表中的对应元素执行减法操作

        Args:
            numbers_a (list[int|float]): 第一个列表
            numbers_b (list[int|float]): 第二个列表
        Returns:
            list[int|float]: 包含对应元素减法结果的列表
        """
        return [a - b for a, b in zip(numbers_a, numbers_b)]

    @staticmethod
    def mul(numbers_a:list[int|float],numbers_b:list[int|float]) -> list[int|float]:
        """对两个列表中的对应元素执行乘法操作

        Args:
            numbers_a (list[int|float]): 第一个列表
            numbers_b (list[int|float]): 第二个列表

        Returns:
            list[int|float]: 包含对应元素乘法结果的列表
        """
        return [a * b for a, b in zip(numbers_a, numbers_b)]

    @staticmethod
    def div(numbers_a:list[int|float],numbers_b:list[int|float]) -> list[int|float]:
        """对两个列表中的对应元素执行除法操作

        Args:
            numbers_a (list[int|float]): 第一个列表
            numbers_b (list[int|float]): 第二个列表
        Returns:
            list[int|float]: 包含对应元素除法结果的列表
        """
        return [a / b for a, b in zip(numbers_a, numbers_b)]

    @staticmethod
    def pow(numbers_a:list[int|float],numbers_b:list[int|float]) -> list[int|float]:
        """对两个列表中的对应元素执行幂运算

        Args:
            numbers_a (list[int|float]): 第一个列表
            numbers_b (list[int|float]): 第二个列表

        Returns:
            list[int|float]: 包含对应元素幂运算结果的列表
        """
        return [a ** b for a, b in zip(numbers_a, numbers_b)]

    @staticmethod
    def mod(numbers_a:list[int|float],numbers_b:list[int|float]) -> list[int|float]:
        """对两个列表中的对应元素执行取模运算

        Args:
            numbers_a (list[int|float]): 第一个列表
            numbers_b (list[int|float]): 第二个列表

        Returns:
            list[int|float]: 包含对应元素取模运算结果的列表
        """
        return [a % b for a, b in zip(numbers_a, numbers_b)]

    @staticmethod
    def stacount(numbers:list[int|float],value:int|float) -> int:
        """统计列表中指定值的个数

        Args:
            numbers (list[int|float]): 要统计的列表
            value (int|float): 要统计的值

        Returns:
            int: 指定值的个数
        """
        return numbers.count(value)

    @staticmethod
    def stazip_with(numbers_a:list[int|float],numbers_b:list[int|float],func:Callable) -> list[int|float]:
        """对两个列表中的对应元素执行指定函数操作

        Args:
            numbers_a (list[int|float]): 第一个列表
            numbers_b (list[int|float]): 第二个列表
            func (Callable[int|float,int|float]): 要执行的函数

        Returns:
            list[int|float]: 包含对应元素函数操作结果的列表
        """
        return [func(a, b) for a, b in zip(numbers_a, numbers_b)]

    @staticmethod
    def stamax(numbers:list[int|float]) -> int|float:
        """返回列表中的最大值

        Args:
            numbers (list[int|float]): 要查找最大值的列表

        Returns:
            int|float: 列表中的最大值
        """
        return max(numbers)

    @staticmethod
    def stamin(numbers:list[int|float]) -> int|float:
        """返回列表中的最小值

        Args:
            numbers (list[int|float]): 要查找最小值的列表

        Returns:
            int|float: 列表中的最小值
        """
        return min(numbers)

    @staticmethod
    def stasum(numbers:list[int|float]) -> int|float:
        """返回列表中所有元素的和

        Args:
            numbers (list[int|float]): 要计算和的列表

        Returns:
            int|float: 列表中所有元素的和
        """
        return sum(numbers)

    @staticmethod
    def staaverage(numbers:list[int|float]) -> int|float:
        """返回列表中所有元素的平均值

        Args:
            numbers (list[int|float]): 要计算平均值的列表

        Returns:
            int|float: 列表中所有元素的平均值
        """
        return sum(numbers) / len(numbers)

    @staticmethod
    def stabin(number:int|float) -> str:
        """将整数或浮点数转换为二进制字符串

        Args:
            number (int|float): 要转换的整数或浮点数

        Returns:
            str: 二进制字符串
        """
        return bin(int(number))[1:]

    @staticmethod
    def stahex(number:int|float) -> str:
        """将整数或浮点数转换为十六进制字符串

        Args:
            number (int|float): 要转换的整数或浮点数

        Returns:
            str: 十六进制字符串
        """
        return hex(int(number))[2:]

    @staticmethod
    def staoct(number:int|float) -> str:
        """将整数或浮点数转换为八进制字符串

        Args:
            number (int|float): 要转换的整数或浮点数

        Returns:
            str: 八进制字符串
        """
        return oct(int(number))[2:]

    @staticmethod
    def round(number:int|float,ndigits:int=0) -> int|float:
        """将浮点数四舍五入为指定的小数位数

        Args:
            number (int|float): 要四舍五入的浮点数
            ndigits (int, optional): 要保留的小数位数. Defaults to 0.

        Returns:
            int|float: 四舍五入后的结果
        """
        return round(number,ndigits)

    def __round__(self, n=None):
        return round(*self.value, n)



if __name__ == "__main__":
    a=Number(9,8,7,show_mode='__value__')
    print(a.count(1))
    print(Number.__version__)
    print(a.bin())
    b=Number(9,0.9,1,2,4,5,2,7.92,show_mode='__value__')
    print(b.average())
