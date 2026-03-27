"""Configuration settings for imbox.

Handles both hardcoded values and environment variables.
"""

import os
from dataclasses import dataclass
from enum import Enum


def str_to_bool(value: str) -> bool:
    """Convert string to boolean."""
    return value.lower() in ("true", "1", "yes")


@dataclass
class Config:
    username: str
    password: str
    imap_url: str
    ssl: bool
    ssl_context: str
    starttls: bool
    port: int = 993


class LogOutputType(Enum):
    clean = "clean"
    default = "default"


class Settings:
    """Configuration settings for imbox."""

    @property
    def imbox_imap_url(self) -> str:
        """Default IMAP server URL."""
        return os.getenv("IMBOX_IMAP_URL", "imap.gmail.com")

    @property
    def imbox_username(self) -> str:
        """IMAP username/email address."""
        return os.getenv("IMBOX_USERNAME", "username")

    @property
    def imbox_password(self) -> str:
        """IMAP password or app-specific password."""
        return os.getenv("IMBOX_PASSWORD", "")

    @property
    def imbox_ssl(self) -> bool:
        """Enable SSL for IMAP connection."""
        return str_to_bool(os.getenv("IMBOX_SSL", "true"))

    @property
    def imbox_ssl_context(self) -> str:
        """SSL context for IMAP connection."""
        return os.getenv("IMBOX_SSL_CONTEXT", "None")

    @property
    def imbox_starttls(self) -> bool:
        """Enable STARTTLS for IMAP connection."""
        return str_to_bool(os.getenv("IMBOX_STARTTLS", "false"))

    @property
    def imbox_port(self) -> int:
        """IMAP port."""
        return int(os.getenv("IMBOX_PORT", 993))

    # Output
    @property
    def output_folder(self) -> str:
        """Output folder for downloaded messages."""
        return os.getenv("OUTPUT_FOLDER", "output")

    @property
    def output(self) -> bool:
        """Enable output."""
        return str_to_bool(os.getenv("OUTPUT", "false"))

    @property
    def output_filename(self) -> str:
        """Filename for output."""
        return os.getenv("OUTPUT_FILENAME", "imbox_results.json")

    @property
    def output_fields(self) -> list[str]:
        """Fields to include in output. Returns empty list if not configured."""
        fields_str = os.getenv("OUTPUT_FIELDS", "").strip()
        if not fields_str:
            return []
        return [field.strip() for field in fields_str.split(",") if field.strip()]

    # Environment-based settings
    @property
    def debug(self) -> bool:
        """Enable debug mode."""
        return str_to_bool(os.getenv("DEBUG", "false"))

    @property
    def log_output_type(self) -> LogOutputType:
        """How much information to output to the console."""
        value = os.getenv("LOG_OUTPUT_TYPE", "default")
        return LogOutputType(value)

    @property
    def log_level(self) -> str:
        """Logging level."""
        return os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def config(self) -> Config:
        """Return configuration object."""
        return Config(
            username=self.imbox_username,
            password=self.imbox_password,
            imap_url=self.imbox_imap_url,
            ssl=self.imbox_ssl,
            ssl_context=self.imbox_ssl_context,
            starttls=self.imbox_starttls,
            port=self.imbox_port,
        )


settings = Settings()
