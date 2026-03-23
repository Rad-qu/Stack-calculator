import re
from stack import Stack

class Compf:
    """
    Стековый компилятор формул
    Преобразует инфиксную форму в постфиксную для стекового калькулятора.
    """

    # Регулярное выражение для токенизации:
    #   ** - оператор возведения в степень,
    #   [a-z] - переменные,
    #   0[oO][0-7]+ - восьмеричные числа,
    #   \d+ - десятичные числа,
    #   [()+\-*/^!] - скобки и остальные операторы.
    TOKEN_PATTERN = re.compile(r"\*\*|[a-z]|0[oO][0-7]+|\d+|[()+\-*/^!]")
    SYMBOLS = re.compile(r"[a-z]|\d+|0[oO][0-7]+")

    def __init__(self):
        # Стек отложенных операций
        self.s = Stack()
        # Список для сбора выходной постфиксной строки
        self.data = []

    def compile(self, expr: str) -> str:
        """
        Преобразует инфиксную формулу в постфиксную.
        """
        self.data.clear()
        tokens = self.tokenize("(" + expr + ")")
        for token in tokens:
            self.process_symbol(token)
        return " ".join(self.data)

    def tokenize(self, expr: str) -> list:
        """Разбивает выражение на токены."""
        return re.findall(self.TOKEN_PATTERN, expr)

    def process_symbol(self, token: str):
        """Обрабатывает один токен в соответствии с алгоритмом сортировочной станции."""
        if token == "(":
            self.s.push(token)
        elif token == ")":
            # Выталкиваем операторы до открывающей скобки
            self.process_suspended_operators(token)
            self.s.pop()                # удаляем '('
        elif self.is_operator(token):
            # Обрабатываем все отложенные операторы с бо́льшим или равным приоритетом
            self.process_suspended_operators(token)
            self.s.push(token)
        elif token == "!":
            # Постфиксный факториал: максимальный приоритет -> сразу в вывод
            self.process_oper(token)
        else:
            # Операнд: число, восьмеричное число или переменная
            self.check_symbol(token)
            self.process_value(token)

    def process_suspended_operators(self, token: str):
        """Выталкивает операторы из стека, пока верхний имеет приоритет выше или равен token."""
        while not self.s.is_empty() and self.is_precedes(self.s.top(), token):
            self.process_oper(self.s.pop())

    def process_value(self, token: str):
        """
        Добавляет операнд в выходную строку.
        Для восьмеричных чисел преобразует их в десятичное строковое представление,
        для десятичных и переменных оставляет как есть.
        """
        if token.startswith('0') and token[1].lower() == 'o':
            # Восьмеричное число -> десятичное
            try:
                value = int(token, 8)
            except ValueError:
                raise Exception(f"Некорректное восьмеричное число: {token}")
            if value < 0 or value > 3999:
                raise Exception(f"Число {token} выходит за допустимый диапазон [0, 3999]")
            self.data.append(str(value))
        else:
            # Десятичное число или переменная
            self.data.append(token)

    def process_oper(self, token: str):
        """Добавляет оператор в выходную строку."""
        self.data.append(token)

    def check_symbol(self, token: str):
        """Проверяет, что токен является допустимым операндом (число или переменная)."""
        if not re.match(self.SYMBOLS, token):
            raise Exception(f"Недопустимый операнд: '{token}'")

    @staticmethod
    def is_operator(token: str) -> bool:
        """Возвращает True, если токен является бинарным оператором."""
        return token in "+-*/^**"

    @staticmethod
    def priority(op: str) -> int:
        """Возвращает приоритет оператора (чем больше, тем выше)."""
        if op in "+-":
            return 1
        elif op in "*/":
            return 2
        else:  # ^, **
            return 3

    @staticmethod
    def is_right_associative(op: str) -> bool:
        """Возвращает True для правоассоциативных операторов."""
        return op in ("**", "^")

    @staticmethod
    def is_precedes(a: str, b: str) -> bool:
        """
        Определяет, должен ли оператор a быть выполнен раньше, чем b.
        Возвращает True, если a имеет более высокий приоритет,
        либо при равном приоритете и b не является правоассоциативным.
        """
        if a == "(":
            return False
        if b == ")":
            return True
        pa = Compf.priority(a)
        pb = Compf.priority(b)
        if pa > pb:
            return True
        if pa < pb:
            return False
        # Приоритеты равны – выталкиваем, если b не правоассоциативный
        return not Compf.is_right_associative(b)

class Compf_power(Compf):
    """
    Подкласс, поддерживающий возведение в степень (как и базовый класс).
    Оставлен для совместимости с исходными тестами.
    """
    pass


class Compf_power_low_priority(Compf_power):
    """
    Вариант, где ** имеет тот же приоритет, что и * и /.
    Переопределяем priority.
    """
    @staticmethod
    def priority(op: str) -> int:
        if op in "+-":
            return 1
        elif op in "*/**":
            return 2
        else:
            return 3


class OctCompf(Compf):
    """
    Компилятор, работающий только с восьмеричными числами (без переменных).
    Переопределяем токенизацию и проверку символов.
    """
    TOKEN_PATTERN = re.compile(r"0[oO][0-7]+|[()+\-*/!]")

    def check_symbol(self, token: str):
        if not re.match(r"0[oO][0-7]+", token):
            raise Exception(f"Недопустимый символ: {token}")


if __name__ == "__main__":
    # Тестирование компиляторов (исходные тесты работают с новыми классами)
    c = OctCompf()
    expr = "0o10 + 0o2 / 0o5"
    print(f"Выражение: {expr}")
    print(f"Постфиксная форма: {c.compile(expr)}")

    c = Compf_power()
    while True:
        try:
            expr = input("Арифметическая формула: ")
            print(f"Результат её компиляции: {c.compile(expr)}")
        except Exception as e:
            print(f"Ошибка: {e}")
        print()