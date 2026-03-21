from pytest import approx, raises
from calc import Calc


class TestCalc:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.c = Calc()

    # Интерпретатор арифметических выражений работает только с цифрами
    def test_raises(self):
        with raises(Exception):
            self.c.compile('a')

    # Тесты на сложение
    def test_addition1(self):
        assert self.c.compile('1+2') == 3

    def test_addition2(self):
        assert self.c.compile('1+2+3+4+5+6') == 21

    def test_addition3(self):
        assert self.c.compile('(1+2)+(3+4)') == 10

    def test_addition4(self):
        assert self.c.compile('(1+(2+3)+4)') == 10

    # Тесты на вычитание
    def test_subtraction1(self):
        assert self.c.compile('1-2') == -1

    def test_subtraction2(self):
        assert self.c.compile('5-2') == 3

    def test_subtraction3(self):
        assert self.c.compile('1-2-3-4-5-6') == -19

    def test_subtraction4(self):
        assert self.c.compile('(1-2)-(3-4)') == 0

    # Тесты на умножение
    def test_multiplication1(self):
        assert self.c.compile('1*2') == 2

    def test_multiplication2(self):
        assert self.c.compile('0*3') == 0

    def test_multiplication3(self):
        assert self.c.compile('7*1*1*1') == 7

    def test_multiplication4(self):
        assert self.c.compile('2*5*2') == 20

    # Тесты на деление
    def test_division1(self):
        assert self.c.compile('1/2') == approx(0.5)

    def test_division2(self):
        assert self.c.compile('2/1') == approx(2.0)

    def test_division3(self):
        assert self.c.compile('0/3') == approx(0.0)

    def test_division4(self):
        assert self.c.compile('8/2/2/2') == approx(1.0)

    def test_division5(self):
        with raises(ZeroDivisionError):
            self.c.compile('1/0')

    # Тесты на сложные арифметические выражения
    def test_expressions1(self):
        assert self.c.compile('(1-2)') == -1

    def test_expressions2(self):
        assert self.c.compile('(1+4)*7') == 35

    def test_expressions3(self):
        assert self.c.compile('7*(8)/4') == approx(14.0)

    def test_expressions4(self):
        test = '1+2+(2*(3+7))/(5+8/3)'
        assert self.c.compile(test) == approx(eval(test))

    def test_expressions5(self):
        test = '(3-5-2*6/(1+1))/(2*5-1+4*(5*2/3))+(7+4+7/9)/(1+6/3)'
        assert self.c.compile(test) == approx(eval(test))
