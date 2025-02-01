from unittest import TestCase
import unittest
from enum_classes import EnumPair
from order_book import OrderBook
import copy

from enum_classes import EnumCcy
from indicator_parabolic_stop_reverse import IndicatorSAR
from order_book_high_freq_fx import OrderBookHighFreqFx
from quote import Quote


class TestIndicatorMovingAverage(TestCase):
    # This code tests the capabilities of SAR Indicator

    def test_constructor(self):
        sar = IndicatorSAR(0.02, 0.2, -0.2, 10)
        self.assertEqual(("Parabolic SAR indicator with dynamic acceleration factor based on price movements, "
            "step 0.02, max AF 0.2, min AF -0.2, and a period of 10."), sar.get_doc_description())
        self.assertEqual("SAR_0.02_0.2_-0.2_10", sar.get_description())
        return_size = sar.get_return_size()
        self.assertEqual(tuple, type(return_size))
        self.assertEqual((1, ), return_size)
        self.assertEqual(1, len(return_size))

    def test_insert_quotes(self):
        ob = OrderBookHighFreqFx(EnumPair.EURUSD)
        quote_1 = Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000.00, 0.00, 0.00, 10.00, True)
        quote_2 = Quote(2, EnumCcy.EUR, EnumCcy.USD, 1, 1, 1000.00, 0.00, 0.00, 11.00, True)
        quote_3 = Quote(3, EnumCcy.EUR, EnumCcy.USD, 2, 2, 1000.00, 0.00, 0.00, 12.00, True)
        quote_4 = Quote(4, EnumCcy.EUR, EnumCcy.USD, 3, 3, 1000.00, 0.00, 0.00, 13.00, True)
        quote_5 = Quote(5, EnumCcy.EUR, EnumCcy.USD, 4, 4, 1000.00, 0.00, 0.00, 12.00, True)
        quote_6 = Quote(6, EnumCcy.EUR, EnumCcy.USD, 5, 5, 1000.00, 0.00, 0.00, 11.00, True)
        quote_7 = Quote(7, EnumCcy.EUR, EnumCcy.USD, 6, 6, 1000.00, 0.00, 0.00, 10.00, True)
        quote_8 = Quote(8, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000.00, 0.00, 0.00, 9.00, True)
        quote_9 = Quote(9, EnumCcy.EUR, EnumCcy.USD, 1, 1, 1000.00, 0.00, 0.00, 10.00, True)
        quote_10 = Quote(10, EnumCcy.EUR, EnumCcy.USD, 2, 2, 1000.00, 0.00, 0.00, 12.00, True)
        quote_11 = Quote(11, EnumCcy.EUR, EnumCcy.USD, 3, 3, 1000.00, 0.00, 0.00, 13.00, True)
        quote_12 = Quote(12, EnumCcy.EUR, EnumCcy.USD, 4, 4, 1000.00, 0.00, 0.00, 11.00, True)
        quote_13 = Quote(13, EnumCcy.EUR, EnumCcy.USD, 5, 5, 1000.00, 0.00, 0.00, 10.00, True)

        sar = IndicatorSAR(0.02, 0.2, -0.2, 10)

        ob.set_indicators([sar])

        ob.incoming_quote(quote_1)
        ob.incoming_quote(quote_2)
        ob.incoming_quote(quote_3)
        ob.incoming_quote(quote_4)
        ob.clear_orderbook()

        self.assertEqual(5.28, round(sar.get_current_value(),2))
        self.assertEqual(float, type(sar.get_current_value()))

        ob.incoming_quote(quote_5)
        ob.incoming_quote(quote_6)
        ob.incoming_quote(quote_7)
        ob.incoming_quote(quote_8)
        ob.clear_orderbook()

        self.assertEqual(6.78, round(sar.get_current_value(),2))

        ob.incoming_quote(quote_9)
        ob.incoming_quote(quote_10)
        ob.incoming_quote(quote_11)
        ob.incoming_quote(quote_12)
        ob.clear_orderbook()
        ob.incoming_quote(quote_13)

        self.assertEqual(10.16, round(sar.get_current_value(),2))

    def test_deep_copy(self):
        sar = IndicatorSAR(0.02, 0.2, -0.2, 10)
        sar_deep_copy = copy.deepcopy(sar)
        self.assertEqual(("Parabolic SAR indicator with dynamic acceleration factor based on price movements, "
            "step 0.02, max AF 0.2, min AF -0.2, and a period of 10."), sar_deep_copy.get_doc_description())
        self.assertEqual("SAR_0.02_0.2_-0.2_10", sar_deep_copy.get_description())
        self.assertTrue(sar != sar_deep_copy)

if __name__ == "__main__":
     unittest.main()