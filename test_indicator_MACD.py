from unittest import TestCase
import unittest
from enum_classes import EnumPair
from order_book import OrderBook
import copy

from enum_classes import EnumCcy
from indicator_MACD import IndicatorMACD
from order_book_high_freq_fx import OrderBookHighFreqFx
from quote import Quote

class TestIndicatorMACD(TestCase):
    #This code tests the capabilities of the MACD indicator class.
    def test_constructor(self):
        macd = IndicatorMACD(12,26,9)
        self.assertEqual("MACD Indicator with short=12, long=26, signal=9.", macd.get_doc_description())
        self.assertEqual("MACD_12_26_9", macd.get_description())
        return_size = macd.get_return_size()
        self.assertEqual(tuple, type(return_size))
        self.assertEqual((3, ), return_size)
        self.assertEqual(1, len(return_size))

    def test_insert_quotes(self):
        ob = OrderBookHighFreqFx(EnumPair.EURUSD)
        quote_1 = Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000.00, 0.00, 0.00, 10.00, True)
        quote_2 = Quote(2, EnumCcy.EUR, EnumCcy.USD, 1, 1, 1000.00, 0.00, 0.00, 11.00, True)
        quote_3 = Quote(3, EnumCcy.EUR, EnumCcy.USD, 2, 2, 1000.00, 0.00, 0.00, 12.00, True)
        quote_4 = Quote(4, EnumCcy.EUR, EnumCcy.USD, 3, 3, 1000.00, 0.00, 0.00, 13.00, True)
        quote_5 = Quote(5, EnumCcy.EUR, EnumCcy.USD, 4, 4, 1000.00, 0.00, 0.00, 14.00, True)
        quote_6 = Quote(6, EnumCcy.EUR, EnumCcy.USD, 5, 5, 1000.00, 0.00, 0.00, 15.00, True)
        quote_7 = Quote(7, EnumCcy.EUR, EnumCcy.USD, 6, 6, 1000.00, 0.00, 0.00, 16.00, True)
        quote_8 = Quote(8, EnumCcy.EUR, EnumCcy.USD, 7, 7, 1000.00, 0.00, 0.00, 17.00, True)
        quote_9 = Quote(9, EnumCcy.EUR, EnumCcy.USD, 8, 8, 1000.00, 0.00, 0.00, 18.00, True)
        quote_10 = Quote(10, EnumCcy.EUR, EnumCcy.USD, 9, 9, 1000.00, 0.00, 0.00, 19.00, True)
        quote_11 = Quote(11, EnumCcy.EUR, EnumCcy.USD, 10, 10, 1000.00, 0.00, 0.00, 20.00, True)
        quote_12 = Quote(12, EnumCcy.EUR, EnumCcy.USD, 11, 11, 1000.00, 0.00, 0.00, 21.00, True)        
        
        macd = IndicatorMACD(12,26,9)

        ob.set_indicators([macd])

        ob.incoming_quote(quote_1)
        ob.incoming_quote(quote_2)
        ob.incoming_quote(quote_3)
        ob.incoming_quote(quote_4)
        ob.incoming_quote(quote_5)
        ob.incoming_quote(quote_6)
        ob.incoming_quote(quote_7)
        ob.incoming_quote(quote_8)
        ob.incoming_quote(quote_9)
        ob.incoming_quote(quote_10)

        self.assertEqual((0.98492, 0.46876, 0.51615), (round(macd.get_current_value()[0],5), round(macd.get_current_value()[1],5), round(macd.get_current_value()[2],5)))
        self.assertEqual(tuple, type(macd.get_current_value()))

        ob.incoming_quote(quote_11)
        ob.incoming_quote(quote_12)

        self.assertEqual((1.25728, 0.71646, 0.54082), (round(macd.get_current_value()[0],5), round(macd.get_current_value()[1],5), round(macd.get_current_value()[2],5)))


    def test_deep_copy(self):
        macd = IndicatorMACD(12,26,9)
        macd_deep_copy = copy.deepcopy(macd)
        self.assertEqual("MACD Indicator with short=12, long=26, signal=9.", macd_deep_copy.get_doc_description())
        self.assertEqual("MACD_12_26_9", macd_deep_copy.get_description())
        self.assertTrue(macd != macd_deep_copy)

if __name__ == "__main__":
     unittest.main()