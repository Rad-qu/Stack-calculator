#!/usr/bin/env python3

import re
from project.stack import Stack


class Compf:
    """
    Стековый компилятор формул преобразует правильные
    арифметические формулы (цепочки языка, задаваемого
    грамматикой G0) в программы для стекового калькулятора
    (цепочки языка, определяемого грамматикой Gs):

    G0:
        F  ->  T  |  F+T  |  F-T
        T  ->  M  |  T*M  |  T/M
        M  -> (F) |   V
        V  ->  a  |   b   |   c   |  ...  |    z

    Gs:
        e  ->  e e + | e e - | e e * | e e / |
                     | a | b | ... | z
    В качестве операндов в формулах допустимы только
    однобуквенные имена переменных [a-z]
    """

    SYMBOLS = re.compile("[a-z]")

    def __init__(self):
        # Создание стека отложенных операций
        self.s = Stack()
        # Создание списка с результатом компиляции
        self.data = []

    def compile(self, str):
        self.data.clear()
        # Последовательный вызов для всех символов
        # взятой в скобки формулы метода process_symbol
        for c in "(" + str + ")":
            self.process_symbol(c)
        return " ".join(self.data)

    # Обработка символа
    def process_symbol(self, c):
        if c == "(":
            self.s.push(c)
        elif c == ")":
            self.process_suspended_operators(c)
            self.s.pop()
        elif c in "+-*/":
            self.process_suspended_operators(c)
            self.s.push(c)
        else:
            self.check_symbol(c)
            self.process_value(c)

    # Обработка отложенных операций
    def process_suspended_operators(self, c):
        while self.is_precedes(self.s.top(), c):
            self.process_oper(self.s.pop())

    # Обработка имени переменной
    def process_value(self, c):
        self.data.append(c)

    # Обработка символа операции
    def process_oper(self, c):
        self.data.append(c)

    # Проверка допустимости символа
    @classmethod
    def check_symbol(self, c):
        if not self.SYMBOLS.match(c):
            raise Exception(f"Недопустимый символ '{c}'")

    # Определение приоритета операции
    @staticmethod
    def priority(c):
        return 1 if (c == "+" or c == "-") else 2

    # Определение отношения предшествования
    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)


class OctCompf(Compf):
    SYMBOLS = re.compile(r'0[oO][0-7]+|[()+\-*/]')

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
    # c = Compf()
    # while True:
    #     inp = input("Арифметическая  формула: ")
    #     print(f"Результат её компиляции: {c.compile(inp)}")
    #     print()

        #Тест для восьмеричной системы
    c = OctCompf()
    expr = "0o10 + 0o2 / 0o5"
    print(f"Выражение: {expr}")
    print(f"Постфиксная форма: {c.compile(expr)}")
