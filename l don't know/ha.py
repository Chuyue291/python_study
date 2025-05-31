import re



class SimpleDict:
    """
    一个简单的字典类，通过字符串格式存储键值对
    格式为: 'keys:key1,key2,...;values:value1,value2,...'
    """
    
    class LenError(Exception):
        """当键和值的数量不匹配时抛出的异常"""
        pass
    
    def __init__(self, string: str):
        """
        初始化字典对象
        
        Args:
            string: 包含键值对的字符串，格式为'keys:key1,key2,...;values:value1,value2,...'
        
        Raises:
            LenError: 如果键和值的数量不匹配
        """
        self.string = string
        self.keys: list[str] = []
        self.values: list[str] = []
        
        pattern = r'keys:([0-9a-zA-Z_,]*);values:([0-9a-zA-Z_,]*)'
        if match := re.fullmatch(pattern, string):
            keys_str = match.group(1)
            values_str = match.group(2)
            
            # 处理空字符串的情况
            self.keys = keys_str.split(',') if keys_str else []
            self.values = values_str.split(',') if values_str else []
            
            if len(self.keys) != len(self.values):
                raise self.LenError("The number of keys and values must match.")

    def __repr__(self) -> str:
        """返回字典的详细表示"""
        return f"SimpleDict(keys={self.keys}, values={self.values})"

    def __str__(self) -> str:
        """返回字典的字符串表示"""
        return self.string
    
    def __getitem__(self, key: str) -> str:
        """
        通过键获取值，支持字典索引语法 dict[key]
        
        Args:
            key: 要查找的键
            
        Returns:
            对应的值
            
        Raises:
            KeyError: 如果键不存在
        """
        return self.get_value(key)
    
    def update_key(self, indexes: list[int], values: list) -> None:
        """
        更新指定索引位置的键
        
        Args:
            indexes: 要更新的键的索引列表
            values: 新的键值列表
            
        Raises:
            LenError: 如果索引列表和值列表长度不匹配
            IndexError: 如果索引超出范围
        """
        if len(indexes) != len(values):
            raise self.LenError("The number of indexes and values must match.")
        
        for i, value in zip(indexes, values):
            if i < 0 or i >= len(self.keys):
                raise IndexError(f"Index {i} is out of range.")
            self.keys[i] = str(value)  # 确保值是字符串
        
        # 更新字符串表示
        self._update_string()
    
    def update_value(self, indexes: list[int], values: list) -> None:
        """
        更新指定索引位置的值
        
        Args:
            indexes: 要更新的值的索引列表
            values: 新的值列表
            
        Raises:
            LenError: 如果索引列表和值列表长度不匹配
            IndexError: 如果索引超出范围
        """
        if len(indexes) != len(values):
            raise self.LenError("The number of indexes and values must match.")
        
        for i, value in zip(indexes, values):
            if i < 0 or i >= len(self.values):
                raise IndexError(f"Index {i} is out of range.")
            self.values[i] = str(value)  # 确保值是字符串
        
        # 更新字符串表示
        self._update_string()

    def _update_string(self) -> None:
        """辅助方法，用于在修改键或值后更新字符串表示"""
        keys_str = ','.join(str(k) for k in self.keys)
        values_str = ','.join(str(v) for v in self.values)
        self.string = f"keys:{keys_str};values:{values_str}"

    def get_value(self, key: str) -> str:
        """
        获取指定键对应的值
        
        Args:
            key: 要查找的键
            
        Returns:
            对应的值
            
        Raises:
            KeyError: 如果键不存在
        """
        try:
            index = self.keys.index(str(key))
            return self.values[index]
        except ValueError:
            raise KeyError(f"Key \"{key}\" isn't found.")
    
    def get(self, key: str, default = None) -> str :
        """
        获取指定键对应的值，如果键不存在则返回默认值
        
        Args:
            key: 要查找的键
            default: 键不存在时返回的默认值
            
        Returns:
            对应的值或默认值
        """
        try:
            return self.get_value(key)
        except KeyError:
            return default
    
    def items(self):
        """
        返回键值对的迭代器
        
        Returns:
            包含(key, value)元组的迭代器
        """
        return zip(self.keys, self.values)


# 测试代码
if __name__ == "__main__":
    a = SimpleDict('keys:1,2,3;values:4,5,6')
    print(a)                 # keys:1,2,3;values:4,5,6
    print(a.keys)            # ['1', '2', '3']
    
    a.update_value([0, 1], [[1, 2], 8])
    print(a)                 # keys:1,2,3;values:[1, 2],8,6
    print(a.values)          # ['[1, 2]', '8', '6']
    
    print(a.get_value('1'))  # [1, 2]
    print(a['2'])            # 8
    print(a.get('3'))        # 6
    print(a.get('4', 'Not found'))  # Not found
    
    for key, value in a.items():
        print(f"{key}: {value}")
