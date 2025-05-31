"""
number类:一个灵活的数值处理类,支持单值和多值操作
特性:
1. 支持单个数值和多个数值的统一操作
2. 实现了基本的算术运算(加减乘除)
3. 支持与普通数值类型的混合运算
4. 提供了丰富的数学函数(平方根、指数、对数等
5. 实现了比较运算和索引操作
6. 包含实用的数值判断方法(是否为整数、正数、负数等)
"""

import math

class number:    
    def __init__(self, *value: int | float) -> None:
        """初始化number对象
        
        Args:
            *value: 可变参数,接受一个或多个数值
                   - 单个数值时:创建单值number对象
                   - 多个数值时:创建多值number对象(内部使用元组存储)
        
        Raises:
            ValueError: 如果没有提供任何值
            TypeError: 如果提供的值不是整数或浮点数
        """
        if not value:
            raise ValueError("number must be initialized with at least one value")
        if not all(isinstance(v, (int, float)) for v in value):
            raise TypeError("All values must be int or float")
        # 如果只有一个值,直接存储该值；否则存储为元组
        self.value: int | float | tuple[int | float, ...] = value[0] if len(value) == 1 else value
    def __str__(self) -> str:
        """返回对象的字符串表示
        
        Returns:
            str: 格式为 'value:值' 的字符串
        """
        return f'value:{self.value}'
    
    def __repr__(self) -> str:
        """返回对象的详细字符串表示,可用于重建对象
        
        返回格式:
        - 单值:number(值)
        - 多值:number(值1, 值2, ...)
        
        Returns:
            str: 可以用于重建对象的字符串表示
        """
        if isinstance(self.value, (int, float)):
            return f'number({self.value})'
        values_str = ', '.join(str(v) for v in self.value)
        return f'number({values_str})'
    def __add__(self, other: "number | int | float") -> "number":
        """实现加法运算
        
        规则:
        1. number + number:
           - 单值+单值:直接相加
           - 多值+多值:对应位置相加(要求长度相同)
           - 单值+多值:不支持
        2. number + int/float:
           - 单值:直接相加
           - 多值:每个元素都加上这个数
           
        Args:
            other: 另一个number对象或数值
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            ValueError: 当试图将单值与多值相加,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相加时
        """
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
        """实现反向加法运算(当左操作数不是number类型时被调用)
        
        用于支持 int/float + number 的情况
        
        Args:
            other: 数值类型(int或float)
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            TypeError: 当左操作数不是int或float类型时
        """
        if isinstance(other, (int, float)):
            return self + other
        raise TypeError(f"Unsupported operand type for +: '{type(other).__name__}' and '{type(self).__name__}'")    
    def __sub__(self, other: "number | int | float") -> "number":
        """实现减法运算
        
        规则:
        1. number - number:
           - 单值-单值:直接相减
           - 多值-多值:对应位置相减(要求长度相同)
           - 单值-多值:不支持
        2. number - int/float:
           - 单值:直接相减
           - 多值:每个元素都减去这个数
           
        Args:
            other: 另一个number对象或数值
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            ValueError: 当试图将单值与多值相减,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相减时
        """
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
        """实现反向减法运算(当左操作数不是number类型时被调用)
        
        用于支持 int/float - number 的情况
        
        规则:
        1. int/float - 单值: 直接相减
        2. int/float - 多值: 用这个数减去每个元素
        
        Args:
            other: 数值类型(int或float)
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            TypeError: 当左操作数不是int或float类型时
        """
        if isinstance(other, (int, float)):
            if isinstance(self.value, (int, float)):
                return number(other - self.value)
            return number(*(other - v for v in self.value))
        raise TypeError(f"Unsupported operand type for -: '{type(other).__name__}' and '{type(self).__name__}'")    
    def __mul__(self, other: "number | int | float") -> "number":
        """实现乘法运算
        
        规则:
        1. number * number:
           - 单值*单值:直接相乘
           - 多值*多值:对应位置相乘(要求长度相同)
           - 单值*多值:不支持
        2. number * int/float:
           - 单值:直接相乘
           - 多值:每个元素都乘以这个数
           
        Args:
            other: 另一个number对象或数值
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            ValueError: 当试图将单值与多值相乘,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相乘时
        """
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
        """实现反向乘法运算(当左操作数不是number类型时被调用)
        
        用于支持 int/float * number 的情况
        由于乘法满足交换律,直接调用__mul__方法即可
        
        Args:
            other: 数值类型(int或float)
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            TypeError: 当左操作数不是int或float类型时
        """
        if isinstance(other, (int, float)):
            return self * other
        raise TypeError(f"Unsupported operand type for *: '{type(other).__name__}' and '{type(self).__name__}'")    
    def __truediv__(self, other: "number | int | float") -> "number":
        """实现除法运算
        
        规则:
        1. number / number:
           - 单值/单值:直接相除
           - 多值/多值:对应位置相除(要求长度相同)
           - 单值/多值:不支持
        2. number / int/float:
           - 单值:直接相除
           - 多值:每个元素都除以这个数
           
        Args:
            other: 另一个number对象或数值
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            ValueError: 当试图将单值与多值相除,或多值间长度不同时
            TypeError: 当使用不支持的类型进行相除时
            ZeroDivisionError: 当除数为零时
        """
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
        """实现反向除法运算(当左操作数不是number类型时被调用)
        
        用于支持 int/float / number 的情况
        
        规则:
        1. int/float / 单值: 直接相除
        2. int/float / 多值: 用这个数除以每个元素
        
        Args:
            other: 数值类型(int或float)
            
        Returns:
            新的number对象,包含运算结果
            
        Raises:
            TypeError: 当左操作数不是int或float类型时
            ZeroDivisionError: 当number对象中包含零值时
        """
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
        """实现相等性比较
        
        规则:
        1. number == number:
           - 单值==单值:直接比较
           - 多值==多值:要求长度相同且对应位置的值都相等
           - 单值==多值:永远返回False
        2. number == int/float:
           - 单值:直接比较
           - 多值:永远返回False
           
        Args:
            other: 另一个number对象或数值
            
        Returns:
            bool: 是否相等
        """
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
        """实现小于比较
        
        规则:
        1. number < number:
           - 单值<单值:直接比较
           - 多值<多值:要求长度相同,按照元组比较规则进行比较
           - 单值<多值:不支持,抛出异常
        2. number < int/float:
           - 单值:直接比较
           - 多值:不支持,抛出异常
           
        Args:
            other: 另一个number对象或数值
            
        Returns:
            bool: 是否小于
            
        Raises:
            ValueError: 当试图比较单值和多值,或多值间长度不同时
            TypeError: 当使用不支持的类型进行比较时
        """
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
        """实现大于比较
        
        规则:
        1. number > number:
           - 单值>单值:直接比较
           - 多值>多值:要求长度相同,按照元组比较规则进行比较
           - 单值>多值:不支持,抛出异常
        2. number > int/float:
           - 单值:直接比较
           - 多值:不支持,抛出异常
           
        Args:
            other: 另一个number对象或数值
            
        Returns:
            bool: 是否大于
            
        Raises:
            ValueError: 当试图比较单值和多值,或多值间长度不同时
            TypeError: 当使用不支持的类型进行比较时
        """
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
        """实现小于等于比较
        
        通过组合__lt__和__eq__的结果实现
        继承了这两个方法的所有规则和限制
        
        Args:
            other: 另一个number对象或数值
            
        Returns:
            bool: 是否小于等于
        """
        return self < other or self == other

    def __ge__(self, other: "number | int | float") -> bool:
        """实现大于等于比较
        
        通过组合__gt__和__eq__的结果实现
        继承了这两个方法的所有规则和限制
        
        Args:
            other: 另一个number对象或数值
            
        Returns:
            bool: 是否大于等于
        """
        return self > other or self == other    
    def __getitem__(self, index: int) -> int | float:
        """获取指定索引位置的值

        通过此方法实现下标访问语法(如: obj[0]),只适用于多值number对象。
        对单值number对象使用此方法会引发TypeError异常。
        
        Args:
            index: 要访问的索引位置
            
        Returns:
            int | float: 指定位置的数值
            
        Raises:
            TypeError: 当对单值number对象使用索引操作时
            IndexError: 当索引超出范围时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot index single value")
        return number(self.value[index])
    
    def __setitem__(self, index: int, value: int | float) -> None:
        """设置指定索引位置的值

        通过此方法实现下标赋值语法(如: obj[0] = 1),只适用于多值number对象。
        對單值number對象使用此方法會引發TypeError異常。
        修改后的结果会被转换为tuple以保持不可变性。
        
        Args:
            index: 要设置的索引位置
            value: 要设置的新值,必须是int或float类型
            
        Raises:
            TypeError: 当对单值number对象使用索引操作时,或value不是数值类型时
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

        通过此方法实现del语句(如: del obj[0]),只适用于多值number对象。
        对单值number对象使用此方法会引发TypeError异常。
        删除后的结果会被转换为tuple以保持不可变性。
        
        Args:
            index: 要删除的索引位置
            
        Raises:
            TypeError: 当对单值number对象使用索引操作时
            IndexError: 当索引超出范围时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot index single value")
        value_list = list(self.value)
        del value_list[index]
        self.value = tuple(value_list)

    # 数学方法
    def sqrt(self) -> "number":
        """返回平方根
        
        计算每个数值的平方根。对于单值number对象直接计算,对于多值number对象分别计算每个值的平方根。
        
        Returns:
            number: 包含平方根结果的number对象
            
        Raises:
            ValueError: 当试图计算负数的平方根时
        """
        if isinstance(self.value, (int, float)):
            if self.value < 0:
                raise ValueError("Cannot calculate square root of negative number")
            return number(math.sqrt(self.value))
        if any(v < 0 for v in self.value):
            raise ValueError("Cannot calculate square root of negative number")
        return number(*(math.sqrt(v) for v in self.value))

    def exp(self) -> "number":
        """返回e的self.value次方
        
        计算以自然对数e为底的指数函数值。对于单值number对象直接计算,对于多值number对象分别计算每个值。
        
        Returns:
            number: 包含指数运算结果的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(math.exp(self.value))
        return number(*(math.exp(v) for v in self.value))

    def log(self, base: float = math.e) -> "number":
        """返回以base为底的对数
        
        计算对数值。默认使用自然对数e作为底数,也可以指定其他正数作为底数。
        对于单值number对象直接计算,对于多值number对象分别计算每个值的对数。
        
        Args:
            base: 对数的底数,默认为自然对数e
            
        Returns:
            number: 包含对数运算结果的number对象
            
        Raises:
            ValueError: 当试图计算非正数的对数时
        """
        if isinstance(self.value, (int, float)):
            if self.value <= 0:
                raise ValueError("Cannot calculate logarithm of non-positive number")
            return number(math.log(self.value, base))
        if any(v <= 0 for v in self.value):
            raise ValueError("Cannot calculate logarithm of non-positive number")
        return number(*(math.log(v, base) for v in self.value))

    def sin(self) -> "number":
        """返回正弦值
        
        计算正弦值。对于单值number对象直接计算,对于多值number对象分别计算每个值的正弦。
        输入值应为弧度制。
        
        Returns:
            number: 包含正弦值的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(math.sin(self.value))
        return number(*(math.sin(v) for v in self.value))

    def cos(self) -> "number":
        """返回余弦值
        
        计算余弦值。对于单值number对象直接计算,对于多值number对象分别计算每个值的余弦。
        输入值应为弧度制。
        
        Returns:
            number: 包含余弦值的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(math.cos(self.value))
        return number(*(math.cos(v) for v in self.value))

    def tan(self) -> "number":
        """返回正切值
        
        计算正切值。对于单值number对象直接计算,对于多值number对象分别计算每个值的正切。
        输入值应为弧度制。
        
        Returns:
            number: 包含正切值的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(math.tan(self.value))
        return number(*(math.tan(v) for v in self.value))

    # 实用方法
    def is_integer(self) -> bool:
        """判断是否全为整数
        
        检查number对象中的所有值是否都是整数。对浮点数,会检查是否可以精确表示为整数
        (如1.0是整数,1.1不是)。
        
        Returns:
            bool: 如果所有值都是整数返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return isinstance(self.value, int) or float(self.value).is_integer()
        return all(isinstance(v, int) or float(v).is_integer() for v in self.value)

    def to_int(self) -> "number":
        """转换为整数
        
        将所有值转换为整数类型。对浮点数会进行截断操作(向零取整)。
        
        Returns:
            number: 包含转换后整数值的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(int(self.value))
        return number(*(int(v) for v in self.value))

    def to_float(self) -> "number":
        """转换为浮点数
        
        将所有值转换为浮点数类型。整数会被转换为等值的浮点数。
        
        Returns:
            number: 包含转换后浮点数值的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(float(self.value))
        return number(*(float(v) for v in self.value))

    def factorial(self) -> "number":
        """计算阶乘
        
        计算每个值的阶乘。只对非负整数有定义。
        
        Returns:
            number: 包含阶乘计算结果的number对象
            
        Raises:
            ValueError: 当值为负数或非整数时
        """
        if isinstance(self.value, (int, float)):
            if not (isinstance(self.value, int) or float(self.value).is_integer()) or self.value < 0:
                raise ValueError("Factorial is only defined for non-negative integers")
            return number(math.factorial(int(self.value)))
        if not self.is_integer() or any(v < 0 for v in self.value):
            raise ValueError("Factorial is only defined for non-negative integers")
        return number(*(math.factorial(int(v)) for v in self.value))

    def is_positive(self) -> bool:
        """判断是否全为正数
        
        检查number对象中的所有值是否都大于0。
        
        Returns:
            bool: 如果所有值都大于0返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return self.value > 0
        return all(v > 0 for v in self.value)

    def is_negative(self) -> bool:
        """判断是否全为负数
        
        检查number对象中的所有值是否都小于0。
        
        Returns:
            bool: 如果所有值都小于0返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return self.value < 0
        return all(v < 0 for v in self.value)

    def is_zero(self) -> bool:
        """判断是否全为零
        
        检查number对象中的所有值是否都等于0。
        
        Returns:
            bool: 如果所有值都等于0返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return self.value == 0
        return all(v == 0 for v in self.value)

    def isnt_zero(self) -> bool:
        """判断是否存在非零值
        
        检查number对象中是否存在不等于0的值。
        
        Returns:
            bool: 如果存在任何不等于0的值返回True,否则返回False
        """
        if isinstance(self.value, (int, float)):
            return self.value != 0
        return any(v != 0 for v in self.value)
    
    @classmethod
    def create(cls, lst: list[str] | tuple[str]) -> "number":
        """String列表转number
        
        将包含数学表达式字符串的列表或元组转换为number对象。
        表达式会被eval函数计算,因此必须是合法的Python表达式。
        为安全起见,不允许使用__import__。
        
        Args:
            lst: 包含数学表达式字符串的列表或元组
            
        Returns:
            number: 包含计算结果的number对象
            
        Raises:
            ValueError: 当输入包含不安全的表达式时
        """
        if  not '__import__' in lst:  
            return cls(*(float(eval(i)) for i in lst))
        raise ValueError("Input must be a list or tuple of strings representing numbers")

    def ceil(self) -> "number":
        """返回向上取整
        
        对每个值进行向上取整操作,返回大于或等于该值的最小整数。
        
        Returns:
            number: 包含向上取整结果的number对象
            
        Raises:
            TypeError: 当值不是数值类型时
        """
        if isinstance(self.value, (tuple, int, float)):
            return number(*(math.ceil(float(v)) for v in self.value))
        else:
            raise TypeError('Not a number(int, float, or tuple)')

    def floor(self) -> "number":
        """返回向下取整
        
        对每个值进行向下取整操作,返回小于或等于该值的最大整数。
        
        Returns:
            number: 包含向下取整结果的number对象
            
        Raises:
            TypeError: 当值不是数值类型时
        """
        if isinstance(self.value, (tuple, int, float)):
            return number(*(math.floor(v) for v in self.value))
        else:
            raise TypeError('Not a number(int, float, or tuple)')

    def round(self) -> "number":
        """返回四舍五入的结果
        
        对每个值进行四舍五入操作,返回最接近的整数。
        
        Returns:
            number: 包含四舍五入结果的number对象
            
        Raises:
            TypeError: 当值不是数值类型时
        """
        if isinstance(self.value, (tuple, int, float)):
            if isinstance(self.value, (int, float)):
                return number(round(self.value))
            return number(*(round(v) for v in self.value))
        else:
            raise TypeError('Not a number(int, float, or tuple)')

    def is_even(self) -> tuple[bool]:
        """判断是否全为偶数
        
        检查每个值是否为偶数。值会被转换为整数进行判断。
        
        Returns:
            tuple[bool]: 每个位置的布尔值表示对应的数是否为偶数
            
        Raises:
            TypeError: 当值不是数值类型时
        """
        if isinstance(self.value, (tuple, int, float)):
            if isinstance(self.value, (int, float)):
                return (int(self.value) % 2 == 0,)
            return tuple(int(v) % 2 == 0 for v in self.value)
        else:
            raise TypeError('Not a number(int, float, or tuple)')

    def is_odd(self) -> tuple[bool]:
        """判断是否全为奇数
        
        检查每个值是否为奇数。值会被转换为整数进行判断。
        
        Returns:
            tuple[bool]: 每个位置的布尔值表示对应的数是否为奇数
            
        Raises:
            TypeError: 当值不是数值类型时
        """
        if isinstance(self.value, (tuple, int, float)):
            if isinstance(self.value, (int, float)):
                return (int(self.value) % 2 == 1,)
            return tuple(int(v) % 2 == 1 for v in self.value)
        else:
            raise TypeError('Not a number(int, float, or tuple)')

    @staticmethod
    def is_prime_number(n: int) -> bool:
        """判断一个数是否为质数的静态辅助方法
        
        Args:
            n: 要判断的整数
            
        Returns:
            bool: 如果是质数返回True,否则返回False
        """
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def is_prime(self) -> tuple[bool]:
        """判断是否为质数
        
        检查每个值是否为质数。值会被转换为整数进行判断。
        只有大于1的整数才可能是质数。
        
        Returns:
            tuple[bool]: 每个位置的布尔值表示对应的数是否为质数
            
        Raises:
            TypeError: 当值不是数值类型时
            ValueError: 当值为负数或非整数时
        """
        if isinstance(self.value, (tuple, int, float)):
            if isinstance(self.value, (int, float)):
                if not float(self.value).is_integer():
                    raise ValueError("Value must be an integer")
                return (self.is_prime_number(int(self.value)),)
            
            # 检查所有值是否为整数
            if not all(float(v).is_integer() for v in self.value):
                raise ValueError("All values must be integers")
                
            return tuple(self.is_prime_number(int(v)) for v in self.value)
        else:
            raise TypeError('Not a number(int, float, or tuple)')
    
    def is_square_of_any_number(self, object: "number", squared_number: int | float) -> tuple[bool]:
        """判断一个数是否是另一个数的平方
        
        检查object中的每个值的平方是否等于squared_number。
        
        Args:
            object: 要检查的number对象
            squared_number: 要比较的平方数
            
        Returns:
            tuple[bool]: 每个位置的布尔值表示对应的数的平方是否等于squared_number
            
        Raises:
            TypeError: 当参数类型不正确时
        """
        if not isinstance(object, number):
            raise TypeError("First argument must be a number object")
            
        if not isinstance(squared_number, (int, float)):
            raise TypeError("Second argument must be int or float")
            
        if isinstance(object.value, (int, float)):
            return (object.value * object.value == squared_number,)
            
        return tuple(v * v == squared_number for v in object.value)
        
    def __len__(self) -> int:
        """返回元素个数
        
        Returns:
            int: 对于单值number返回1,对于多值number返回元素个数
        """
        if isinstance(self.value, (int, float)):
            return 1
        return len(self.value)
        
    def __reversed__(self) -> "number":
        """返回反转后的number对象
        
        对于单值number保持不变,对于多值number返回元素顺序反转后的新对象。
        
        Returns:
            number: 反转后的新number对象
        """
        if isinstance(self.value, (int, float)):
            return number(self.value)
        return number(*reversed(self.value))
        
    def add(self, value: "number | int | float", index: int = None) -> "number":
        """在指定位置添加新值
        
        将一个或多个值添加到number对象中。可以指定插入位置,默认添加到末尾。
        如果当前对象是单值number,会先转换为多值number。
        
        Args:
            value: 要添加的值,可以是number对象或数字
            index: 要插入的位置,如果不指定则添加到末尾
            
        Returns:
            number: 添加值后的新number对象
            
        Raises:
            TypeError: 当value不是合法的类型时
            IndexError: 当index超出范围时
        """
        # 将当前值转换为列表
        current = [self.value] if isinstance(self.value, (int, float)) else list(self.value)
        
        # 处理要添加的值
        if isinstance(value, number):
            if isinstance(value.value, (int, float)):
                to_add = [value.value]
            else:
                to_add = list(value.value)
        elif isinstance(value, (int, float)):
            to_add = [value]
        else:
            raise TypeError("Value must be number object or numeric type")
            
        # 插入值
        if index is None:
            current.extend(to_add)
        else:
            if not (0 <= index <= len(current)):
                raise IndexError("Index out of range")
            for i, v in enumerate(to_add):
                current.insert(index + i, v)
                
        # 返回新的number对象
        return number(*current)
    
    def remove(self, value: int | list[int] | None = None, index: int | list[int] | None = None) -> "number":
        """移除指定索引位置的元素

        支持通过单个索引或索引列表来移除一个或多个元素。当同时指定value和index时,index具有更高优先级。
        
        Args:
            value: 要移除元素的索引位置或索引列表
            index: 要移除元素的索引位置或索引列表(优先级高于value)
            
        Returns:
            number: 移除值后的number对象(self),支持链式调用
            
        Raises:
            TypeError: 当对单值number使用此方法,或传入的索引类型不正确时
            IndexError: 当任何索引超出范围时
            ValueError: 当未提供任何索引时
            
        Examples:
            >>> n = number(1, 2, 3, 4, 5)
            >>> n.remove(1)  # 移除索引1的元素
            number(1, 3, 4, 5)
            >>> n.remove([1, 3])  # 移除索引1和3的元素
            number(1, 3, 5)
            >>> n.remove(index=[-1, 0])  # 使用负索引,移除最后一个和第一个元素
            number(3)
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot remove values from a single-value number")
            
        # 转换为列表以便修改
        current_values = list(self.value)
        length = len(current_values)
        
        # 确定要使用的索引
        idx = index if index is not None else value
        if idx is None:
            raise ValueError("Must specify either value or index parameter")
            
        # 将单个索引转换为列表
        if isinstance(idx, (int)):
            indices = [idx]
        elif isinstance(idx, (list, tuple)):
            indices = list(idx)
        else:
            raise TypeError(f"Index must be an integer or a list of integers, not {type(idx)}")

        # 对索引进行预处理:去重、转换负索引、验证范围、从大到小排序
        processed_indices = set()
        for i in indices:
            if not isinstance(i, int):
                raise TypeError(f"All indices must be integers, got {type(i)}")
                
            # 转换负索引为正索引
            pos = i if i >= 0 else length + i
            
            # 检查索引范围
            if not (0 <= pos < length):
                raise IndexError(f"Index {i} is out of range [-{length}, {length})")
                
            processed_indices.add(pos)
        
        # 从大到小排序以避免删除时影响其他索引的位置
        for pos in sorted(processed_indices, reverse=True):
            del current_values[pos]
            
        # 更新对象的状态
        self.value = tuple(current_values)
        return self  # 支持链式调用
    
    def delitem(self, start: int, end: int = None) -> None:
        """删除指定范围内的元素
        
        删除从start到end(不含)之间的所有元素。如果不指定end,则只删除start位置的元素。
        不能对单值number对象使用此方法。
        
        Args:
            start: 起始索引
            end: 结束索引(可选),如果不指定则只删除start位置的元素
            
        Raises:
            TypeError: 当对单值number使用此方法时
            IndexError: 当索引超出范围时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot delete items from single value")
            
        current_values = list(self.value)
        
        if end is not None:
            if start < 0:
                start = len(current_values) + start
            if end < 0:
                end = len(current_values) + end
            if not (0 <= start < len(current_values)) or not (0 <= end <= len(current_values)):
                raise IndexError("Index out of range")
            del current_values[start:end]
        else:
            if start < 0:
                start = len(current_values) + start
            if not (0 <= start < len(current_values)):
                raise IndexError("Index out of range")
            del current_values[start]
            
        self.value = tuple(current_values)

    def gcd(self, other: "number") -> "number":
        """计算最大公约数
        
        如果是多值number对象,则对应位置的数字计算最大公约数。
        要求所有数字都是整数。
        
        Args:
            other: 另一个number对象
            
        Returns:
            number: 包含最大公约数的number对象
            
        Raises:
            TypeError: 当参数类型不正确时
            ValueError: 当值不是整数时
        """
        def _gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return abs(a)
            
        if not isinstance(other, number):
            raise TypeError("Argument must be a number object")
            
        if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
            if not (float(self.value).is_integer() and float(other.value).is_integer()):
                raise ValueError("Values must be integers")
            return number(_gcd(int(self.value), int(other.value)))
            
        if len(self) != len(other):
            raise ValueError("Cannot calculate GCD of numbers with different lengths")
            
        if not all(float(v).is_integer() for v in self.value + other.value):
            raise ValueError("All values must be integers")
            
        return number(*[_gcd(int(a), int(b)) for a, b in zip(self.value, other.value)])
        
    def lcm(self, other: "number") -> "number":
        """计算最小公倍数
        
        如果是多值number对象,则对应位置的数字计算最小公倍数。
        要求所有数字都是整数。
        
        Args:
            other: 另一个number对象
            
        Returns:
            number: 包含最小公倍数的number对象
            
        Raises:
            TypeError: 当参数类型不正确时
            ValueError: 当值不是整数时
            ZeroDivisionError: 当任一数为0时
        """
        def _lcm(a: int, b: int) -> int:
            if a == 0 or b == 0:
                raise ZeroDivisionError("Cannot calculate LCM with zero")
            return abs(a * b) // math.gcd(a, b)
            
        if not isinstance(other, number):
            raise TypeError("Argument must be a number object")
            
        if isinstance(self.value, (int, float)) and isinstance(other.value, (int, float)):
            if not (float(self.value).is_integer() and float(other.value).is_integer()):
                raise ValueError("Values must be integers")
            return number(_lcm(int(self.value), int(other.value)))
            
        if len(self) != len(other):
            raise ValueError("Cannot calculate LCM of numbers with different lengths")
            
        if not all(float(v).is_integer() for v in self.value + other.value):
            raise ValueError("All values must be integers")
            
        return number(*[_lcm(int(a), int(b)) for a, b in zip(self.value, other.value)])
        
    def abs(self) -> "number":
        """返回绝对值
        
        Returns:
            number: 包含绝对值的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(abs(self.value))
        return number(*(abs(v) for v in self.value))
        
    def power(self, n: int) -> "number":
        """计算幂
        
        计算每个数的n次方。
        
        Args:
            n: 指数,必须是整数
            
        Returns:
            number: 包含幂运算结果的number对象
            
        Raises:
            TypeError: 当n不是整数时
        """
        if not isinstance(n, int):
            raise TypeError("Exponent must be an integer")
            
        if isinstance(self.value, (int, float)):
            return number(pow(self.value, n))
        return number(*(pow(v, n) for v in self.value))
        
    def sum(self) -> int | float:
        """计算所有元素的和
        
        Returns:
            int | float: 所有元素的和
        """
        if isinstance(self.value, (int, float)):
            return self.value
        return sum(self.value)
        
    def average(self) -> float:
        """计算平均值
        
        Returns:
            float: 所有元素的平均值
        """
        if isinstance(self.value, (int, float)):
            return float(self.value)
        return sum(self.value) / len(self.value)
        
    def min(self) -> int | float:
        """返回最小值
        
        Returns:
            int | float: 最小的元素
        """
        if isinstance(self.value, (int, float)):
            return self.value
        return min(self.value)
        
    def max(self) -> int | float:
        """返回最大值
        
        Returns:
            int | float: 最大的元素
        """
        if isinstance(self.value, (int, float)):
            return self.value
        return max(self.value)
        
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
        
        如果元素个数为奇数,返回中间的数；
        如果元素个数为偶数,返回中间两个数的平均值。
        
        Returns:
            float: 中位数
            
        Raises:
            TypeError: 当对象为单值number时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot calculate median of single value")
        sorted_values = sorted(self.value)
        n = len(sorted_values)
        if n % 2 == 0:
            return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
        return float(sorted_values[n//2])

    def mode(self) -> "number":
        """计算众数(出现次数最多的值)
        
        如果有多个众数,全部返回。
        
        Returns:
            number: 包含众数的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(self.value)
            
        from collections import Counter
        counts = Counter(self.value)
        max_freq = max(counts.values())
        modes = tuple(num for num, freq in counts.items() if freq == max_freq)
        return number(*modes)

    def variance(self) -> float:
        """计算方差
        
        Returns:
            float: 方差
            
        Raises:
            TypeError: 当对象为单值number时
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
            TypeError: 当对象为单值number时
        """
        return math.sqrt(self.variance())

    def normalize(self) -> "number":
        """归一化处理
        
        将所有值缩放到[0,1]区间。
        如果所有值相同,则返回全0序列。
        
        Returns:
            number: 归一化后的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(1.0)
            
        min_val = min(self.value)
        max_val = max(self.value)
        if min_val == max_val:
            return number(*(0.0 for _ in self.value))
        return number(*((x - min_val) / (max_val - min_val) for x in self.value))

    def unique(self) -> "number":
        """返回去重后的值
        
        保持原有顺序。
        
        Returns:
            number: 去重后的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(self.value)
        seen = []
        for x in self.value:
            if x not in seen:
                seen.append(x)
        return number(*seen)

    def is_sorted(self) -> bool:
        """检查是否已排序
        
        Returns:
            bool: 如果是升序排序则返回True
        """
        if isinstance(self.value, (int, float)):
            return True
        return all(a <= b for a, b in zip(self.value[:-1], self.value[1:]))

    def sort(self, reverse: bool = False) -> "number":
        """返回排序后的值
        
        Args:
            reverse: 是否降序排序,默认False(升序)
            
        Returns:
            number: 排序后的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(self.value)
        return number(*sorted(self.value, reverse=reverse))

    def cumsum(self) -> "number":
        """计算累积和
        
        返回一个新的number对象,其中每个位置包含到该位置为止所有数的和。
        
        Returns:
            number: 累积和的number对象
        """
        if isinstance(self.value, (int, float)):
            return number(self.value)
        result = []
        total = 0
        for x in self.value:
            total += x
            result.append(total)
        return number(*result)

    def diff(self) -> "number":
        """计算相邻元素的差
        
        返回一个新的number对象,包含相邻元素的差值。
        结果的长度比原序列少1。
        
        Returns:
            number: 差值的number对象
            
        Raises:
            TypeError: 当对象为单值number时
        """
        if isinstance(self.value, (int, float)):
            raise TypeError("Cannot calculate differences of single value")
        return number(*(b - a for a, b in zip(self.value[:-1], self.value[1:])))
        
    def __hash__(self) -> int:
        """返回哈希值
        
        对于单值number,返回其值的哈希值；
        对于多值number,返回所有值的哈希值的组合。
        
        Returns:
            int: 哈希值
        """
        if isinstance(self.value, (int, float)):
            return hash(self.value)
        return hash(tuple(self.value))
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
    print(f"hash(a) = {hash(a)}")

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
    print(d.__class__ == number)
    a = number.create(['1+8', '2+8', '3+8'])
    print(a)
    b = number.create(['1+8.0', '2+8.85', '3+8.0'])
    print(b)
    e= number(1, 2, 3, 4)
    e.delitem(1,3)
    print(e)
    del e[-1]
    e[-1] = 100
    print(e)
    print(f"e after deletion and modification: {e.value}")
