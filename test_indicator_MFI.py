from unittest import TestCase
import unittest
from enum_classes import EnumPair
from order_book import OrderBook
import copy

from enum_classes import EnumCcy
from indicator_money_flow_index import IndicatorMoneyFlowIndex
from order_book_high_freq_fx import OrderBookHighFreqFx
from quote import Quote


class TestIndicatorMovingAverage(TestCase):
    # This code tests the capabilities of the MFI Indicator

    def test_constructor(self):
        mfi = IndicatorMoneyFlowIndex(14)
        self.assertEqual("Money Flow Index (MFI) with 14 periods, based on volume variation and price movements over the period.", mfi.get_doc_description())
        self.assertEqual("MFI_14", mfi.get_description())
        return_size = mfi.get_return_size()
        self.assertEqual(tuple, type(return_size))
        self.assertEqual((1,), return_size)
        self.assertEqual(1, len(return_size))

    def test_insert_quotes(self):
        ob = OrderBookHighFreqFx(EnumPair.EURUSD)
        quote_1 = Quote(1, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000.00, 0.00, 0.00, 10.00, True)
        quote_2 = Quote(2, EnumCcy.EUR, EnumCcy.USD, 1, 1, 5000.00, 0.00, 0.00, 11.00, True)
        quote_3 = Quote(3, EnumCcy.EUR, EnumCcy.USD, 2, 2, 2000.00, 0.00, 0.00, 12.00, True)
        quote_4 = Quote(4, EnumCcy.EUR, EnumCcy.USD, 3, 3, 3000.00, 0.00, 0.00, 11.00, True)
        quote_5 = Quote(5, EnumCcy.EUR, EnumCcy.USD, 4, 4, 1000.00, 0.00, 0.00, 10.00, True)
        quote_6 = Quote(6, EnumCcy.EUR, EnumCcy.USD, 5, 5, 2000.00, 0.00, 0.00, 9.00, True)

        quote_8 = Quote(8, EnumCcy.EUR, EnumCcy.USD, 0, 0, 1000.00, 0.00, 0.00, 13.00, False)
        quote_9 = Quote(9, EnumCcy.EUR, EnumCcy.USD, 1, 1, 5000.00, 0.00, 0.00, 14.00, False)
        quote_10 = Quote(10, EnumCcy.EUR, EnumCcy.USD, 2, 2, 2000.00, 0.00, 0.00, 14.00, False)
        quote_11 = Quote(11, EnumCcy.EUR, EnumCcy.USD, 3, 3, 3000.00, 0.00, 0.00, 15.00, False)
        quote_12 = Quote(12, EnumCcy.EUR, EnumCcy.USD, 4, 4, 1000.00, 0.00, 0.00, 14.00, False)
        quote_13 = Quote(13, EnumCcy.EUR, EnumCcy.USD, 5, 5, 2000.00, 0.00, 0.00, 13.00, False)

        mfi = IndicatorMoneyFlowIndex(3)

        ob.set_indicators([mfi])

        ob.incoming_quote(quote_1)
        ob.incoming_quote(quote_2)
        ob.incoming_quote(quote_3)
        ob.incoming_quote(quote_8)
        ob.incoming_quote(quote_9)
        ob.incoming_quote(quote_10)

        self.assertEqual(None, mfi.get_current_value())
        ob.clear_orderbook()

        ob.incoming_quote(quote_4)
        ob.incoming_quote(quote_5)
        ob.incoming_quote(quote_6)
        ob.incoming_quote(quote_11)
        ob.incoming_quote(quote_12)
        ob.incoming_quote(quote_13)

        self.assertEqual(66.97248, round(mfi.get_current_value(),5))
        self.assertEqual(float, type(mfi.get_current_value()))

    def test_deep_copy(self):
        mfi = IndicatorMoneyFlowIndex(14)
        mfi_deep_copy = copy.deepcopy(mfi)
        self.assertEqual("Money Flow Index (MFI) with 14 periods, based on volume variation and price movements over the period.", mfi_deep_copy.get_doc_description())
        self.assertEqual("MFI_14", mfi_deep_copy.get_description())
        self.assertTrue(mfi != mfi_deep_copy)

if __name__ == "__main__":
    unittest.main()