from __future__ import annotations

from app.services.storage import StorageManager


def cleanup_old_files():
    """Cleanup function to be called periodically."""
    storage = StorageManager()
    storage.cleanup_old_files()

