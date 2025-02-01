from typing import List
from indicator import Indicator
from indicator_best_bid_offer_variance import IndicatorBestBidOfferVariance
from indicator_moving_average_on_price import IndicatorMovingAverageOnPrice
from indicator_moving_average_on_amount import IndicatorMovingAverageOnAmount
from indicator_quantity_of_quotes_in_book import IndicatorQuantityOfQuotesInBook
from indicator_MACD import IndicatorMACD
from indicator_RSI import IndicatorRSI
from indicator_bollinger_bands import IndicatorBollingerBands
from indicator_MACD import IndicatorMACD
from indicator_RSI import IndicatorRSI
from indicator_parabolic_stop_reverse import IndicatorSAR
from indicator_money_flow_index import IndicatorMoneyFlowIndex
from indicator_VPVMA import IndicatorVPVMA

# Chosen set of indicators
INDICATORS: tuple = (
                        IndicatorMACD(24, 52, 18),
                        IndicatorMACD(12, 26, 9),
                        IndicatorMoneyFlowIndex(14),
                        IndicatorMoneyFlowIndex(28),
                        IndicatorMovingAverageOnAmount(9),
                        IndicatorBollingerBands(9, 1, 9, 18),
                        IndicatorBollingerBands(20, 2, 10, 50),
                        IndicatorVPVMA(12,26,9,0.1),
                    )
