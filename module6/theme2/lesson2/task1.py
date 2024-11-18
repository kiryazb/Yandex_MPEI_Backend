import unittest


def bartender(order):
    if isinstance(order, int) and order > 0:
        return order
    return 'Извините, я не могу вас обслужить!'


class TestBar(unittest.TestCase):

    def test_bartender(self):
        test_cases = [
            (5, 5),  # Заказ 5 стаканов пива
            (0, 'Извините, я не могу вас обслужить!'),  # Заказ 0 стаканов пива
            (0.33, 'Извините, я не могу вас обслужить!'),  # Заказ 0.33 стакана пива
            (-1.999999, 'Извините, я не могу вас обслужить!'),  # Отрицательное число
            ('фываолдж', 'Извините, я не могу вас обслужить!')  # Некорректная строка
        ]

        for order, expected in test_cases:
            with self.subTest(order=order):
                self.assertEqual(bartender(order), expected)
