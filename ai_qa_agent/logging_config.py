"""Structured logging configuration."""

from __future__ import annotations

import logging
import sys
from collections.abc import Callable
from typing import Any

import structlog

Processor = Callable[[Any, str, Any], Any]


def configure_logging(log_level: str = "INFO", json_logs: bool = False) -> None:
    """Configure structured logging for the application."""
    processors: list[Processor] = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if json_logs:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level)),
        cache_logger_on_first_use=True,
    )

    # Keep third-party libraries on standard logging with a simple formatter
    # to avoid conflicts with structlog's bound logger expectations.
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level))
