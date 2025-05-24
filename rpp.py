"""
RangePlusPlus class: An enhanced version of range class with additional features
Including: custom step size, ascending/descending order, map function, multiple iteration types (list/set/tuple)
"""
# The class's name is from c++ ! But l don't like C++. :(
# Use this in formally occasions, like: "from rpp import RangePlusPlus".although some people can't see this. :(
class RangePlusPlus:
    def __init__(self, start, end, map, step=1, ascending=True, iter_type='list'):
        """
        Initialize RangePlusPlus object
        :param start: starting value
        :param end: ending value
        :param step: step size, default is 1
        :param ascending: whether in ascending order, default True
        :param map: map function, default None (identity function)
        :param iter_type: iteration type, options: 'list'/'set'/'tuple', default 'list'
        """
        self.start = start
        self.end = end
        self.step = step
        self.ascending = ascending
        self.map = map if map else lambda x: x  # Use identity function if no map provided
        self.iter_type = iter_type.lower()  # Convert to lowercase for consistent handling
        self._iterator = None  # Internal iterator

    def __str__(self):
        """
        Convert object to string representation
        :return: String in corresponding format based on iter_type
        """
        # Generate base number sequence
        numbers = list(range(self.start, self.end, self.step))
        mapped_numbers = [self.map(x) for x in numbers]  # Apply map function
        if not self.ascending:
            mapped_numbers = mapped_numbers[::-1]  # Reverse sequence if descending
        if self.iter_type == 'set':
            from collections import OrderedDict
            result = list(OrderedDict.fromkeys(mapped_numbers))  # Remove duplicates while preserving order
        else:
            result = mapped_numbers
            
        # Return string in appropriate format based on type
        if self.iter_type == 'set':
            return '{' + ', '.join(map(str, result)) + '}'
        elif self.iter_type == 'tuple':
            return '(' + ', '.join(map(str, result)) + ')'
        else:  # list
            return '[' + ', '.join(map(str, result)) + ']'

    def __iter__(self):
        """
        Return iterator
        :return: self as iterator
        """
        numbers = list(range(self.start, self.end, self.step))
        mapped_numbers = [self.map(x) for x in numbers]
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
        Implement next method for iterator
        :return: Next element in sequence
        :raises: StopIteration when iteration is complete
        """
        if self._iterator is None:
            self.__iter__()  # Initialize iterator if not initialized
        try:
            return next(self._iterator)
        except StopIteration:
            self._iterator = None  # Reset iterator
            raise StopIteration
