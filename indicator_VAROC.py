
from quote import Quote


import copy
from indicator import Indicator
from collections import deque
import numpy as np


class IndicatorVAROC(Indicator):
    def __init__(self, period: int = 14):
        super().__init__()
        self.__period = period
        self.__prices = deque(maxlen=period)
        self.__varoc = None

    @property
    def period(self):
        return self.__period

    def incoming_quote(self, quote: Quote) -> None:
        """
        Ajoute un nouveau prix extrait de la quote et met à jour l'indicateur VAROC.
        """
        price = quote.get_price()  # Extraction du prix depuis l'objet Quote
        self.__prices.append(price)

        # Attendre d'avoir suffisamment de données pour le calcul
        if len(self.__prices) < self.__period:
            self.__varoc = None  # Pas de calcul possible
            return

        # Calcul du ROC et de la volatilité
        recent_prices = list(self.__prices)
        roc = ((recent_prices[-1] - recent_prices[0]) / recent_prices[0]) * 100
        volatility = np.std(recent_prices)

        # Calcul du VAROC
        self.__varoc = roc / volatility if volatility != 0 else 0

    def get_current_value(self) -> float:
        return self.__varoc

    def get_return_size(self) -> tuple:
        return (1,)

    def get_description(self) -> str:
        return f"VAROC_{self.__period}"

    def get_doc_description(self) -> str:
        return f"Volatility-Adjusted Rate of Change (VAROC) sur {self.__period} périodes."

    def __deepcopy__(self, memo):
        """Permet de créer une copie profonde valide de l'indicateur."""
        copied_obj = self.__class__(self.__period)
        memo[id(self)] = copied_obj
        copied_obj.__prices = copy.deepcopy(self.__prices, memo)
        copied_obj.__varoc = self.__varoc
        return copied_obj
