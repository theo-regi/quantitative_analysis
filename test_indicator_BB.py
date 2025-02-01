from unittest import TestCase
import unittest
from enum_classes import EnumPair
from order_book import OrderBook
import copy

from enum_classes import EnumCcy
from indicator_bollinger_bands import IndicatorBollingerBands
from order_book_high_freq_fx import OrderBookHighFreqFx
from quote import Quote


class TestIndicatorBB(TestCase):
    # This code tests the capabilities of the indicator Bollinger Bands

    def test_constructor(self):
        bb = IndicatorBollingerBands(5, 2, 3, 5)
        self.assertEqual(("Bollinger Bands with 5 periods and multiplier 2. "
            "BBW with short SMA (3) and long SMA (5)."), bb.get_doc_description())
        self.assertEqual("BOLL_5_2_BBW_3_5", bb.get_description())
        return_size = bb.get_return_size()
        self.assertEqual(tuple, type(return_size))
        self.assertEqual((6, ), return_size)
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

        bb = IndicatorBollingerBands(5,2,3,5)

        ob.set_indicators([bb])

        ob.incoming_quote(quote_1)
        ob.incoming_quote(quote_2)
        ob.incoming_quote(quote_3)
        ob.incoming_quote(quote_4)
        ob.incoming_quote(quote_5)

        self.assertEqual((4.59, 6, 7.41, 0.47, 0.16, 0.09), 
                         (round(bb.get_current_value()[0], 2),
                          round(bb.get_current_value()[1], 2),
                          round(bb.get_current_value()[2], 2),
                          round(bb.get_current_value()[3], 2),
                          round(bb.get_current_value()[4], 2),
                          round(bb.get_current_value()[5], 2),
                          ))
        self.assertEqual(tuple, type(bb.get_current_value()))
    
        ob.incoming_quote(quote_6)
        ob.incoming_quote(quote_7)

        self.assertEqual((5.59, 7, 8.41, 0.4, 0.44, 0.26), 
                         (round(bb.get_current_value()[0], 2),
                          round(bb.get_current_value()[1], 2),
                          round(bb.get_current_value()[2], 2),
                          round(bb.get_current_value()[3], 2),
                          round(bb.get_current_value()[4], 2),
                          round(bb.get_current_value()[5], 2),
                          ))
        
    def test_deep_copy(self):
        bb = IndicatorBollingerBands(5, 2, 3, 5)
        bb_deep_copy = copy.deepcopy(bb)

        self.assertEqual(("Bollinger Bands with 5 periods and multiplier 2. "
            "BBW with short SMA (3) and long SMA (5)."), bb_deep_copy.get_doc_description())
        self.assertEqual("BOLL_5_2_BBW_3_5", bb_deep_copy.get_description())

        self.assertTrue(bb != bb_deep_copy)

if __name__ == "__main__":
     unittest.main()