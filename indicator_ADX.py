from collections import deque
from math import fabs
from copy import deepcopy
from indicator import Indicator
from quote import Quote

class IndicatorADX(Indicator):
    def __init__(self, period: int = 14):
        self.__period = period
        self.__true_range = deque(maxlen=period)
        self.__positive_dm = deque(maxlen=period)
        self.__negative_dm = deque(maxlen=period)
        self.__dx_list = deque(maxlen=period)
        self.__smoothed_tr = 0.0
        self.__smoothed_pos_dm = 0.0
        self.__smoothed_neg_dm = 0.0
        self.__adx = 0.0

    def incoming_quote(self, quote: Quote) -> None:
        best_bid = self._order_book.get_best_price(True)
        best_offer = self._order_book.get_best_price(False)

        # Initialize the first bid if no previous data exists
        if not self.__true_range:
            self.__true_range.append(best_bid)
            return

        previous_bid = self.__true_range[-1]

        # True Range Calculation
        tr = max(
            fabs(best_bid - previous_bid),
            fabs(best_offer - previous_bid),
            fabs(best_offer - best_bid)
        )
        self.__true_range.append(tr)

        # Directional Movement Calculation
        positive_dm = max(best_bid - previous_bid, 0) if best_bid > previous_bid else 0
        negative_dm = max(previous_bid - best_bid, 0) if previous_bid > best_bid else 0
        self.__positive_dm.append(positive_dm)
        self.__negative_dm.append(negative_dm)

        # Wait until we have enough data for smoothing
        if len(self.__true_range) < self.__period:
            return

        # Smoothing
        if len(self.__true_range) == self.__period:
            self.__smoothed_tr = sum(self.__true_range)
            self.__smoothed_pos_dm = sum(self.__positive_dm)
            self.__smoothed_neg_dm = sum(self.__negative_dm)
        else:
            self.__smoothed_tr = self.__smoothed_tr - (self.__smoothed_tr / self.__period) + tr
            self.__smoothed_pos_dm = self.__smoothed_pos_dm - (self.__smoothed_pos_dm / self.__period) + positive_dm
            self.__smoothed_neg_dm = self.__smoothed_neg_dm - (self.__smoothed_neg_dm / self.__period) + negative_dm

        # Directional Indices and DX
        if self.__smoothed_tr > 0:
            pos_di = (self.__smoothed_pos_dm / self.__smoothed_tr) * 100
            neg_di = (self.__smoothed_neg_dm / self.__smoothed_tr) * 100
            dx = fabs(pos_di - neg_di) / (pos_di + neg_di) * 100 if (pos_di + neg_di) != 0 else 0
            self.__dx_list.append(dx)

            # ADX Calculation
            if len(self.__dx_list) == self.__period:
                self.__adx = sum(self.__dx_list) / self.__period
            else:
                self.__adx = ((self.__adx * (self.__period - 1)) + dx) / self.__period

    def get_current_value(self) -> float:
        return self.__adx

    def get_return_size(self) -> tuple:
        return (1,)

    def get_description(self) -> str:
        return f"ADX_{self.__period}"

    def get_doc_description(self) -> str:
        return f"ADX over {self.__period} periods."

    def __deepcopy__(self, memo):
        copied_object = self.__class__(self.__period)
        memo[id(self)] = copied_object

        # Explicitly copy each attribute
        copied_object.__true_range = deepcopy(self.__true_range, memo)
        copied_object.__positive_dm = deepcopy(self.__positive_dm, memo)
        copied_object.__negative_dm = deepcopy(self.__negative_dm, memo)
        copied_object.__dx_list = deepcopy(self.__dx_list, memo)
        copied_object.__smoothed_tr = self.__smoothed_tr
        copied_object.__smoothed_pos_dm = self.__smoothed_pos_dm
        copied_object.__smoothed_neg_dm = self.__smoothed_neg_dm
        copied_object.__adx = self.__adx

        return copied_object
