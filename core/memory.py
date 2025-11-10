# core/memory.py
"""
Memory Management Module

Purpose:
- Initializes and configures the application's persistent memory database.
- Provides a unified interface for session and memory storage used by agents.
- Currently implemented with SQLite for simplicity, but easily extendable
  to other backends (e.g., PostgreSQL).

Usage:
    from core.memory import build_db
    db = build_db()
"""

from agno.db.sqlite import SqliteDb
from core.config import get_settings


def build_db() -> SqliteDb:
    """
    Build and return a persistent SQLite database instance.

    Behavior:
        - Reads the database connection URL from application settings.
        - Supports URLs of the form: "sqlite:///./file_name.db".
        - Defaults to "agno_memory.db" if the URL is not SQLite-based.
        - The resulting database is used to persist agent sessions and user memories.

    Returns:
        SqliteDb: Configured database instance connected to the target file.
    """
    settings = get_settings()

    # Detect and extract file path from SQLite connection URL
    if settings.AGNO_DB_URL.startswith("sqlite:///"):
        # Example: "sqlite:///./agno_memory.db" → "./agno_memory.db"
        db_file = settings.AGNO_DB_URL.replace("sqlite:///", "")
    else:
        # Fallback for unsupported URLs or missing config
        db_file = "agno_memory.db"

    return SqliteDb(db_file=db_file)
