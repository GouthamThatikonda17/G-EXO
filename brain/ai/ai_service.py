"""
=========================================================
Project G-EXO AI Service
Version : 3.3
Developer : Thatikonda Goutham Teja
=========================================================
"""

import os
from dotenv import load_dotenv
from ai.provider import AIProvider
from ai.exceptions import (
    ProviderError,
    ProviderAuthenticationError,
    ProviderModelNotFoundError,
    ProviderQuotaExceededError
)
from logger import log

load_dotenv()


class AIService(AIProvider):
    """
    Single entry point for all LLM calls in G-EXO.
    Features:
    - Lazy provider initialization (never blocks application startup)
    - Fully configurable provider ordering via AI_PROVIDER_ORDER
    - Standardized exception catching for clean architecture
    - Tracks unavailable providers by name to avoid reference leaks
    - Caches provider instances for the lifetime of this service
    """

    def __init__(self):
        self._providers = []
        self._unavailable_providers = set()
        self._initialized = False

    def _init_providers(self):
        if self._initialized:
            return

        # Lazy imports to prevent startup crashes if dependencies are missing
        from ai.gemini import GeminiProvider
        from ai.openrouter_provider import OpenRouterProvider
        from ai.ollama_provider import OllamaProvider

        provider_map = {
            "gemini": GeminiProvider,
            "openrouter": OpenRouterProvider,
            "ollama": OllamaProvider
        }

        order_env = os.getenv("AI_PROVIDER_ORDER")
        if not order_env:
            # Fallback to DEFAULT_AI_PROVIDER if strict order is absent
            order_env = os.getenv("DEFAULT_AI_PROVIDER")

        if not order_env:
            log("[AIService] Neither AI_PROVIDER_ORDER nor DEFAULT_AI_PROVIDER are configured.", "WARNING")
            self._initialized = True
            return

        # Parse comma-separated list into exact order
        configured_order = [p.strip().lower() for p in order_env.split(",") if p.strip()]

        for name in configured_order:
            if name in provider_map:
                try:
                    # Instantiate once and cache in the instance list
                    provider_instance = provider_map[name]()
                    self._providers.append(provider_instance)
                    log(f"[AIService] Successfully initialized '{name}' provider.")
                except ProviderError as e:
                    log(f"[AIService] Skipped '{name}' provider: {e}", "WARNING")
                except Exception as e:
                    log(f"[AIService] Skipped '{name}' provider unexpectedly: {e}", "WARNING")

        self._initialized = True

    def _handle_provider_error(self, provider_name: str, error: Exception, current_index: int):
        """
        Handles provider errors, marking them unavailable for fatal configuration/auth errors
        and determining the next fallback provider.
        """
        is_fatal = isinstance(error, (
            ProviderAuthenticationError,
            ProviderModelNotFoundError,
            ProviderQuotaExceededError
        ))
        
        # Determine the next available provider for logging purposes
        next_provider_name = None
        for j in range(current_index + 1, len(self._providers)):
            p_name = self._providers[j].__class__.__name__.replace("Provider", "").lower()
            if p_name not in self._unavailable_providers:
                next_provider_name = p_name.capitalize()
                break
        
        if is_fatal:
            self._unavailable_providers.add(provider_name)
            log(f"[AI] {provider_name.capitalize()} unavailable ({str(error)})", "WARNING")
            if next_provider_name:
                log(f"[AI] Falling back to {next_provider_name}", "WARNING")
        else:
            log(f"[AIService] {provider_name.capitalize()} failed: {error}. Falling back to next...", "WARNING")

    # =====================================================
    # CHAT GENERATION
    # =====================================================
    def generate(self, prompt: str) -> str:
        self._init_providers()
        
        last_error = None
        attempted = False

        for i, provider in enumerate(self._providers):
            provider_name = provider.__class__.__name__.replace("Provider", "").lower()
            if provider_name in self._unavailable_providers:
                continue
                
            attempted = True
            try:
                # Execution delegated to the concrete provider
                return provider.generate(prompt)
            except ProviderError as e:
                last_error = e
                self._handle_provider_error(provider_name, e, i)
                continue
            except Exception as e:
                last_error = e
                self._handle_provider_error(provider_name, e, i)
                continue

        if not attempted:
            log("[AIService] Generate failed: No AI providers are configured or available.", "ERROR")
            return "AI Error: All providers are unavailable. Please check your configuration."

        log(f"[AIService] All providers exhausted. Last error: {last_error}", "ERROR")
        return "AI Error: I'm having trouble connecting to my language models right now."

    # =====================================================
    # PLANNER GENERATION
    # =====================================================
    def plan(self, prompt: str) -> str:
        self._init_providers()
        fallback_plan = '{"intent":"chat","tool":null,"action":null,"arguments":{}}'
        
        last_error = None
        attempted = False

        for i, provider in enumerate(self._providers):
            provider_name = provider.__class__.__name__.replace("Provider", "").lower()
            if provider_name in self._unavailable_providers:
                continue
                
            attempted = True
            try:
                # Execution delegated to the concrete provider
                return provider.plan(prompt)
            except ProviderError as e:
                last_error = e
                self._handle_provider_error(provider_name, e, i)
                continue
            except Exception as e:
                last_error = e
                self._handle_provider_error(provider_name, e, i)
                continue

        if not attempted:
            log("[AIService] Plan failed: No AI providers are available.", "ERROR")
            return fallback_plan

        log(f"[AIService] All providers exhausted for planning. Last error: {last_error}", "ERROR")
        return fallback_plan