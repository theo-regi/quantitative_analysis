from indicator import Indicator
from quote import Quote

class IndicatorBollingerBands(Indicator):
    """
    Bollinger Bands indicator: calculated around a Simple Moving Average of the price over the last
    x periods (input). We substract or add a number of time (multiplier) the standard deviation.
    The research paper highlight the usage of a long and a short bollinger band width to determine
    signals, the problem for us is that it influences the result. We will only pass the values of
    these short and long SMA alongside the BB values. 
    """

    def __init__(self, periods: int = 20, multiplier: float = 2.0, bbw_short: int = 10, bbw_long: int = 50) -> None:
        """
        Initialize the Bollinger Bands indicator with BBW calculations.
        :param periods: Number of periods for the moving average.
        :param multiplier: Standard deviation multiplier.
        """
        super().__init__()
        self.__periods = periods
        self.__multiplier = multiplier
        self.__bbw_short = bbw_short
        self.__bbw_long = bbw_long
        self.__prices = []
        self.__bbws = []
        #self.__current_bands = (None, None, None, None, None, None)  # (lower_band, moving_average, upper_band, bb width, short SMA, long SMA)
        self.__current_bands = (None, None, None, None) #Need to change definition after first tests, the unittest where for before first changes.
        #Description
        self.__doc_description = (
            f"Bollinger Bands with {self.__periods} periods and multiplier {self.__multiplier}. "
            f"BBW with short SMA ({self.__bbw_short}) and long SMA ({self.__bbw_long})."
        )
        self.__description = f"BOLL_{self.__periods}_{self.__multiplier}_BBW_{self.__bbw_short}_{self.__bbw_long}"
    
    def incoming_quote(self, quote: Quote) -> None:
        # Use the mid-price for the Bollinger Bands calculation
        mid_price = (self._order_book.get_best_price(True) + self._order_book.get_best_price(False)) / 2
        self.__prices.append(mid_price)

        # Keep only the latest `periods` prices
        if len(self.__prices) > self.__periods:
            self.__prices.pop(0)

        # Calculate Bollinger Bands when enough data is available
        if len(self.__prices) == self.__periods:
            moving_average = sum(self.__prices) / self.__periods
            variance = sum((price - moving_average) ** 2 for price in self.__prices) / self.__periods
            std_dev = variance ** 0.5
            lower_band = moving_average - self.__multiplier * std_dev
            upper_band = moving_average + self.__multiplier * std_dev

            # Calculate BBW
            bbw = (upper_band - lower_band) / moving_average
            self.__bbws.append(bbw)

            # Keep only the latest `bbw_long` BBW values for SMA calculation
            if len(self.__bbws) > self.__bbw_long:
                self.__bbws.pop(0)
            
            short_sma = sum(self.__bbws[-self.__bbw_short:]) / self.__bbw_short
            long_sma = sum(self.__bbws[-self.__bbw_long:]) / self.__bbw_long
            """Version de base des bandes de bollinger, non utilisée après les premiers tests
            self.__current_bands = (lower_band,        
                                    moving_average, 
                                    upper_band,        
                                    bbw, 
                                    short_sma, 
                                    long_sma)"""

            self.__current_bands = (moving_average, 
                                    bbw, 
                                    short_sma, 
                                    long_sma)

    def get_current_value(self):
        return self.__current_bands

    def get_return_size(self) -> tuple:
        return (4,)

    def get_description(self) -> str:
        return self.__description

    def get_doc_description(self) -> str:
        return self.__doc_description

    def __deepcopy__(self, memodict={}):
        return  IndicatorBollingerBands(self.__periods, self.__multiplier, self.__bbw_short, self.__bbw_long)
