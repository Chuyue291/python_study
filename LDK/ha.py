import re


class SimpleDict:
    """
    一个简单的字典类，通过字符串格式存储键值对
    格式为: 'keys:key1,key2,...;values:value1,value2,...'
    经过性能优化，支持延迟更新和批量更新，并增强了安全性
    """
    
    class LenError(Exception):
        """当键和值的数量不匹配时抛出的异常"""
        pass
    
    class FormatError(Exception):
        """当输入字符串格式不正确时抛出的异常"""
        pass
    
    class ValidationError(Exception):
        """当输入数据验证失败时抛出的异常"""
        pass
    
    # 定义允许的字符模式
    _KEY_PATTERN = re.compile(r'^[0-9a-zA-Z_]*$')
    _VALUE_PATTERN = re.compile(r'^[0-9a-zA-Z_\[\],\s\.]*$')  # 允许列表字符
    _MAX_KEY_LENGTH = 100
    _MAX_VALUE_LENGTH = 1000
    _MAX_ITEMS = 10000  # 防止过多项目
    
    def __init__(self, string: str):
        """
        初始化字典对象
        
        Args:
            string: 包含键值对的字符串，格式为'keys:key1,key2,...;values:value1,value2,...'
        
        Raises:
            LenError: 如果键和值的数量不匹配
            FormatError: 如果字符串格式不正确
            ValidationError: 如果键或值不符合验证规则
        """
        self._validate_input_string(string)
        
        self.string = string
        self.keys: list[str] = []
        self.values: list[str] = []
        self._dirty = False  # 脏标记，用于延迟字符串更新
        
        pattern = r'keys:([0-9a-zA-Z_,]*);values:([0-9a-zA-Z_\[\],\s\.]*)'
        match = re.fullmatch(pattern, string)
        if not match:
            raise self.FormatError("Invalid string format. Expected format: 'keys:key1,key2,...;values:value1,value2,...'")
            
        keys_str = match.group(1)
        values_str = match.group(2)
        
        # 处理空字符串的情况
        self.keys = keys_str.split(',') if keys_str else []
        self.values = values_str.split(',') if values_str else []
        
        # 验证数量匹配
        if len(self.keys) != len(self.values):
            raise self.LenError("The number of keys and values must match.")
            
        # 验证每个键和值
        for key in self.keys:
            self._validate_key(key)
        
        for value in self.values:
            self._validate_value(value)
            
        # 防止过多项目
        if len(self.keys) > self._MAX_ITEMS:
            raise self.ValidationError(f"Too many items. Maximum allowed: {self._MAX_ITEMS}")

    def _validate_input_string(self, string: str) -> None:
        """
        验证输入字符串的基本有效性
        
        Args:
            string: 输入字符串
            
        Raises:
            FormatError: 如果字符串格式不正确或为空
            ValidationError: 如果字符串过长
        """
        if not string:
            raise self.FormatError("Input string cannot be empty")
            
        if len(string) > 10 * 1024 * 1024:  # 10MB限制
            raise self.ValidationError("Input string is too large")
            
        # 检查基本格式
        if not string.startswith("keys:") or ";values:" not in string:
            raise self.FormatError("Invalid string format. Expected format: 'keys:key1,key2,...;values:value1,value2,...'")
    
    def _validate_key(self, key: str) -> None:
        """验证键是否符合规则"""
        if not key:  # 空键是合法的
            return
            
        if len(key) > self._MAX_KEY_LENGTH:
            raise self.ValidationError(f"Key too long: {key[:10]}... (max {self._MAX_KEY_LENGTH} chars)")
            
        if not self._KEY_PATTERN.match(key):
            raise self.ValidationError(f"Invalid key format: {key} (only alphanumeric and underscore allowed)")
    
    def _validate_value(self, value: str) -> None:
        """验证值是否符合规则"""
        if len(value) > self._MAX_VALUE_LENGTH:
            raise self.ValidationError(f"Value too long: {value[:10]}... (max {self._MAX_VALUE_LENGTH} chars)")
            
        if not self._VALUE_PATTERN.match(value):
            raise self.ValidationError(f"Invalid value format: {value} (only alphanumeric, underscore, and list characters allowed)")

    def __repr__(self) -> str:
        """返回字典的详细表示"""
        return f"SimpleDict(keys={self.keys}, values={self.values})"

    def __str__(self) -> str:
        """返回字典的字符串表示，如果数据被修改则更新字符串"""
        if self._dirty:
            self._update_string()
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
            ValidationError: 如果新键不符合规则
        """
        # 安全检查
        self._validate_update_args(indexes, values)
        
        for i, value in zip(indexes, values):
            # 索引范围检查
            if i < 0 or i >= len(self.keys):
                raise IndexError(f"Index {i} is out of range (0-{len(self.keys)-1})")
                
            # 转换为字符串并验证
            str_value = str(value)
            self._validate_key(str_value)
            self.keys[i] = str_value
        
        # 标记为脏，不立即更新字符串
        self._dirty = True
    
    def update_value(self, indexes: list[int], values: list) -> None:
        """
        更新指定索引位置的值
        
        Args:
            indexes: 要更新的值的索引列表
            values: 新的值列表
            
        Raises:
            LenError: 如果索引列表和值列表长度不匹配
            IndexError: 如果索引超出范围
            ValidationError: 如果新值不符合规则
        """
        # 安全检查
        self._validate_update_args(indexes, values)
        
        for i, value in zip(indexes, values):
            # 索引范围检查
            if i < 0 or i >= len(self.values):
                raise IndexError(f"Index {i} is out of range (0-{len(self.values)-1})")
                
            # 转换为字符串并验证
            str_value = str(value)
            self._validate_value(str_value)
            self.values[i] = str_value
        
        # 标记为脏，不立即更新字符串
        self._dirty = True
    
    def _validate_update_args(self, indexes: list[int], values: list) -> None:
        """验证更新操作的参数"""
        # 类型检查
        if not isinstance(indexes, list):
            raise TypeError("indexes must be a list")
        if not isinstance(values, list):
            raise TypeError("values must be a list")
            
        # 长度匹配检查
        if len(indexes) != len(values):
            raise self.LenError("The number of indexes and values must match.")
            
        # 数量限制
        if len(indexes) > self._MAX_ITEMS:
            raise self.ValidationError(f"Too many items in a single update. Maximum allowed: {self._MAX_ITEMS}")
            
        # 检查索引类型
        for i in indexes:
            if not isinstance(i, int):
                raise TypeError(f"Index must be an integer, got {type(i).__name__}")

    def batch_update(self, key_updates: dict[int, object] = None, 
                    value_updates: dict[int, object] = None) -> None:
        """
        批量更新键和值
        
        Args:
            key_updates: 字典 {索引: 新键值}
            value_updates: 字典 {索引: 新值}
            
        Raises:
            IndexError: 如果索引超出范围
            ValidationError: 如果新键或新值不符合规则
        """
        if not key_updates and not value_updates:
            return  # 没有要更新的内容

        # 确保参数是字典或None
        if key_updates is not None and not isinstance(key_updates, dict):
            raise TypeError("key_updates must be a dictionary or None")
        if value_updates is not None and not isinstance(value_updates, dict):
            raise TypeError("value_updates must be a dictionary or None")
            
        # 为None时初始化为空字典
        key_updates = key_updates or {}
        value_updates = value_updates or {}

        # 验证批量更新大小
        total_updates = len(key_updates) + len(value_updates)
        if total_updates > self._MAX_ITEMS:
            raise self.ValidationError(f"Too many items in batch update. Maximum allowed: {self._MAX_ITEMS}")

        # 更新键
        for idx, new_key in key_updates.items():
            if not isinstance(idx, int):
                raise TypeError(f"Index must be an integer, got {type(idx).__name__}")
            
            if idx < 0 or idx >= len(self.keys):
                raise IndexError(f"Key index {idx} is out of range (0-{len(self.keys)-1})")
            
            # 转换并验证新键
            str_key = str(new_key)
            self._validate_key(str_key)
            self.keys[idx] = str_key
        
        # 更新值
        for idx, new_value in value_updates.items():
            if not isinstance(idx, int):
                raise TypeError(f"Index must be an integer, got {type(idx).__name__}")
            
            if idx < 0 or idx >= len(self.values):
                raise IndexError(f"Value index {idx} is out of range (0-{len(self.values)-1})")
            
            # 转换并验证新值
            str_value = str(new_value)
            self._validate_value(str_value)
            self.values[idx] = str_value
                
        if key_updates or value_updates:
            self._dirty = True
    
    def _update_string(self) -> None:
        """辅助方法，用于在修改键或值后更新字符串表示"""
        # 再次验证所有键和值（以防万一）
        for key in self.keys:
            self._validate_key(key)
        
        for value in self.values:
            self._validate_value(value)
        
        keys_str = ','.join(str(k) for k in self.keys)
        values_str = ','.join(str(v) for v in self.values)
        self.string = f"keys:{keys_str};values:{values_str}"
        self._dirty = False  # 重置脏标记

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
        # 安全转换为字符串
        str_key = str(key)
        
        try:
            index = self.keys.index(str_key)
            return self.values[index]
        except ValueError:
            raise KeyError(f"Key \"{str_key}\" isn't found.")
    
    def get(self, key: str, default: object = None) -> str:
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
    
    def items(self) -> list[tuple[str, str]]:
        """
        返回键值对的列表
        
        Returns:
            包含(key, value)元组的列表
        """
        return list(zip(self.keys, self.values))
    
    def force_update_string(self) -> None:
        """
        强制更新字符串表示，无论是否标记为脏
        
        如果需要确保获取最新的字符串表示，可以调用此方法
        """
        self._update_string()
    
    def __len__(self) -> int:
        """返回字典中键值对的数量"""
        return len(self.keys)
    
    def __contains__(self, key: object) -> bool:
        """检查字典是否包含指定的键"""
        return str(key) in self.keys


# 测试代码
if __name__ == "__main__":
    try:
        d = SimpleDict("keys:key1,key2;values:value1,value2")
        print(d)
        print(d.get("key1"))  # 输出: value1
        print(d.get("key3", "default"))  # 输出: default
        
        d.update_key([0], ["new_key1"])
        d.update_value([1], ["new_value2"])
        print(d)
        
        d.batch_update({0: "batch_key1"}, {1: "batch_value2"})
        print(d)
        
    except Exception as e:
        print(f"Error: {e}")