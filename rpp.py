"""
RangePlusPlus类,一个增强版的range类,具有额外的功能特性
包括：自定义步长、升序/降序、映射函数、多种迭代类型（列表/集合/元组）
"""
# 这个类的名字来源于C++！但我不喜欢C++。:(
# 在正式场合请这样使用：from rpp import RangePlusPlus。虽然有些人看不到这条注释。:(
class RangePlusPlus:    
    def __init__(self, start, end, mapping=None, step=1, ascending=True, iter_type='list'):
        """
        初始化 RangePlusPlus 对象
        :param start: 起始值
        :param end: 结束值
        :param step: 步长,默认为1
        :param ascending: 是否升序,默认为True
        :param mapping: 映射函数,默认为None(恒等函数)
        :param iter_type: 迭代类型，可选：'list'/'set'/'tuple'，默认为'list'
        """
        self.start = start
        self.end = end
        self.step = step
        self.ascending = ascending
        self.mapping = mapping if mapping else lambda x: x  # Use identity function if no mapping provided
        self.iter_type = iter_type.lower()  # Convert to lowercase for consistent handling
        self._iterator = None  # Internal iterator
        
    def __str__(self):
        """
        将对象转换为字符串表示
        :return: 根据iter_type返回相应格式的字符串
        """
        # 生成基础数字序列
        numbers = list(range(self.start, self.end, self.step))
        mapped_numbers = [self.mapping(x) for x in numbers]  # 应用映射函数
        if not self.ascending:
            mapped_numbers = mapped_numbers[::-1]  # 如果是降序则反转序列
        if self.iter_type == 'set':
            from collections import OrderedDict
            result = list(OrderedDict.fromkeys(mapped_numbers))  # 去除重复项并保持顺序
        else:
            result = mapped_numbers
            
        # 根据类型返回适当格式的字符串
        if self.iter_type == 'set':
            return '{' + ', '.join(map(str, result)) + '}'
        elif self.iter_type == 'tuple':
            return '(' + ', '.join(map(str, result)) + ')'
        else:  # list
            return '[' + ', '.join(map(str, result)) + ']'
            
    def __iter__(self):
        """
        返回迭代器
        :return: 返回self作为迭代器
        """
        numbers = list(range(self.start, self.end, self.step))
        mapped_numbers = [self.mapping(x) for x in numbers]
        if not self.ascending:
            mapped_numbers = mapped_numbers[::-1]
        if self.iter_type == 'set':
            from collections import OrderedDict
            self._iterator = iter(OrderedDict.fromkeys(mapped_numbers))
        else:
            self._iterator = iter(mapped_numbers)
        return self
        
    def __next__(self):
        """
        实现迭代器的next方法
        :return: 序列中的下一个元素
        :raises: 当迭代完成时抛出StopIteration异常
        """
        if self._iterator is None:
            self.__iter__()  # 如果迭代器未初始化则进行初始化
        try:
            return next(self._iterator)
        except StopIteration:
            self._iterator = None  # 重置迭代器
            raise StopIteration
