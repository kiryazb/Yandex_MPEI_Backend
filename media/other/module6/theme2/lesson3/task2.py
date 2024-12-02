import unittest


class Calculator:
    """Производит арифметические действия."""

    def summ(self, *args):
        """
        Возвращает сумму принятых аргументов,
        если аргументов нет, возвращает None.
        """
        if len(args) == 0:
            return None
        return sum(args)


class TestCalc(unittest.TestCase):
    """Тестируем Calculator."""

    @classmethod
    def setUpClass(cls):
        """Вызывается один раз перед запуском всех тестов класса."""
        cls.calc = Calculator()

    def test_summ(self):
        self.assertEqual(self.calc.summ(1, 2, -3), 0)

    def test_summ_no_argument(self):
        self.assertIsNone(self.calc.summ())

    def test_summ_one_argument(self):
        self.assertEqual(self.calc.summ(-3), -3)
