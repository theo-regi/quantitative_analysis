from indicator import Indicator
from quote import Quote

class IndicatorMACD(Indicator):
    def __init__(self, short_period=12, long_period=26, signal_period=9):
        """
        MACD (Movering Average Convergence-Divergence) class initialization.
        MACD shows the relation between a short (short_period) and long (long_period) 
        moving averages (exponential).
        Then, it adds a signal line corresponding to another moving average (signal_period)
        MACD should give indications on a underlying trend and also when the
        trend is reversing. We can apply MACD to multiple time frames.
        """
        super().__init__()
        #Period for MACD calculations (correspond to number of last prices)
        self.__short_period = short_period
        self.__long_period = long_period
        self.__signal_period = signal_period
        #List for prices storage
        self.prices = [] 
        #Storage of MACD values (value of short and long moving average, value of 
        #MACD line (derives from long and short values) and signal line).
        self.__short_ema = None
        self.__long_ema = None
        self.__macd_line = []
        self.__signal_line = None
        self.__histogram = None
        #Description
        self.__doc_description = f"MACD Indicator with short={self.__short_period}, long={self.__long_period}, signal={self.__signal_period}."
        self.__description = f"MACD_{self.__short_period}_{self.__long_period}_{self.__signal_period}"

    def __calculate_macd(self, close_price: float):
        """
        MACD proper calculation:
        """
        if self.__short_ema is None:
            self.__short_ema = close_price
            self.__long_ema = close_price
        else:
            alpha_short = 2 / (self.__short_period + 1)
            alpha_long = 2 / (self.__long_period + 1)
            self.__short_ema = alpha_short * close_price + (1 - alpha_short) * self.__short_ema
            self.__long_ema = alpha_long * close_price + (1 - alpha_long) * self.__long_ema

        macd_line_value = self.__short_ema - self.__long_ema
        self.__macd_line.append(macd_line_value)

        #Resizing macd_line
        if len(self.__macd_line) > self.__signal_period:
            self.__macd_line.pop(0)

        if len(self.__macd_line) >= self.__signal_period:
            self.__signal_line = sum(self.__macd_line) / self.__signal_period
            self.__histogram = macd_line_value - self.__signal_line
        else:
            self.__signal_line = None
            self.__histogram = None

    def incoming_quote(self, quote: Quote) -> None:
        """
        On new quote, we get median price of the book, deriving from best_bid and best_offer
        and we actualize MACD indicator with new value.
        """
        best_bid = self._order_book.get_best_price(True)
        best_offer = self._order_book.get_best_price(False)
        close_price = (best_bid + best_offer) / 2  # Prix médian utilisé comme Close
        self.prices.append(close_price)  # Stocker les prix
        self.__calculate_macd(close_price)

    def get_current_value(self) -> tuple:
        """
        Returns value of the MACD indicator under tuple format (macd_line, signal_line, histogram).
        If not enough data, returns None.
        """
        if self.__signal_line is None or self.__histogram is None:
            return None
        return (
            self.__macd_line[-1],
            #self.__signal_line,    Supression au vu des premiers résultats
            self.__histogram,
        )

    def get_return_size(self) -> tuple:
        return 3,

    def is_ready(self):
        """Check if data are available"""
        return len(self.prices) >= max(self.__short_period, self.__long_period)

    def get_description(self) -> str:
        return self.__description

    def get_doc_description(self) -> str:
        return self.__doc_description

    def __deepcopy__(self, memo):
        return IndicatorMACD(self.__short_period, self.__long_period, self.__signal_period)

