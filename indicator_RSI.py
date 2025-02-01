from indicator import Indicator
from quote import Quote


class IndicatorRSI(Indicator):
    def __init__(self, period: int = 14):
        self.__doc_description = f"Relative Strength Index (RSI) over {period} periods."
        self.__description = f"RSI_{period}"
        self.__period = period
        self.__gains = []
        self.__losses = []
        self.prices = []  # Ajouter une liste pour stocker les prix
        self._previous_price = None

    def incoming_quote(self, quote: Quote) -> None:
        current_price = quote.get_price()
        self.prices.append(current_price)  # Stocker les prix

        # S'assurer qu'on a un prix précédent pour calculer les variations
        if self._previous_price is not None:
            change = current_price - self._previous_price
            gain = max(change, 0)
            loss = abs(min(change, 0))

            if hasattr(self, '_avg_gain') and hasattr(self, '_avg_loss'):
                # Mise à jour des moyennes pondérées après la première période
                self._avg_gain = (self._avg_gain * (self.__period - 1) + gain) / self.__period
                self._avg_loss = (self._avg_loss * (self.__period - 1) + loss) / self.__period
            else:
                # Initialisation des moyennes lors des premières périodes
                self.__gains.append(gain)
                self.__losses.append(loss)

                if len(self.__gains) == self.__period:
                    self._avg_gain = sum(self.__gains) / self.__period
                    self._avg_loss = sum(self.__losses) / self.__period

            # Limiter la taille des gains et pertes à la période définie
            if len(self.__gains) > self.__period:
                self.__gains.pop(0)
            if len(self.__losses) > self.__period:
                self.__losses.pop(0)

        self._previous_price = current_price

    def get_current_value(self) -> float:
        # Vérifie qu'on a suffisamment de données pour calculer le RSI
        if not hasattr(self, '_avg_gain') or not hasattr(self, '_avg_loss'):
            return 50.0  # Retourne RSI neutre

        avg_gain = self._avg_gain
        avg_loss = self._avg_loss

        if avg_loss == 0:
            return 100.0  # Si aucune perte, RSI est maximal

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def get_return_size(self) -> tuple:
        return 1,

    def is_ready(self):
        return len(self.prices) >= self.__period

    def get_description(self) -> str:
        return self.__description

    def get_doc_description(self) -> str:
        return self.__doc_description

    def __deepcopy__(self, memodict={}):
        return IndicatorRSI(self.__period)
