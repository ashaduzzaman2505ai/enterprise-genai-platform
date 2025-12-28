from typing import Optional


class TokenCounter:
    """Count tokens for a given text using tiktoken when available.

    Falls back to a simple word-based token count if `tiktoken` is not
    installed or the requested model encoding is not available.
    """

    def __init__(self, model_name: str = "gpt-4") -> None:
        self.model_name = model_name
        self._encoder = None

        try:
            import tiktoken

            self._tiktoken = tiktoken
        except Exception:
            self._tiktoken = None

    def _ensure_encoder(self):
        if self._encoder is None and self._tiktoken:
            try:
                self._encoder = self._tiktoken.encoding_for_model(self.model_name)
            except Exception:
                # model not found; fallback to a base encoding
                try:
                    self._encoder = self._tiktoken.get_encoding("cl100k_base")
                except Exception:
                    self._encoder = None

    def count(self, text: str) -> int:
        self._ensure_encoder()
        if self._encoder:
            return len(self._encoder.encode(text))

        # Fallback: simple heuristic (words)
        return max(0, len(text.split()))
