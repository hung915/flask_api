# SRC SOC (Single responsibility)
# class Journal:
#     def __init__(self):
#         self.entries = []
#         self.count = 0
#
#     def add_entry(self, text):
#         self.count += 1
#         self.entries.append(f'{self.count}: {text}')
#
#     def remove_entry(self, pos):
#         del self.entries[pos]
#
#     def __str__(self):
#         return '\n'.join(self.entries)
#
#     def save(self, filename):
#         file = open(filename, 'w')
#         file.write(str(self))
#         file.close()
#
#     def load(self, filname):
#         pass
#
#
# class PersistenceManager:
#     @staticmethod
#     def save_to_file(journal, filename):
#         file = open(filename, 'w')
#         file.write(str(journal))
#         file.close()
#
#
# j = Journal()
# j.add_entry('I cried today')
# j.add_entry('I ate a bug')
# print(f'Journal entries:\n{j}')
# file = 'D:\journal.txt'
# PersistenceManager.save_to_file(j, file)
# with open(file) as fh:
#     print(fh.read())

# Open-Closed: Open for extension, closed for modification
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size


class ProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size:
                yield p

    def filter_by_color_and_size(self, products, color, size):
        for p in products:
            if p.size == size and p.color == color:
                yield p


# 2 properties -> 3 combinations
# 3 properties -> 7 combinations

# Specification


class Specification:
    def is_satisfied(self, item):
        pass

    def __and__(self, other):
        return AndSpecification(self, other)


class Filter:
    def filter(self, items, spec):
        pass


class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size


class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(map(
            lambda spec: spec.is_satisfied(item), self.args
        ))


apple = Product('Apple', Color.GREEN, Size.SMALL)
tree = Product('Tree', Color.GREEN, Size.LARGE)
house = Product('House', Color.BLUE, Size.LARGE)

products = [apple, tree, house]

pf = ProductFilter()
print('Green products (old):')
for p in pf.filter_by_color(products, Color.GREEN):
    print(f'- {p.name} is green')

bf = BetterFilter()
print('Green products (New):')
green = ColorSpecification(Color.GREEN)
for p in bf.filter(products, green):
    print(f'- {p.name} is green')

print('Large products:')
large = SizeSpecification(Size.LARGE)
for p in bf.filter(products, large):
    print(f'- {p.name} is large')

print('Large Blue products:')
# large_blue = AndSpecification(large, ColorSpecification(Color.BLUE))

large_blue = large & ColorSpecification(Color.BLUE)
for p in bf.filter(products, large_blue):
    print(f'- {p.name} is large and blue')

#Liskov Substitution Principle

