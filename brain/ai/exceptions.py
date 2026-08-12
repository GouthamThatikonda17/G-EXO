"""
=========================================================
Project G-EXO AI Provider Exceptions
Version : 1.1
Developer : Thatikonda Goutham Teja
=========================================================
"""

class ProviderError(Exception):
    """Base exception for all AI provider errors."""
    pass

class ProviderAuthenticationError(ProviderError):
    """Raised when an API key is missing, invalid, or unauthorized."""
    pass

class ProviderQuotaExceededError(ProviderError):
    """Raised when an API rate limit or quota is exhausted."""
    pass

class ProviderModelNotFoundError(ProviderError):
    """Raised when the requested model does not exist or is unavailable."""
    pass

class ProviderNetworkError(ProviderError):
    """Raised when a network timeout or connection failure occurs."""
    pass

class PlannerError(Exception):
    """Raised when the AI Planner fails to generate or extract a valid execution plan."""
    pass
