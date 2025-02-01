from indicator import Indicator
from quote import Quote
import numpy as np
from copy import deepcopy

class IndicatorVPVMA(Indicator):
    def __init__(self, fast_period=12, slow_period=26, signal_period=9, bandwidth=0.1):
        super().__init__()
        self.__fast_period = fast_period
        self.__slow_period = slow_period
        self.__signal_period = signal_period
        self.__bandwidth = bandwidth

        # Stockage des prix et volumes
        self.__prices = []
        self.__volumes = []
        self.__vpvma_histogram = []

        #signal
        self.__bandwidthcurrent_signal = "HOLD" # par défaut

        # Historique pour ESVMap et ELVMap
        self.__esvmap_history = []
        self.__elvmap_history = []

        # VPVMA-related values
        self.__svwma = None
        self.__lvwma = None
        self.__dv = None
        self.__esvmap = None
        self.__elvmap = None
        self.__vpvma = None
        self.__signal_line = None

    def calculate_svwma(self, period):
        if len(self.__prices) < period:
            #print(f"Pas assez de données pour SVWMA (period: {period}).")
            return None
        weighted_price_sum = sum([p * v for p, v in zip(self.__prices[-period:], self.__volumes[-period:])])
        volume_sum = sum(self.__volumes[-period:])
        return weighted_price_sum / volume_sum if volume_sum != 0 else None

    def calculate_daily_volatility(self):
        if len(self.__prices) < self.__slow_period:
            #print(f"Pas assez de données pour calculer la volatilité (period: {self.slow_period}).")
            return None
        return np.std(self.__prices[-self.__slow_period:])

    def calculate_ema(self, values, period):
        if len(values) < period:
            #print(f"Pas assez de données pour EMA (period: {period}, values: {len(values)}).")
            return None
        alpha = 2 / (period + 1)
        ema = values[0]
        for value in values[1:]:
            ema = alpha * value + (1 - alpha) * ema
        return ema

    def calculate_signals(self):
        """
        Calcule les signaux de trading basés sur les valeurs actuelles de VPVMA et de la ligne de signal.
        """
        # Vérifiez que toutes les données nécessaires sont disponibles
        if self.__vpvma is None or self.__signal_line is None or len(self.__vpvma_histogram) < self.__signal_period:
            #print(f"Not enough data for signals. VPVMA: {self.vpvma}, Signal Line: {self.signal_line}")
            self.__current_signal = "HOLD"
            return self.__current_signal

        # Vérification du croisement entre VPVMA et la ligne de signal
        if self.__vpvma > self.__signal_line:
            self.__current_signal = "BUY"
        elif self.__vpvma < self.__signal_line:
            self.__current_signal = "SELL"
        else:
            self.__current_signal = "HOLD"

        return self.__current_signal

    def incoming_quote(self, quote: Quote) -> None:
        # Récupération des prix bid et offer, calcul du prix moyen et du volume
        best_bid = self._order_book.get_best_price(True)
        best_offer = self._order_book.get_best_price(False)
        close_price = (best_bid + best_offer) / 2
        volume = quote.get_amount()

        # Ajout des données
        self.__prices.append(close_price)
        self.__volumes.append(volume)

        # Limiter les listes aux périodes nécessaires
        max_period = max(self.__fast_period, self.__slow_period, self.__signal_period)
        if len(self.__prices) > max_period:
            self.__prices.pop(0)
            self.__volumes.pop(0)

        # Calcul SVWMA et LVWMA
        self.__svwma = self.calculate_svwma(self.__fast_period) if len(self.__prices) >= self.__fast_period else None
        self.__lvwma = self.calculate_svwma(self.__slow_period) if len(self.__prices) >= self.__slow_period else None

        # Calcul de la volatilité quotidienne
        self.__dv = self.calculate_daily_volatility() if len(self.__prices) >= self.__slow_period else None

        # Calcul ESVMap et ELVMap
        if self.__svwma and self.__lvwma and self.__dv:
            self.__esvmap_history.append(self.__svwma * self.__dv)
            self.__elvmap_history.append(self.__lvwma * self.__dv)

            if len(self.__esvmap_history) >= self.__fast_period:
                self.__esvmap = self.calculate_ema(self.__esvmap_history, self.__fast_period)

            if len(self.__elvmap_history) >= self.__slow_period:
                self.__elvmap = self.calculate_ema(self.__elvmap_history, self.__slow_period)

            # Calcul VPVMA et signal_line
            if self.__esvmap is not None and self.__elvmap is not None:
                self.__vpvma = self.__esvmap - self.__elvmap
                self.__vpvma_histogram.append(self.__vpvma)

                if len(self.__vpvma_histogram) >= self.__signal_period:
                    self.__signal_line = np.mean(self.__vpvma_histogram[-self.__signal_period:])

        # Mise à jour du signal
        #self.calculate_signals()

    def get_current_value(self) -> tuple:
        """Retourne les valeurs actuelles du VPVMA et de la ligne de signal."""
        return self.__vpvma, self.__signal_line

    def is_ready(self) -> bool:
        """Vérifie si l'indicateur est prêt à être utilisé."""
        return (
            len(self.__prices) >= max(self.__fast_period, self.__slow_period, self.__signal_period) and
            self.__svwma is not None and
            self.__lvwma is not None and
            self.__dv is not None
        )

    def get_signal(self) -> str:
        """
        Retourne le signal actuel (BUY, SELL, HOLD).
        """
        if not hasattr(self, "current_signal"):
            self.__current_signal = "HOLD"
        return self.__current_signal

    def get_description(self) -> str:
        """Retourne une description textuelle de l'indicateur."""
        return "Volume Price-Weighted Moving Average Indicator"

    def get_doc_description(self) -> str:
        """Retourne une description technique/documentaire de l'indicateur."""
        return "Indicator that calculates VPVMA based on volume and price movements."

    def get_return_size(self):
        """Retourne la taille du retour (deux valeurs : VPVMA et ligne de signal)."""
        return (2,)

    def __deepcopy__(self, memo):
        """Gestion de la copie profonde de l'objet."""
        copied = self.__class__(
            fast_period=self.__fast_period,
            slow_period=self.__slow_period,
            signal_period=self.__signal_period,
            bandwidth=self.__bandwidth
        )
        copied.__prices = deepcopy(self.__prices, memo)
        copied.__volumes = deepcopy(self.__volumes, memo)
        return copied
