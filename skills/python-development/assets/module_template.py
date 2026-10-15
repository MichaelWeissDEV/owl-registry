"""Example canonical Python module demonstrating modern idiomatic practices."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Protocol

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT: Final[float] = 30.0


class ServiceError(Exception):
    """Base exception for service failures."""


class DataStore(Protocol):
    """Abstract interface for persistent storage."""

    def get(self, key: str) -> bytes | None:
        """Retrieve stored bytes by key."""
        ...

    def put(self, key: str, value: bytes) -> None:
        """Persist bytes under key."""
        ...


@dataclass(slots=True, frozen=True)
class ServiceConfig:
    """Immutable service configuration."""

    base_dir: Path
    timeout: float = DEFAULT_TIMEOUT
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.timeout <= 0:
            raise ValueError(f"Timeout must be positive, got {self.timeout}")


class CacheManager:
    """Manages cache lifecycle with explicit storage backend injection."""

    def __init__(self, store: DataStore, config: ServiceConfig) -> None:
        self._store = store
        self._config = config

    def retrieve(self, key: str) -> bytes | None:
        """Fetch payload from store with error boundary."""
        try:
            return self._store.get(key)
        except Exception as exc:
            logger.error("Failed to fetch key %s: %s", key, exc)
            raise ServiceError(f"Error reading {key}") from exc
