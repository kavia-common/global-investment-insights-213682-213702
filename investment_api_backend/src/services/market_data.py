from typing import Dict

from src.core.config import get_settings

settings = get_settings()


class MarketDataService:
    """Service providing market data. Stubbed with safe mock values."""

    # PUBLIC_INTERFACE
    def get_quote(self, symbol: str, market: str = "US") -> Dict[str, float]:
        """Return a mock quote for a symbol. Replace with real integration later."""
        # Mock behavior: deterministic pseudo price based on symbol hash
        price = float(abs(hash(symbol + market)) % 10000) / 100.0 + 10.0
        return {"symbol": symbol, "price": round(price, 2)}


market_data_service = MarketDataService()
