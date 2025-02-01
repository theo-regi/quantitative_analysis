from indicator import Indicator
from quote import Quote


class IndicatorMoneyFlowIndex(Indicator):
    """
    Money Flow Index (MFI) indicator is design to find momentum situations using prices and volumes.
    The original version of this indicator (and in the paper) is functionning with executed_volume.
    However, we don't have these data from the market, and get_executed_quote_for_volume in the orderbook
    is not designed for that.
    Therefore, we need to track the volumes and prices in the book, and retaylor the indicator to estimate
    these data. At the end, our result is that it tracks all lasts x (periods) volumes entering
    and getting out the book.
    """
    def __init__(self, periods: int = 14):
        """
        Initialize the Money Flow Index indicator with volume variation.
        :param periods: Number of periods for MFI calculation.
        """
        super().__init__()
        self.__periods = periods
        self.__prices = []  # Mid-prices for the period
        self.__volumes = []  # Total volumes (bid + ask) for the period
        self.__volume_variations = []  # Volume variations over the period
        self.__money_flows = []  # Stores raw money flows for MFI calculation
        self.__current_mfi = None

        #Decription
        self.__description = "MFI_{}".format(self.__periods)
        self.__doc_description = (
            "Money Flow Index (MFI) with {} periods, based on volume variation and price movements over the period.".format(self.__periods)
        )


    def incoming_quote(self, quote: Quote):
        if self._order_book.get_current_snapshot(True) and self._order_book.get_current_snapshot(False):
            # Calculate the mid-price
            mid_price =  (self._order_book.get_best_price(True) + self._order_book.get_best_price(False))/ 2

            # Calculate the total volume in the order book
            total_volume = self._order_book.get_best_quote(True).get_amount() + self._order_book.get_best_quote(False).get_amount()

            # Append mid-price and total volume to storage
            self.__prices.append(mid_price)
            self.__volumes.append(total_volume)

            # Keep only the last `periods` values
            if len(self.__prices) > self.__periods:
                self.__prices.pop(0)
                self.__volumes.pop(0)

            # Calculate volume variation if we have enough data
            if len(self.__volumes) == self.__periods:
                volume_variation = abs(self.__volumes[-1] - self.__volumes[0])
                self.__volume_variations.append(volume_variation)

                # Keep only the last `periods` volume variations
                if len(self.__volume_variations) > self.__periods:
                    self.__volume_variations.pop(0)

                # Calculate raw money flow based on mid-price and volume variation
                raw_money_flow = ((max(self.__prices) + min(self.__prices) + self.__prices[-1])/3) * sum(self.__volume_variations)
                self.__money_flows.append(raw_money_flow)

                # Keep only the last `periods` money flows
                if len(self.__money_flows) > self.__periods:
                    self.__money_flows.pop(0)

                # Calculate the Money Flow Index if we have enough data
                if len(self.__money_flows) == self.__periods:
                    positive_money_flow = sum(
                        flow for i, flow in enumerate(self.__money_flows)
                        if self.__volume_variations[i] -  self.__volume_variations[i-1]> 0
                    )
                    negative_money_flow = sum(
                        flow for i, flow in enumerate(self.__money_flows)
                        if self.__volume_variations[i] -  self.__volume_variations[i-1] < 0
                    )

                    # Avoid division by zero
                    if negative_money_flow == 0:
                        self.current_mfi = 100.0
                    else:
                        money_flow_ratio = positive_money_flow / negative_money_flow
                        self.current_mfi = 100.0 - (100.0 / (1 + money_flow_ratio))

    def get_current_value(self):
        return self.current_mfi

    def get_return_size(self) -> tuple:
        return (1,)

    def get_description(self) -> str:
        return self.__description

    def get_doc_description(self) -> str:
        return self.__doc_description

    def __deepcopy__(self, memodict={}):
        return IndicatorMoneyFlowIndex(self.__periods)
