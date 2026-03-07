"""
AI model interface layer for PSAE.
"""

from __future__ import annotations

import json
import os
import re
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional


class AIModelInterface(ABC):
    """Abstract interface for all model wrappers."""

    name: str
    version: str

    def __init__(
        self,
        name: str,
        version: str = "unknown",
        rate_limit_seconds: float = 0.0,
        retry_attempts: int = 3,
        retry_backoff_seconds: float = 1.0,
    ) -> None:
        self.name = name
        self.version = version
        self.rate_limit_seconds = rate_limit_seconds
        self.retry_attempts = max(1, retry_attempts)
        self.retry_backoff_seconds = max(0.0, retry_backoff_seconds)
        self._last_query_at = 0.0

    def _apply_rate_limit(self) -> None:
        if self.rate_limit_seconds <= 0:
            return

        elapsed = time.time() - self._last_query_at
        if elapsed < self.rate_limit_seconds:
            time.sleep(self.rate_limit_seconds - elapsed)

    def _mark_query(self) -> None:
        self._last_query_at = time.time()

    @abstractmethod
    def query(self, prompt: str) -> str:
        """Run one prompt and return model text output."""

    def batch_query(self, prompts: List[str]) -> List[str]:
        """Sequential batch execution with shared retry/rate-limit behavior."""
        return [self.query(prompt) for prompt in prompts]


class OpenAIWrapper(AIModelInterface):
    """OpenAI chat-completions wrapper."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.1,
        timeout: int = 60,
        max_tokens: int = 4096,
        rate_limit_seconds: float = 0.0,
        retry_attempts: int = 3,
    ) -> None:
        super().__init__(
            name="openai",
            version=model,
            rate_limit_seconds=rate_limit_seconds,
            retry_attempts=retry_attempts,
        )
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def query(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Missing OPENAI_API_KEY for OpenAIWrapper.")

        self._apply_rate_limit()
        last_error: Optional[Exception] = None

        for attempt in range(1, self.retry_attempts + 1):
            try:
                from openai import OpenAI

                client = OpenAI(api_key=self.api_key, timeout=self.timeout)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                self._mark_query()
                return response.choices[0].message.content or ""
            except Exception as exc:
                last_error = exc
                if attempt < self.retry_attempts:
                    time.sleep(self.retry_backoff_seconds * attempt)

        raise RuntimeError(f"OpenAI query failed after retries: {last_error}")


class AnthropicWrapper(AIModelInterface):
    """Anthropic messages API wrapper."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.1,
        timeout: int = 60,
        max_tokens: int = 4096,
        rate_limit_seconds: float = 0.0,
        retry_attempts: int = 3,
    ) -> None:
        super().__init__(
            name="anthropic",
            version=model,
            rate_limit_seconds=rate_limit_seconds,
            retry_attempts=retry_attempts,
        )
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

    def query(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Missing ANTHROPIC_API_KEY for AnthropicWrapper.")

        self._apply_rate_limit()
        last_error: Optional[Exception] = None

        for attempt in range(1, self.retry_attempts + 1):
            try:
                import anthropic

                client = anthropic.Anthropic(api_key=self.api_key, timeout=self.timeout)
                response = client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}],
                )
                self._mark_query()
                return "".join(
                    block.text for block in response.content if getattr(block, "text", None)
                )
            except Exception as exc:
                last_error = exc
                if attempt < self.retry_attempts:
                    time.sleep(self.retry_backoff_seconds * attempt)

        raise RuntimeError(f"Anthropic query failed after retries: {last_error}")


class GeminiWrapper(AIModelInterface):
    """Google Gemini wrapper."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-1.5-pro",
        temperature: float = 0.1,
        timeout: int = 60,
        max_tokens: int = 4096,
        rate_limit_seconds: float = 0.0,
        retry_attempts: int = 3,
    ) -> None:
        super().__init__(
            name="google",
            version=model,
            rate_limit_seconds=rate_limit_seconds,
            retry_attempts=retry_attempts,
        )
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

    def query(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("Missing GOOGLE_API_KEY for GeminiWrapper.")

        self._apply_rate_limit()
        last_error: Optional[Exception] = None

        for attempt in range(1, self.retry_attempts + 1):
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.api_key)
                generation_config = {
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                }
                model = genai.GenerativeModel(
                    model_name=self.model,
                    generation_config=generation_config,
                )
                response = model.generate_content(prompt)
                self._mark_query()
                return getattr(response, "text", "") or ""
            except Exception as exc:
                last_error = exc
                if attempt < self.retry_attempts:
                    time.sleep(self.retry_backoff_seconds * attempt)

        raise RuntimeError(f"Gemini query failed after retries: {last_error}")


class HumanExpertBaseline(AIModelInterface):
    """
    Human baseline that returns pre-scored responses from JSON.

    Supported JSON formats:
    1) {"responses": [{"test_id": "...", "response": "..."}]}
    2) [{"test_id": "...", "response": "..."}]
    """

    def __init__(
        self,
        responses_path: str,
        default_response: str = "No human baseline response found for this prompt.",
    ) -> None:
        super().__init__(name="human_expert", version="baseline")
        self.responses_path = Path(responses_path)
        self.default_response = default_response
        self._responses_by_test_id = self._load_responses()

    def _load_responses(self) -> Dict[str, str]:
        if not self.responses_path.exists():
            raise FileNotFoundError(f"Human baseline file not found: {self.responses_path}")

        with open(self.responses_path, "r", encoding="utf-8") as handle:
            data: Any = json.load(handle)

        entries: List[Dict[str, Any]]
        if isinstance(data, dict) and "responses" in data:
            entries = data["responses"]
        elif isinstance(data, list):
            entries = data
        else:
            raise ValueError("Invalid human baseline JSON format.")

        output: Dict[str, str] = {}
        for item in entries:
            test_id = str(item.get("test_id", "")).strip()
            response = str(item.get("response", "")).strip()
            if test_id and response:
                output[test_id] = response

        return output

    def get_response_by_test_id(self, test_id: str) -> str:
        return self._responses_by_test_id.get(test_id, self.default_response)

    def query(self, prompt: str) -> str:
        # Try to identify IDs such as SC-001, EN-002, IN-003, RE-004 in prompt text.
        match = re.search(r"\b[A-Z]{2}-\d{3}\b", prompt)
        if not match:
            return self.default_response
        return self.get_response_by_test_id(match.group(0))
