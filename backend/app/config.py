import os
from enum import Enum
from typing import Dict


class DictionaryType(Enum):
    """Available dictionary types"""

    GOOGLE_10K = "google_10k"
    SCOWL_MEDIUM = (
        "scowl_medium"  # 58k words - high quality, includes common words like "ache"
    )
    SCOWL_LARGE = "scowl_large"  # 126k words - comprehensive but curated
    COMPREHENSIVE = "comprehensive"
    AUTO = "auto"  # Try SCOWL Medium first, then others


class Config:
    """Application configuration"""

    # Dictionary configuration
    DICTIONARY_TYPE = DictionaryType(os.getenv("WORDMIXR_DICTIONARY", "scowl_large"))

    # Dictionary file mappings
    DICTIONARY_FILES: Dict[DictionaryType, list] = {
        DictionaryType.GOOGLE_10K: [
            "google-10000-english.txt",
            "/app/google-10000-english.txt",
            "app/google-10000-english.txt",
        ],
        DictionaryType.SCOWL_MEDIUM: [
            "scowl-medium.txt",
            "/app/scowl-medium.txt",
            "app/scowl-medium.txt",
        ],
        DictionaryType.SCOWL_LARGE: [
            "scowl-large.txt",
            "/app/scowl-large.txt",
            "app/scowl-large.txt",
        ],
        DictionaryType.COMPREHENSIVE: [
            "words_alpha.txt",
            "/app/words_alpha.txt",
            "app/words_alpha.txt",
        ],
        DictionaryType.AUTO: [],  # Will use multiple in priority order
    }

    @classmethod
    def get_dictionary_paths(cls) -> list:
        """Get dictionary file paths in priority order"""
        if cls.DICTIONARY_TYPE == DictionaryType.AUTO:
            # Try SCOWL Large first (best for games), then Medium, then Google 10k, then comprehensive
            return (
                cls.DICTIONARY_FILES[DictionaryType.SCOWL_LARGE]
                + cls.DICTIONARY_FILES[DictionaryType.SCOWL_MEDIUM]
                + cls.DICTIONARY_FILES[DictionaryType.GOOGLE_10K]
                + cls.DICTIONARY_FILES[DictionaryType.COMPREHENSIVE]
            )
        else:
            return cls.DICTIONARY_FILES[cls.DICTIONARY_TYPE]

    @classmethod
    def get_dictionary_info(cls) -> dict:
        """Get information about current dictionary configuration"""
        return {
            "type": cls.DICTIONARY_TYPE.value,
            "description": cls._get_dictionary_description(cls.DICTIONARY_TYPE),
        }

    @classmethod
    def _get_dictionary_description(cls, dict_type: DictionaryType) -> str:
        """Get human-readable description of dictionary type"""
        descriptions = {
            DictionaryType.GOOGLE_10K: "Google 10,000 most common English words (high quality but limited coverage)",
            DictionaryType.SCOWL_MEDIUM: "SCOWL Medium: 58k curated words (good quality but missing some words like 'gird')",
            DictionaryType.SCOWL_LARGE: "SCOWL Large: 126k curated words (perfect for word games, includes 'ache' and 'gird')",
            DictionaryType.COMPREHENSIVE: "Comprehensive English dictionary (370k+ words, includes obscure terms)",
            DictionaryType.AUTO: "Auto-select: SCOWL Large preferred, with intelligent fallbacks",
        }
        return descriptions.get(dict_type, "Unknown dictionary type")
