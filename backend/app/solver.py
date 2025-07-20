import os
from collections import Counter

from config import Config


def load_dictionary() -> tuple[set, dict]:
    """Load dictionary words from configured file with metadata."""
    # Get dictionary paths from configuration
    dict_paths = Config.get_dictionary_paths()

    # Try to load from each path in order
    for filepath in dict_paths:
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    words = set()
                    for word in f:
                        word = word.strip().lower()
                        if (
                            word and len(word) >= 2
                        ):  # Only include words with 2+ characters
                            words.add(word)

                    # Determine dictionary type based on filepath and size
                    if "google-10000" in filepath:
                        dict_type = "google_10k"
                    elif "scowl-medium" in filepath:
                        dict_type = "scowl_medium"
                    elif "scowl-large" in filepath:
                        dict_type = "scowl_large"
                    elif len(words) < 20000:
                        dict_type = "small"
                    elif len(words) < 70000:
                        dict_type = "medium"
                    elif len(words) < 200000:
                        dict_type = "large"
                    else:
                        dict_type = "comprehensive"

                    dict_info = {
                        "filepath": filepath,
                        "size": len(words),
                        "type": dict_type,
                        "config": Config.get_dictionary_info(),
                    }

                    print(f"Loaded dictionary: {filepath} ({len(words)} words)")
                    return words, dict_info

            except Exception as e:
                print(f"Error loading dictionary from {filepath}: {e}")
                continue

    # Ultimate fallback - small curated dictionary
    print("Warning: Using fallback dictionary")
    fallback_words = {
        "the",
        "be",
        "to",
        "of",
        "and",
        "in",
        "have",
        "it",
        "for",
        "not",
        "with",
        "he",
        "as",
        "you",
        "do",
        "at",
        "this",
        "but",
        "his",
        "by",
        "from",
        "they",
        "she",
        "or",
        "an",
        "will",
        "my",
        "one",
        "all",
        "would",
        "there",
        "their",
        "what",
        "so",
        "up",
        "out",
        "if",
        "about",
        "who",
        "get",
        "which",
        "go",
        "me",
        "when",
        "make",
        "can",
        "like",
        "time",
        "no",
        "just",
        "him",
        "know",
        "take",
        "people",
        "into",
        "year",
        "your",
        "good",
        "some",
        "could",
        "them",
        "see",
        "other",
        "than",
        "then",
        "now",
        "look",
        "only",
        "come",
        "its",
        "over",
        "think",
        "also",
        "back",
        "after",
        "use",
        "two",
        "how",
        "our",
        "work",
        "first",
        "well",
        "way",
        "even",
        "new",
        "want",
        "because",
        "any",
        "these",
        "give",
        "day",
        "most",
        "us",
        "cat",
        "dog",
        "run",
        "sun",
        "fun",
        "gun",
        "cut",
        "put",
        "but",
        "get",
        "set",
        "let",
        "net",
        "pet",
        "wet",
        "yet",
        "met",
        "bet",
        "eat",
        "hat",
        "bat",
        "rat",
        "cat",
        "fat",
        "sat",
        "mat",
        "pat",
        "bad",
        "sad",
        "mad",
        "had",
        "bag",
        "tag",
        "lag",
        "rag",
        "big",
        "dig",
        "fig",
        "pig",
        "wig",
        "hot",
        "pot",
        "lot",
        "not",
        "got",
        "top",
        "pop",
        "hop",
        "cop",
        "red",
        "bed",
        "led",
        "fed",
        "ten",
        "pen",
        "hen",
        "men",
        "den",
        "yes",
        "bus",
        "box",
        "fox",
        "six",
        "mix",
        "fix",
        "zip",
        "tip",
        "lip",
        "hip",
        "dip",
        "cup",
        "pup",
    }

    fallback_info = {
        "filepath": "builtin_fallback",
        "size": len(fallback_words),
        "type": "fallback",
        "config": Config.get_dictionary_info(),
    }

    return fallback_words, fallback_info


def is_valid_word(word, min_length=3, dictionary_type="scowl_large"):
    """Check if a word meets quality criteria with enhanced filtering."""
    # Must be at least minimum length
    if len(word) < min_length:
        return False

    # Skip words that are just repeated letters (like 'aaa', 'bbb')
    if len(set(word)) == 1 and len(word) > 1:
        return False

    # Basic non-words to skip
    non_words = {
        "aa",
        "bb",
        "cc",
        "dd",
        "ee",
        "ff",
        "gg",
        "hh",
        "ii",
        "jj",
        "kk",
        "ll",
        "mm",
        "nn",
        "oo",
        "pp",
        "qq",
        "rr",
        "ss",
        "tt",
        "uu",
        "vv",
        "ww",
        "xx",
        "yy",
        "zz",
    }

    if word in non_words:
        return False

    # Enhanced filtering for comprehensive dictionaries
    if dictionary_type == "comprehensive":
        # Skip obvious Latin words (common Latin endings)
        latin_endings = {"us", "um", "ae", "is", "os", "es", "ei", "ii"}
        if any(word.endswith(ending) for ending in latin_endings) and len(word) <= 5:
            return False

        # Skip words with too many consonants in a row (likely not English)
        consonants = "bcdfghjklmnpqrstvwxyz"
        consonant_count = 0
        max_consonants = 0
        for char in word:
            if char in consonants:
                consonant_count += 1
                max_consonants = max(max_consonants, consonant_count)
            else:
                consonant_count = 0

        if max_consonants > 4:  # More than 4 consonants in a row is suspicious
            return False

        # Skip words with unusual letter patterns
        if word.count("x") > 1 or word.count("z") > 1:
            return False

        # Skip known problematic words from previous analysis
        problematic_words = {
            "haec",
            "hic",
            "hoc",
            "chab",
            "bache",
            "habe",
            "bch",
            "ech",
            "hae",
            "ecb",
            "hcb",
            "ceh",
            "beh",
            "heb",
            "chb",
            "bhc",
        }

        if word in problematic_words:
            return False

    return True


def find_valid_words(letters, dictionary, min_length=3, dictionary_type="scowl_large"):
    """Find all valid words that can be formed using the given letters."""
    if not letters or not dictionary:
        return []

    letter_count = Counter(letters.lower())
    valid_words = set()

    for word in dictionary:
        if len(word) > len(letters):
            continue

        # Apply quality filter
        if not is_valid_word(word, min_length, dictionary_type):
            continue

        word_count = Counter(word)
        # Check if all letters in the word are available in sufficient quantity
        if all(word_count[char] <= letter_count[char] for char in word_count):
            valid_words.add(word)

    # Return sorted list of words, shortest first, then alphabetically
    return sorted(valid_words, key=lambda x: (len(x), x))


def get_anagrams(letters, dictionary, min_length=3, dictionary_type="scowl_large"):
    """Find anagrams (words using all letters exactly once)."""
    if not letters or not dictionary:
        return []

    letter_count = Counter(letters.lower())
    anagrams = []

    for word in dictionary:
        if len(word) == len(letters):
            # Apply quality filter
            if not is_valid_word(word, min_length, dictionary_type):
                continue

            word_count = Counter(word)
            if word_count == letter_count:
                anagrams.append(word)

    return sorted(anagrams, key=lambda x: (len(x), x))
