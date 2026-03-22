#!/usr/bin/env python3

import re
from operator import add, sub, mul, truediv, pow
from stack import Stack
from compf import Compf, Compf_power, OctCompf


class Calc(Compf):
    """
    Интерпретатор арифметических выражений вычисляет значения
    правильных арифметических формул, в которых в качестве
    операндов допустимы только цифры [0-9]
    """

    SYMBOLS = re.compile("[0-9]")

    def __init__(self):
             super().__init__()
        self.r = Stack()

    def compile(self, str):
        Compf.compile(self, str)   # родительский метод уже удаляет пробелы
        return self.r.top()

    def process_value(self, c):
        self.r.push(int(c))

    def process_oper(self, c):
        if c == '!':
            val = self.r.pop()
            self.r.push(self.factorial(val))
        else:
            second, first = self.r.pop(), self.r.pop()
            self.r.push({"+": add, "-": sub, "*": mul,
                         "/": truediv}[c](first, second))

    @staticmethod
    def factorial(n):
        if not isinstance(n, int) or n < 0:
            raise Exception("Факториал определён только для неотрицательных целых чисел")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
      
class Calc_power(Compf_power):

    SYMBOLS = re.compile(r'0|[1-9][0-9]*')
    TOKEN_PATTERN = re.compile(r"\*\*|[()+\-*/^]|0|[1-9][0-9]*")

    def __init__(self):
        # Инициализация (конструктор) класса Compf
        super().__init__()
        # Создание стека чисел для работы стекового калькулятора
        self.r = Stack()
        
    def tokenize(self, expr):
        return re.findall(self.TOKEN_PATTERN, expr)
    
    # Интерпретация арифметического выражения
    def compile(self, str):
        Compf_power.compile(self, str)
        return self.r.top()

    # Обработка цифры
    def process_value(self, c):
        self.r.push(int(c))

    # Обработка символа операции
    def process_oper(self, c):
        second, first = self.r.pop(), self.r.pop()
        self.r.push({"+": add, "-": sub, "*": mul,
                     "/": truediv, "**" : pow, "^": pow}[c](first, second))




class OctCalc(OctCompf):
    def __init__(self):
        super().__init__()
        self.r = Stack()

    def compile(self, expr):
        super().compile(expr)
        return self.r.top()

    def process_value(self, token):
        value = int(token, 8)
        if value < 0 or value > 3999:
            raise Exception(f"Число {token} выходит за допустимый диапазон [0, 3999]")
        self.r.push(value)

    def process_oper(self, c):
        if c == '!':
            val = self.r.pop()
            self.r.push(self.factorial(val))
        else:
            second, first = self.r.pop(), self.r.pop()
            self.r.push({"+": add, "-": sub, "*": mul, "/": truediv}[c](first, second))

    @staticmethod
    def factorial(n):
        if not isinstance(n, int) or n < 0:
            raise Exception("Факториал определён только для неотрицательных целых чисел")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


if __name__ == "__main__":
    print("=== Тестирование Calc с унарным факториалом ===")
    calc = Calc()

    test_expressions = [
        "2-3!",                # -4
        "3!+2",                # 8
        "(2+3)!",              # 120
        "3!!",                 # 720
        "(3!)!",               # 720
        "0!",                  # 1
        "5!/5",                # 24.0
        "(2+3)!*5",            # 600
        "(5-2)!+2",            # 4
        "5!/(3!-2!)+(2+3)!",   # 150.0
        "0!!",                 # 1
        "(2+3)!/(5-2)!",       # 20.0
        "(3!+4)/2!",           # 5.0
        "(2+3)! * (4! - 5) / (3+2)"  # 456.0
    ]

    for expr in test_expressions:
        try:
            result = calc.compile(expr)
            print(f"{expr:40} = {result}")
        except Exception as e:
            print(f"{expr:40} -> Ошибка: {e}")

    print("\n=== Тестирование OctCalc с унарным факториалом ===")
    oct_calc = OctCalc()

    oct_expressions = [
        "0o10!",                   # 8! = 40320
        "(0o10 + 0o2)!",           # 10! = 3628800
        "0o10! + 0o7!",            # 40320 + 5040 = 45360
        "0o20 * (0o10 + 0o3)! / 0o2",  # 16 * 39916800 / 2 = 319334400.0
        "0o777!",                  # 511! (огромное число, но допустимо)
        "0o7777!"                  # число >3999 → исключение
    ]

    for expr in oct_expressions:
        try:
            result = oct_calc.compile(expr)
            print(f"{expr:40} = {result}")
        except Exception as e:
            print(f"{expr:40} -> Ошибка: {e}")
            
    c = Calc_power()
    while True:
        str = input("Арифметическое выражение: ")
        print(f"Результат его вычисления: {c.compile(str)}")
        print()
