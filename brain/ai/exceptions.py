"""
=========================================================
Project G-EXO AI Provider Exceptions
Version : 1.0
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