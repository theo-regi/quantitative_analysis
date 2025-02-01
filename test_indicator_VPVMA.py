from unittest import TestCase, main

from enum_classes import EnumPair, EnumCcy
from order_book import OrderBook
from quote import Quote
from indicator_VPVMA import IndicatorVPVMA


class TestIndicatorVPVMA(TestCase):
    def setUp(self):
        self.order_book = OrderBook()
        self.vpvma_indicator = IndicatorVPVMA(fast_period=12, slow_period=26, signal_period=9, bandwidth=0.1)
        self.order_book.set_indicators([self.vpvma_indicator])

    def test_vpvma_initial_state(self):
        """
        Vérifie que la valeur initiale de VPVMA est None.
        """
        vpvma_value = self.vpvma_indicator.get_current_value()
        print(f"Initial VPVMA value: {vpvma_value}")
        self.assertIsNone(vpvma_value[0], "VPVMA should initially be None")
        self.assertIsNone(vpvma_value[1], "Signal line should initially be None")

    def test_vpvma_with_insufficient_data(self):
        """
        Vérifie le comportement avec un nombre insuffisant de quotes.
        """
        self.order_book.incoming_quote(Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, 1.1, True))
        self.order_book.incoming_quote(Quote(2, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2000, 0, 0, 1.2, True))

        vpvma_value = self.vpvma_indicator.get_current_value()
        self.assertIsNone(vpvma_value[0], "VPVMA should be None with insufficient data")
        self.assertIsNone(vpvma_value[1], "Signal line should be None with insufficient data")

    def test_vpvma_calculation(self):
        quotes = [
            Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, 1.10, True),
            Quote(2, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1050, 0, 0, 1.12, True),
            Quote(3, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2000, 0, 0, 1.08, True),
            Quote(4, EnumCcy.EUR, EnumCcy.USD, 0, 0, 500, 0, 0, 1.15, True),
            Quote(5, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1250, 0, 0, 1.11, True),
            Quote(6, EnumCcy.EUR, EnumCcy.USD, 0, 0, 4000, 0, 0, 1.14, True),
            Quote(7, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1350, 0, 0, 1.09, True),
            Quote(8, EnumCcy.EUR, EnumCcy.USD, 0, 0, 100, 0, 0, 1.16, True),
            Quote(9, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1400, 0, 0, 1.13, True),
            Quote(10, EnumCcy.EUR, EnumCcy.USD, 0, 0, 900, 0, 0, 1.12, True),
            Quote(11, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2900, 0, 0, 1.18, True),
            Quote(12, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, 1.10, True),
            Quote(13, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1650, 0, 0, 1.17, True),
            Quote(14, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1200, 0, 0, 1.09, True),
            Quote(15, EnumCcy.EUR, EnumCcy.USD, 0, 0, 150, 0, 0, 1.20, True),
            Quote(16, EnumCcy.EUR, EnumCcy.USD, 0, 0, 3500, 0, 0, 1.12, True),
            Quote(17, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1850, 0, 0, 1.15, True),
            Quote(18, EnumCcy.EUR, EnumCcy.USD, 0, 0, 100, 0, 0, 1.08, True),
            Quote(19, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1100, 0, 0, 1.14, True),
            Quote(20, EnumCcy.EUR, EnumCcy.USD, 0, 0, 200, 0, 0, 1.09, True),
            Quote(21, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2050, 0, 0, 1.16, True),
            Quote(22, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2100, 0, 0, 1.11, True),
            Quote(23, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2950, 0, 0, 1.19, True),
            Quote(24, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2200, 0, 0, 1.13, True),
            Quote(25, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1290, 0, 0, 1.08, True),
            Quote(26, EnumCcy.EUR, EnumCcy.USD, 0, 0, 3000, 0, 0, 1.14, True),
            Quote(27, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2350, 0, 0, 1.12, True),
            Quote(28, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2400, 0, 0, 1.18, True),
            Quote(29, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1450, 0, 0, 1.10, True),
            Quote(30, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2400, 0, 0, 1.15, True),
            Quote(31, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1250, 0, 0, 1.09, True),
            Quote(32, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2400, 0, 0, 1.13, True),
            Quote(33, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2650, 0, 0, 1.11, True),
            Quote(34, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2700, 0, 0, 1.19, True),
            Quote(35, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2750, 0, 0, 1.10, True),
            Quote(36, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2100, 0, 0, 1.16, True),
            Quote(37, EnumCcy.EUR, EnumCcy.USD, 0, 0, 3550, 0, 0, 1.09, True),
            Quote(38, EnumCcy.EUR, EnumCcy.USD, 0, 0, 3200, 0, 0, 1.20, True),
            Quote(39, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2150, 0, 0, 1.14, True),
            Quote(40, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2900, 0, 0, 1.08, True),
            Quote(41, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1950, 0, 0, 1.12, True),
            Quote(42, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2600, 0, 0, 1.15, True),
            Quote(43, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2950, 0, 0, 1.11, True),
            Quote(44, EnumCcy.EUR, EnumCcy.USD, 0, 0, 3900, 0, 0, 1.13, True),
            Quote(45, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1050, 0, 0, 1.18, True),
            Quote(46, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2300, 0, 0, 1.09, True),
            Quote(47, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1850, 0, 0, 1.17, True),
            Quote(48, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2000, 0, 0, 1.10, True),
            Quote(49, EnumCcy.EUR, EnumCcy.USD, 0, 0, 3950, 0, 0, 1.16, True),
            Quote(50, EnumCcy.EUR, EnumCcy.USD, 0, 0, 300, 0, 0, 1.12, True),
            Quote(51, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1950, 0, 0, 1.12, True),
            Quote(52, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2600, 0, 0, 1.15, True),
            Quote(53, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2050, 0, 0, 0.8, True),
            Quote(54, EnumCcy.EUR, EnumCcy.USD, 0, 0, 3200, 0, 0, 1.13, True),
            Quote(55, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1980, 0, 0, 1.8, True),
            Quote(56, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1300, 0, 0, 1.27, True),
            Quote(57, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1850, 0, 0, 1.17, True),
            Quote(58, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2000, 0, 0, 1.10, True),
            Quote(59, EnumCcy.EUR, EnumCcy.USD, 0, 0, 350, 0, 0, 1.29, True),
            Quote(60, EnumCcy.EUR, EnumCcy.USD, 0, 0, 5000, 0, 0, 1.01, True),
        ]

        for quote in quotes:
            self.order_book.incoming_quote(quote)

        vpvma_value = self.vpvma_indicator.get_current_value()
        print(f"Calculated VPVMA value: {vpvma_value}")
        self.assertIsNotNone(vpvma_value[0], "VPVMA should be calculable after sufficient data")

    def test_current_signal_update(self):
        """
        Teste que l'attribut `self.current_signal` est correctement mis à jour.
        """
        quotes = [
            Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, 1.10, True),  # Pas assez de données
            Quote(2, EnumCcy.EUR, EnumCcy.USD, 0, 0, 2000, 0, 0, 1.20, True),  # Pas assez de données
            Quote(3, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1500, 0, 0, 1.25, True),  # Pas assez de données
            Quote(4, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1200, 0, 0, 1.15, True),  # Pas assez de données
            Quote(5, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1800, 0, 0, 1.30, True),  # BUY
            Quote(6, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1400, 0, 0, 1.10, True),  # SELL
        ]

        # La période minimale pour générer des signaux correspond à `max(fast_period, slow_period, signal_period)`
        sufficient_data_period = max(
            self.vpvma_indicator.fast_period,
            self.vpvma_indicator.slow_period,
            self.vpvma_indicator.signal_period
        )

        # Avant d'atteindre sufficient_data_period, tous les signaux sont "HOLD"
        expected_signals = ["HOLD"] * sufficient_data_period + ["BUY", "SELL"]

        for i, quote in enumerate(quotes):
            self.order_book.incoming_quote(quote)  # Ajoute la quote dans le carnet d'ordres
            signal = self.vpvma_indicator.get_signal()  # Récupère le signal via get_signal()
            print(f"Quote {i + 1}: Expected Signal: {expected_signals[i]}, Actual Signal: {signal}")
            self.assertEqual(signal, expected_signals[i])  # Vérifie si le signal est correct

    def test_vpvma_is_ready(self):
        """
        Vérifie si l'indicateur devient prêt après suffisamment de données.
        """
        for i in range(30):
            quote = Quote(i, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, 1.1 + i * 0.01, True)
            self.order_book.incoming_quote(quote)

        self.assertTrue(self.vpvma_indicator.is_ready(), "VPVMA should be ready after receiving sufficient data")


if __name__ == "__main__":
    main()