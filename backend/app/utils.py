import re
from typing import Any, Dict, List, TypedDict


class ValidationResult(TypedDict):
    valid: bool
    errors: List[str]
    cleaned: str


def clean_letters(letters: str) -> str:
    """Clean and validate input letters."""
    if not letters:
        return ""

    # Remove non-alphabetic characters and convert to lowercase
    cleaned = re.sub(r"[^a-zA-Z]", "", letters).lower()
    return cleaned


def validate_letters(letters: str) -> ValidationResult:
    """Validate the input letters and return validation result."""
    result: ValidationResult = {"valid": True, "errors": [], "cleaned": letters}

    if not letters:
        result["valid"] = False
        result["errors"].append("Letters parameter is required")
        return result

    cleaned = clean_letters(letters)

    if not cleaned:
        result["valid"] = False
        result["errors"].append("No valid letters found in input")
        return result

    if len(cleaned) > 20:
        result["valid"] = False
        result["errors"].append("Too many letters (maximum 20 allowed)")
        return result

    result["cleaned"] = cleaned
    return result


def format_response(words: List[str], letters: str) -> Dict[str, Any]:
    """Format the API response."""
    return {
        "success": True,
        "input_letters": letters,
        "word_count": len(words),
        "words": words,
    }


def format_error_response(errors: List[str]) -> Dict[str, Any]:
    """Format an error response."""
    return {"success": False, "errors": errors, "words": []}
