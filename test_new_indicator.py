from unittest import TestCase, main
from enum_classes import EnumPair, EnumCcy

from order_book_high_freq_fx import OrderBookHighFreqFx  # Classe concrète utilisée
from order_book import OrderBook
from quote import Quote
import numpy as np
from unittest.mock import MagicMock

from indicator_ATR import IndicatorATR

from datetime import datetime

from indicator_ADX import IndicatorADX
from indicator_VAROC import IndicatorVAROC


class TestIndicatorADX(TestCase):
    def setUp(self):
        self.order_book = OrderBookHighFreqFx(EnumPair.EURUSD)

    def test_adx_calculation(self):
        indicator = IndicatorADX(14)
        self.order_book.set_indicators([indicator])

        # Inject quotes
        quotes = [
            10, 15, 20, 18, 22, 25, 28, 30, 32, 35, 38, 36, 39, 40,
            40, 42, 43, 41, 44, 46, 45, 47, 48, 46, 50, 52, 51, 53, 54, 55
        ]
        # Injection des quotes dans l'OrderBook
        for i, price in enumerate(quotes, start=1):
            self.order_book.incoming_quote(Quote(i, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, price, True))

        adx = indicator.get_current_value()
        print(f"ADX calculated: {adx}")
        self.assertGreater(adx, 0)

    def test_adx_with_stagnation(self):
        indicator = IndicatorADX(14)
        self.order_book.set_indicators([indicator])

        for price in [10] * 20:  # Stagnation
            self.order_book.incoming_quote(Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, price, True))

        adx = indicator.get_current_value()
        print(f"ADX with stagnation: {adx}")
        self.assertEqual(adx, 0)

    def test_adx_reset(self):
        indicator = IndicatorADX(14)
        self.order_book.set_indicators([indicator])

        # Première série de quotes (au moins 27 quotes pour un calcul correct)
        initial_quotes = [
            10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
            80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140
        ]
        for i, price in enumerate(initial_quotes, start=1):
            self.order_book.incoming_quote(Quote(i, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, price, True))

        adx_before_reset = indicator.get_current_value()
        print(f"ADX before reset: {adx_before_reset}")
        self.assertGreater(adx_before_reset, 0)

        # Réinitialisation de l'OrderBook
        self.order_book = OrderBookHighFreqFx(EnumPair.EURUSD)
        self.order_book.set_indicators([indicator])

        # Nouvelle série de quotes (encore au moins 27)
        new_quotes = [
            140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200,
            205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270
        ]
        for i, price in enumerate(new_quotes, start=1):
            self.order_book.incoming_quote(Quote(i, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000, 0, 0, price, True))

        adx_after_reset = indicator.get_current_value()
        print(f"ADX after reset: {adx_after_reset}")
        self.assertGreater(adx_after_reset, 0)

class TestIndicatorVAROC(TestCase):
    def test_initialization(self):
        """Test l'initialisation de l'indicateur."""
        indicator = IndicatorVAROC(14)
        self.assertEqual(indicator.period, 14)
        self.assertIsNone(indicator.get_current_value())

    def test_incoming_quote_valid_update(self):
        """
        Test le bon fonctionnement de incoming_quote en utilisant des objets Quote valides.
        """
        indicator = IndicatorVAROC(period=14)

        # Création d'un ensemble d'objets Quote avec des prix croissants
        quotes = [
            Quote(
                quote_id_arg=i,
                currency1_arg="EUR",
                currency2_arg="USD",
                local_timestamp_arg=i * 1000,
                ecn_timestamp_arg=i * 2000,
                amount_arg=1000,
                minqty_arg=10,
                lotsize_arg=1,
                price_arg=100 + i,  # Prix croissants
                way_arg="B"
            )
            for i in range(20)  # Génère 20 quotes
        ]

        # Ajouter les quotes une par une et s'assurer qu'il n'y a pas d'erreur
        for quote in quotes:
            indicator.incoming_quote(quote)  # Passer chaque quote valide

        # Calcul manuel pour valider l'indicateur
        prices = [q.get_price() for q in quotes[-14:]]  # Les 14 dernières valeurs
        roc = ((prices[-1] - prices[0]) / prices[0]) * 100
        volatility = np.std(prices)
        expected_varoc = roc / volatility if volatility != 0 else 0

        # Vérifier la valeur calculée par l'indicateur
        self.assertAlmostEqual(indicator.get_current_value(), expected_varoc, places=5)

    def test_get_description(self):
        """Test de la description de l'indicateur."""
        indicator = IndicatorVAROC(14)
        self.assertEqual(indicator.get_description(), "VAROC_14")

    def test_get_return_size(self):
        """Test des dimensions de sortie de l'indicateur."""
        indicator = IndicatorVAROC(14)
        self.assertEqual(indicator.get_return_size(), (1,))


if __name__ == "__main__":
    main()