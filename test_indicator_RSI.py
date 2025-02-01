from unittest import TestCase
import unittest
from enum_classes import EnumPair
from order_book import OrderBook
import copy

from enum_classes import EnumCcy
from indicator_RSI import IndicatorRSI
from order_book_high_freq_fx import OrderBookHighFreqFx
from quote import Quote


class TestIndicatorMovingAverage(TestCase):
    # This code tests the capabilities of the RSI Indicator

    def test_constructor(self):
        rsi = IndicatorRSI(5)
        self.assertEqual("Relative Strength Index (RSI) over 5 periods.", rsi.get_doc_description())
        self.assertEqual("RSI_5", rsi.get_description())
        return_size = rsi.get_return_size()
        self.assertEqual(tuple, type(return_size))
        self.assertEqual((1,), return_size)
        self.assertEqual(1, len(return_size))

    def test_insert_quotes(self):
        ob = OrderBookHighFreqFx(EnumPair.EURUSD)
        quote_1 = Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000.00, 0.00, 0.00, 10.00, True)
        quote_2 = Quote(2, EnumCcy.EUR, EnumCcy.USD, 1, 1, 1000.00, 0.00, 0.00, 11.00, True)
        quote_3 = Quote(3, EnumCcy.EUR, EnumCcy.USD, 2, 2, 1000.00, 0.00, 0.00, 9.00, True)
        quote_4 = Quote(4, EnumCcy.EUR, EnumCcy.USD, 3, 3, 1000.00, 0.00, 0.00, 10.00, True)
        quote_5 = Quote(5, EnumCcy.EUR, EnumCcy.USD, 4, 4, 1000.00, 0.00, 0.00, 12.00, True)
        quote_6 = Quote(6, EnumCcy.EUR, EnumCcy.USD, 5, 5, 1000.00, 0.00, 0.00, 13.00, True)
        quote_7 = Quote(7, EnumCcy.EUR, EnumCcy.USD, 6, 6, 1000.00, 0.00, 0.00, 12.00, True)

        rsi = IndicatorRSI(5)

        ob.set_indicators([rsi])

        ob.incoming_quote(quote_1)
        ob.incoming_quote(quote_2)
        ob.incoming_quote(quote_3)
        ob.incoming_quote(quote_4)
        ob.incoming_quote(quote_5)

        self.assertEqual(50.0, rsi.get_current_value())
        self.assertEqual(float, type(rsi.get_current_value()))

        ob.incoming_quote(quote_6)
        ob.incoming_quote(quote_7)

        self.assertEqual(57.14286, round(rsi.get_current_value(),5))

    def test_deep_copy(self):
        rsi = IndicatorRSI(5)
        rsi_deep_copy = copy.deepcopy(rsi)
        self.assertEqual("Relative Strength Index (RSI) over 5 periods.", rsi_deep_copy.get_doc_description())
        self.assertEqual("RSI_5", rsi_deep_copy.get_description())
        self.assertTrue(rsi != rsi_deep_copy)

if __name__ == "__main__":
     unittest.main()