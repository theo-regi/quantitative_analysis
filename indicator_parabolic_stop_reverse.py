from indicator import Indicator
from quote import Quote

class IndicatorSAR(Indicator):
    """
    SAR Indicator is designed to find new trends based on the price dynamic and how fast it changes.
    We record the last x (periods) prices, and look at the extreme points. When an extreme point appears,
    then we look at its amplitude to dynamically adjust the acceleration factor (Alpha/AF).
    """
    def __init__(self, af: float = 0.02, max_AF: float = 0.2, min_AF: float = -0.2, period: int = 100):
        """
        Initialize the SAR indicator.
        :param step: Base multiplier for dynamic AF adjustment.
        :param max_AF: Maximum acceleration factor (AF).
        :param min_AF: Minimum acceleration factor (AF). -> We create a chanel for AF to stay in
        :param period: Number of periods to record for SAR calculation.
        """
        super().__init__()
        self.__af = af #Initial AF
        self.__max_AF = max_AF #Maximum alpha value
        self.__min_AF = min_AF #Minimum alpha value
        self.__period = period
        self.__current_sar = None
        self.__current_trend = None  #"up" or "down"
        self.__extreme_price = None  #Extreme price (EP)
        self.__acceleration_factor = None
        self.__price_history = []  #List to record price history

        #Description
        self.__description = f"SAR_{self.__af}_{self.__max_AF}_{self.__min_AF}_{self.__period}"
        self.__doc_description = (
            f"Parabolic SAR indicator with dynamic acceleration factor based on price movements, "
            f"step {self.__af}, max AF {self.__max_AF}, min AF {self.__min_AF}, and a period of {self.__period}."
        )

    def incoming_quote(self, quote: Quote):
        mid_price = (self._order_book.get_best_price(True) + self._order_book.get_best_price(False)) / 2

        # Record the mid-price and get only the last self.__period prices
        self.__price_history.append(mid_price)
        if len(self.__price_history) > self.__period:
            self.__price_history.pop(0)

        # Initialize SAR and trend
        if self.__current_sar is None:
            self.__current_sar = mid_price
            self.__current_trend = "up"
            self.__extreme_price = mid_price
            self.__acceleration_factor = self.__af
            return

        # Update SAR and trend
        if self.__current_trend == "up":
            # Update SAR
            self.__current_sar += self.__acceleration_factor * (self.__extreme_price - self.__current_sar)

            # Update EP and dynamic AF if new high
            if mid_price > self.__extreme_price:
                old_extreme_price = self.__extreme_price
                self.__extreme_price = mid_price
                self.__acceleration_factor = min(self.__acceleration_factor+(self.__extreme_price - old_extreme_price), self.__max_AF)

            # Check for trend reversal
            if mid_price < self.__current_sar:
                self.__current_trend = "down"
                self.__current_sar = self.__extreme_price
                old_extreme_price = self.__extreme_price
                self.__extreme_price = mid_price
                self.__acceleration_factor = self.__af

        elif self.__current_trend == "down":
            # Update SAR
            self.__current_sar -= self.__acceleration_factor * (self.__current_sar - self.__extreme_price)

            # Update EP and dynamic AF if new low
            if mid_price < self.__extreme_price:
                old_extreme_price = self.__extreme_price
                self.__extreme_price = mid_price
                self.__acceleration_factor = max(self.__acceleration_factor-(old_extreme_price-self.__extreme_price), self.__min_AF)

            # Check for trend reversal
            if mid_price > self.__current_sar:
                self.__current_trend = "up"
                self.__current_sar = self.__extreme_price
                old_extreme_price = self.__extreme_price
                self.__extreme_price = mid_price
                self.__acceleration_factor = self.__af

    def get_current_value(self):
        return self.__current_sar

    def get_return_size(self) -> tuple:
        return (1,)

    def get_description(self) -> str:
        return self.__description

    def get_doc_description(self) -> str:
        return self.__doc_description

    def __deepcopy__(self, memodict={}):
        return IndicatorSAR(self.__af, self.__max_AF, self.__min_AF, self.__period)
