from typing import Dict

from src.core.config import get_settings

settings = get_settings()


class TradingService:
    """Service for executing trades. Stubbed to simulate orders safely."""

    # PUBLIC_INTERFACE
    def place_order(self, provider: str, symbol: str, side: str, quantity: float, market: str = "US") -> Dict:
        """Simulate placing an order with a provider. Returns a mock order receipt."""
        return {
            "provider": provider,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "market": market,
            "status": "simulated",
            "order_id": f"SIM-{abs(hash(provider+symbol+side)) % 10_000_000}",
        }


trading_service = TradingService()
