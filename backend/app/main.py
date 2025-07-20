import logging
from contextlib import asynccontextmanager

from config import Config
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from solver import find_valid_words, get_anagrams, load_dictionary
from utils import format_error_response, format_response, validate_letters

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global dictionary and metadata - loaded at startup
DICTIONARY = None
DICTIONARY_INFO = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the dictionary when the app starts."""
    global DICTIONARY, DICTIONARY_INFO
    logger.info("Loading word dictionary...")
    logger.info(
        f"Dictionary configuration: {Config.get_dictionary_info()['description']}"
    )

    # Load dictionary using configuration system
    try:
        DICTIONARY, DICTIONARY_INFO = load_dictionary()
        logger.info(f"Successfully loaded {DICTIONARY_INFO['type']} dictionary")
        logger.info(
            f"Dictionary: {DICTIONARY_INFO['filepath']} ({DICTIONARY_INFO['size']} words)"
        )
    except Exception as e:
        logger.error(f"Failed to load dictionary: {e}")
        DICTIONARY = set()
        DICTIONARY_INFO = {
            "filepath": "none",
            "size": 0,
            "type": "error",
            "config": {"type": "unknown", "description": "Failed to load"},
        }

    yield

    # Cleanup (if needed)
    DICTIONARY = None
    DICTIONARY_INFO = None


# Initialize FastAPI app
app = FastAPI(
    title="WordMixr API",
    description="A word puzzle solver API that finds valid words from scrambled letters",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],  # Add Vite dev server port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Remove the old startup event since we're using lifespan now
async def _unused_startup_placeholder():
    """Placeholder for removed startup event."""
    pass


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to WordMixr API",
        "version": "1.0.0",
        "endpoints": {
            "/solve": "GET - Solve word puzzles with scrambled letters",
            "/anagrams": "GET - Find anagrams using all letters exactly once",
        },
    }


@app.get("/solve")
async def solve_puzzle(
    letters: str = Query(
        "", description="Scrambled letters to solve"
    ),
    min_word_length: int = Query(
        3, description="Minimum word length to include in results", ge=1, le=10
    ),
):
    """
    Solve word puzzles by finding all valid words that can be formed from the given letters.

    Args:
        letters: String of letters to use for forming words
        min_word_length: Minimum length of words to include (default: 3)

    Returns:
        JSON response with list of valid words
    """
    if DICTIONARY is None:
        raise HTTPException(status_code=500, detail="Dictionary not loaded")

    # Validate input
    validation = validate_letters(letters)
    if not validation["valid"]:
        return format_error_response(validation["errors"])

    cleaned_letters = validation["cleaned"]

    try:
        # Find valid words with minimum length filter
        dict_type = (
            DICTIONARY_INFO.get("type", "scowl_large")
            if DICTIONARY_INFO
            else "scowl_large"
        )
        valid_words = find_valid_words(
            cleaned_letters, DICTIONARY, min_word_length, dict_type
        )

        logger.info(
            f"Found {len(valid_words)} words for letters: {cleaned_letters} (min length: {min_word_length})"
        )

        return format_response(valid_words, cleaned_letters)

    except Exception as e:
        logger.error(f"Error solving puzzle: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/anagrams")
async def find_anagrams(
    letters: str = Query(
        "", description="Letters to find anagrams for"
    ),
    min_word_length: int = Query(
        3, description="Minimum word length to include in results", ge=1, le=10
    ),
):
    """
    Find anagrams - words that use all the given letters exactly once.

    Args:
        letters: String of letters to find anagrams for
        min_word_length: Minimum length of words to include (default: 3)

    Returns:
        JSON response with list of anagrams
    """
    if DICTIONARY is None:
        raise HTTPException(status_code=500, detail="Dictionary not loaded")

    # Validate input
    validation = validate_letters(letters)
    if not validation["valid"]:
        return format_error_response(validation["errors"])

    cleaned_letters = validation["cleaned"]

    try:
        # Find anagrams with minimum length filter
        dict_type = (
            DICTIONARY_INFO.get("type", "scowl_large")
            if DICTIONARY_INFO
            else "scowl_large"
        )
        anagrams = get_anagrams(cleaned_letters, DICTIONARY, min_word_length, dict_type)

        logger.info(
            f"Found {len(anagrams)} anagrams for letters: {cleaned_letters} (min length: {min_word_length})"
        )

        return format_response(anagrams, cleaned_letters)

    except Exception as e:
        logger.error(f"Error finding anagrams: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    """Health check endpoint with dictionary configuration info."""
    return {
        "status": "healthy",
        "dictionary_loaded": DICTIONARY is not None,
        "dictionary_size": len(DICTIONARY) if DICTIONARY else 0,
        "dictionary_info": DICTIONARY_INFO if DICTIONARY_INFO else {},
        "configuration": {
            "dictionary_type": Config.DICTIONARY_TYPE.value,
            "environment_var": "WORDMIXR_DICTIONARY",
            "available_types": [
                "google_10k",
                "scowl_medium",
                "scowl_large",
                "comprehensive",
                "auto",
            ],
        },
    }


if __name__ == "__main__":
    import uvicorn

    # Bind to all interfaces for containerized deployment
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104
