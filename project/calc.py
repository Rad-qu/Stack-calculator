#!/usr/bin/env python3

import re
from operator import add, sub, mul, truediv, pow
from stack import Stack
from compf import Compf, Compf_power


class Calc(Compf):
    """
    Интерпретатор арифметических выражений вычисляет значения
    правильных арифметических формул, в которых в качестве
    операндов допустимы только числа от 0 до 3999
    """

    SYMBOLS = re.compile("[0-9]")

    def __init__(self):
        # Инициализация (конструктор) класса Compf
        super().__init__()
        # Создание стека чисел для работы стекового калькулятора
        self.r = Stack()

    # Интерпретация арифметического выражения
    def compile(self, str):
        Compf.compile(self, str)
        return self.r.top()

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))

    # Обработка символа операции
    def process_oper(self, c):
        second, first = self.r.pop(), self.r.pop()
        self.r.push({"+": add, "-": sub, "*": mul,
                     "/": truediv}[c](first, second))

class Calc_power(Compf_power):

    token_pattern = re.compile(r"\*\*|[()+\-*/^]|[0]|[1-9][0-9]{0,3}")

    def __init__(self):
        # Инициализация (конструктор) класса Compf
        super().__init__()
        # Создание стека чисел для работы стекового калькулятора
        self.r = Stack()
        
    def tokenize(self, expr):
        return super().tokenize(expr)
    
    # Интерпретация арифметического выражения
    def compile(self, str):
        Compf.compile(self, str)
        return self.r.top()

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))

    #возведение в степень
    @staticmethod
    def power(base, exponent):
        return base**exponent

    # Обработка символа операции
    def process_oper(self, c):
        second, first = self.r.pop(), self.r.pop()
        self.r.push({"+": add, "-": sub, "*": mul,
                     "/": truediv}[c](first, second))
        

if __name__ == "__main__":
    c = Calc()
    while True:
        str = input("Арифметическое выражение: ")
        print(f"Результат его вычисления: {c.compile(str)}")
        print()
