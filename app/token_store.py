from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken


class TokenStore:
    def __init__(self) -> None:
        self.base_dir = Path.home() / ".insta_analyzer"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.key_file = self.base_dir / "key.bin"
        self.token_file = self.base_dir / "token.enc"

    def _load_or_create_key(self) -> bytes:
        if self.key_file.exists():
            return self.key_file.read_bytes()

        key = Fernet.generate_key()
        self.key_file.write_bytes(key)
        return key

    def save_token(self, access_token: str, ig_user_id: str) -> None:
        key = self._load_or_create_key()
        payload = json.dumps(
            {
                "access_token": access_token,
                "ig_user_id": ig_user_id,
            }
        ).encode("utf-8")
        encrypted = Fernet(key).encrypt(payload)
        self.token_file.write_bytes(encrypted)

    def load_token(self) -> Optional[dict]:
        if not self.token_file.exists():
            return None

        key = self._load_or_create_key()
        encrypted = self.token_file.read_bytes()
        try:
            raw = Fernet(key).decrypt(encrypted)
            return json.loads(raw.decode("utf-8"))
        except (InvalidToken, json.JSONDecodeError):
            return None

    def clear(self) -> None:
        if self.token_file.exists():
            self.token_file.unlink()
