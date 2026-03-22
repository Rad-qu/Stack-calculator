#!/usr/bin/env python3

import re
from stack import Stack


class Compf:
    """
    Стековый компилятор формул преобразует правильные
    арифметические формулы (цепочки языка, задаваемого
    грамматикой G0) в программы для стекового калькулятора
    (цепочки языка, определяемого грамматикой Gs):
    ...

    В качестве операндов в формулах допустимы только
    однобуквенные имена переменных [a-z]
    """

    SYMBOLS = re.compile("[a-z]")

    def __init__(self):
        self.s = Stack()
        self.data = []

    def compile(self, str):
        self.data.clear()
        # Удаляем все пробельные символы, чтобы избежать ошибок
        str = ''.join(str.split())
        # Последовательный вызов для всех символов взятой в скобки формулы
        for c in "(" + str + ")":
            self.process_symbol(c)
        return " ".join(self.data)

    def process_symbol(self, c):
        if c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in "+-*/":
            self.process_suspended_operators(c)
            self.s.push(c)
        elif c == '!':
            self.process_oper(c)   # максимальный приоритет -> сразу в вывод
        else:
            self.check_symbol(c)
            self.process_value(c)

    def process_suspended_operators(self, c):
        while self.is_precedes(self.s.top(), c):
            self.process_oper(self.s.pop())

    def process_value(self, c):
        self.data.append(c)

    def process_oper(self, c):
        self.data.append(c)

    @classmethod
    def check_symbol(self, c):
        if not self.SYMBOLS.match(c):
            raise Exception(f"Недопустимый символ '{c}'")

    @staticmethod
    def priority(c):
        return 1 if (c == "+" or c == "-") else 2

    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)


class OctCompf(Compf):
    def compile(self, expr):
        self.data.clear()
        tokens = self.SYMBOLS.findall("(" + expr + ")")
        for token in tokens:
            if token.startswith('0') and token[1].lower() == 'o':
                self.process_value(token)
            else:
                self.process_symbol(token)
        return " ".join(self.data)

    def process_value(self, c):
        try:
            value = int(c, 8)
        except ValueError:
            raise Exception(f"Некорректное восьмеричное число: {c}")
        if value < 0 or value > 3999:
            raise Exception(f"Число {c} выходит за допустимый диапазон [0, 3999]")
        self.data.append(str(value))

    @staticmethod
    def priority(c):
        if c == '/':
            return 0
        elif c == '*':
            return 2
        else:
            return 1


if __name__ == "__main__":
    c = OctCompf()
    expr = "0o10 + 0o2 / 0o5"
    print(f"Выражение: {expr}")
    print(f"Постфиксная форма: {c.compile(expr)}")