#!/usr/bin/env python3
"""
Интерпретатор арифметических выражений на основе стекового компилятора.
Поддерживает:
- десятичные и восьмеричные числа (0o...);
- операторы: +, -, *, /, **, ^, ! (постфиксный факториал);
- правоассоциативное возведение в степень.
Вычисляет значение выражения, используя стек чисел.
"""

import re
from operator import add, sub, mul, truediv, pow
from stack import Stack
from compf import Compf, Compf_power, OctCompf


class Calc(Compf):
    """
    Интерпретатор, наследующий компилятор Compf и добавляющий
    стек чисел для вычисления постфиксной формы.
    """

    # Переопределяем токенизацию для чисел (десятичные, восьмеричные)
    # и переменных (но в калькуляторе переменные не используются)
    TOKEN_PATTERN = re.compile(r"\*\*|[a-z]|0[oO][0-7]+|\d+|[()+\-*/^!]")

    def __init__(self):
        super().__init__()
        # Стек для чисел (результатов промежуточных вычислений)
        self.r = Stack()

    def compile(self, expr: str):
        """
        Преобразует выражение в постфиксную форму (через родительский метод)
        и вычисляет результат, используя стек r.
        """
        super().compile(expr)
        return self.r.top()

    def process_value(self, token: str):
        """
        Обработка операнда: преобразует токен в число и помещает в стек.
        Для восьмеричных чисел выполняет преобразование из системы с основанием 8.
        """
        if token.startswith('0') and token[1].lower() == 'o':
            try:
                value = int(token, 8)
            except ValueError:
                raise Exception(f"Некорректное восьмеричное число: {token}")
            if value < 0 or value > 3999:
                raise Exception(f"Число {token} выходит за допустимый диапазон [0, 3999]")
            self.r.push(value)
        else:
            # Десятичное число
            self.r.push(int(token))

    def process_oper(self, token: str):
        """
        Обработка оператора: извлекает операнды из стека, выполняет операцию
        и помещает результат обратно.
        """
        if token == '!':
            val = self.r.pop()
            self.r.push(self.factorial(val))
        else:
            second = self.r.pop()
            first = self.r.pop()
            op = {
                "+": add, "-": sub, "*": mul,
                "/": truediv, "**": pow, "^": pow
            }[token]
            self.r.push(op(first, second))

    @staticmethod
    def factorial(n: int) -> int:
        """Вычисляет факториал целого неотрицательного числа."""
        if not isinstance(n, int) or n < 0:
            raise Exception("Факториал определён только для неотрицательных целых чисел")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


# ----------------------------- Подклассы для обратной совместимости -----------------------------

class Calc_power(Calc):
    """Подкласс для совместимости с исходными тестами (возведение в степень)."""
    pass


class OctCalc(OctCompf, Calc):
    """
    Калькулятор, работающий только с восьмеричными числами.
    Использует множественное наследование: компиляцию от OctCompf, вычисление от Calc.
    """
    def compile(self, expr: str):
        # Вызываем компиляцию из OctCompf (которая уже переопределена)
        OctCompf.compile(self, expr)
        return self.r.top()


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
        try:
            expr = input("Арифметическое выражение: ")
            print(f"Результат его вычисления: {c.compile(expr)}")
        except Exception as e:
            print(f"Ошибка: {e}")
        print()