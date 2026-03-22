#!/usr/bin/env python3

import re
from operator import add, sub, mul, truediv
from stack import Stack
from compf import Compf, OctCompf


class Calc(Compf):
    """
    Интерпретатор арифметических выражений вычисляет значения
    правильных арифметических формул, в которых в качестве
    операндов допустимы только цифры [0-9]
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
        second = self.r.pop()
        first = self.r.pop()
        ops = {"+": add, "-": sub, "*": mul, "/": truediv}
        self.r.push(ops[c](first, second))


if __name__ == "__main__":
    # c = Calc()
    # while True:
    #     str = input("Арифметическое выражение: ")
    #     print(f"Результат его вычисления: {c.compile(str)}")
    #     print()

    expr = "0o20 * (0o10 + 0o3) / 0o2 - 0o7 * 0o5 + 0o12 / 0o4 + 0o1 * (0o30 - 0o10)"
    comp = OctCompf()
    print(f"Выражение: {expr}")
    print(f"Постфиксная форма: {comp.compile(expr)}")

    calc = OctCalc()
    print(f"Результат вычисления: {calc.compile(expr)}")