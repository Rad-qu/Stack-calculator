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
        elif c == '!':
            self.process_oper(c)   # максимальный приоритет -> сразу в вывод
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

class Compf_power(Compf):
    """
    
    Стековый компилятор формул с поддержкой возведения в степень(обозначается ** или ^),
    причем она является правоассоциативной, и имеющеет максимальный приоритет.
    При компиляции теперь используется токенизация
    
    """

    def __init__(self):
        super().__init__()

    TOKEN_PATTERN = re.compile(r"\*\*|[a-z]|[()+\-*/^]")

    def tokenize(self, expr):
        return re.findall(self.TOKEN_PATTERN, expr)
    
    def compile(self, str):
        self.data.clear()
        tokens = self.tokenize("(" + str + ")")
        for token in tokens:
            self.process_symbol(token)
        
        return " ".join(self.data)

    def process_symbol(self, token):
        if token == "(":
            self.s.push(token)
        elif token == ")":
            self.process_suspended_operators(token)
            self.s.pop()
        elif token in "+-*/^" or token == '**':
            self.process_suspended_operators(token)
            self.s.push(token)
        else:
            self.check_symbol(token)
            self.process_value(token)
    
    def process_suspended_operators(self, token):
        return super().process_suspended_operators(token)
    
    @staticmethod
    def priority(op):
        if op in "+-": return 1
        elif op in "*/": return 2
        else: return 3

    @staticmethod
    def is_right_associative(op):
        right_associative_operators = ("**", "^")
        return op in right_associative_operators

    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        if b == ")":
            return True
        if Compf_power.priority(a) > Compf_power.priority(b):
            return True
        if Compf_power.priority(a) < Compf_power.priority(b):
            return False
        return not Compf_power.is_right_associative(b)
      
class Compf_power_low_priority(Compf_power):

    @staticmethod
    def priority(op):
        if op in "+-": return 1
        elif op in "*/" or op == "**": return 2

class OctCompf(Compf):

    SYMBOLS = re.compile(r'0[oO][0-7]+|[()+\-*/!]')

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
    c = Compf_power()
    while True:
        str = input("Арифметическая  формула: ")
        print(f"Результат её компиляции: {c.compile(str)}")
        print()

