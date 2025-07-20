import pytest
import os
import sys
from collections import Counter

# Add the app directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from solver import (
    load_dictionary, 
    find_valid_words, 
    get_anagrams, 
    is_valid_word
)

# Helper function for loading specific dictionaries in tests
def load_specific_dictionary(filepath):
    """Helper function to load a specific dictionary file for testing"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            words = set()
            for word in f:
                word = word.strip().lower()
                if word and len(word) >= 2:
                    words.add(word)
            return words
    except FileNotFoundError:
        pytest.skip(f"Dictionary file {filepath} not found - skipping test")
    except Exception as e:
        pytest.fail(f"Error loading dictionary {filepath}: {e}")

class TestDictionaryLoading:
    """Test dictionary loading functionality"""
    
    def test_load_dictionary_scowl_large(self):
        """Test loading SCOWL Large dictionary"""
        # Change to app directory for file access
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        
        dictionary = load_specific_dictionary("scowl-large.txt")
        
        assert isinstance(dictionary, set)
        assert len(dictionary) > 100000  # Should have 120k+ words
        assert "ache" in dictionary  # Critical word for Word Cookies
        assert "gird" in dictionary  # Another critical word we found missing
        assert "beach" in dictionary  # Common word
        
    def test_load_dictionary_scowl_medium(self):
        """Test loading SCOWL Medium dictionary"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        
        dictionary = load_specific_dictionary("scowl-medium.txt")
        
        assert isinstance(dictionary, set)
        assert len(dictionary) > 50000  # Should have 58k+ words
        assert "ache" in dictionary  # Should have this
        assert "gird" not in dictionary  # Missing in medium
        
    def test_load_dictionary_google_10k(self):
        """Test loading Google 10k dictionary"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        
        dictionary = load_specific_dictionary("google-10000-english.txt")
        
        assert isinstance(dictionary, set)
        assert len(dictionary) > 9000  # Should have ~10k words
        assert "beach" in dictionary  # Common word
        assert "ache" not in dictionary  # Missing in Google 10k
        assert "gird" not in dictionary  # Missing in Google 10k

class TestDataQuality:
    """Test data quality and coverage of critical words"""
    
    @pytest.fixture
    def scowl_large_dict(self):
        """Load SCOWL Large dictionary for testing"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        return load_specific_dictionary("scowl-large.txt")
    
    def test_word_cookies_critical_words(self, scowl_large_dict):
        """Test that critical words found missing in earlier testing are present"""
        critical_words = [
            "ache",  # Missing in Google 10k
            "gird",  # Missing in SCOWL Medium and Google 10k
            "beach", # Common word
            "each",  # Common word
            "drink", # Common word
            "grind", # Common word
        ]
        
        for word in critical_words:
            assert word in scowl_large_dict, f"Critical word '{word}' missing from SCOWL Large dictionary"
    
    def test_common_3_letter_words(self, scowl_large_dict):
        """Test coverage of common 3-letter words"""
        common_3_letter = ["the", "and", "you", "are", "for", "can", "had", "her", "his", "one", "our", "out", "day", "get", "has", "him", "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"]
        
        missing_words = [word for word in common_3_letter if word not in scowl_large_dict]
        assert len(missing_words) < 5, f"Too many common 3-letter words missing: {missing_words}"
    
    def test_no_obvious_non_words(self, scowl_large_dict):
        """Test that obvious non-words are not included"""
        # Focus on clearly nonsensical combinations, not abbreviations
        non_words = ["haec", "bch", "ech", "xqz", "qjx", "zxcv"]
        
        present_non_words = [word for word in non_words if word in scowl_large_dict]
        assert len(present_non_words) == 0, f"Non-words found in dictionary: {present_non_words}"
        
        # Note: Some abbreviations like 'aaa', 'bbb', 'xxx' might be legitimate in SCOWL Large

class TestSolverFunctions:
    """Test core solver functionality"""
    
    @pytest.fixture
    def test_dictionary(self):
        """Small test dictionary for controlled testing"""
        return {
            "cat", "act", "tac", "bat", "tab", "cab", "ace", "beach", "each", "ache", "gird"
        }
    
    def test_find_valid_words_basic(self, test_dictionary):
        """Test basic word finding functionality"""
        letters = "bhace"
        words = find_valid_words(letters, test_dictionary, min_length=3)
        
        expected = ["ace", "cab", "ache", "each", "beach"]
        assert set(words) == set(expected)
        
        # Test sorting: shortest first, then alphabetical
        assert words == ["ace", "cab", "ache", "each", "beach"]
    
    def test_find_valid_words_min_length_filter(self, test_dictionary):
        """Test minimum length filtering"""
        letters = "bhace"
        
        # Test 4+ letters
        words_4_plus = find_valid_words(letters, test_dictionary, min_length=4)
        assert set(words_4_plus) == {"ache", "each", "beach"}
        
        # Test 5+ letters
        words_5_plus = find_valid_words(letters, test_dictionary, min_length=5)
        assert words_5_plus == ["beach"]
    
    def test_find_valid_words_letter_constraints(self, test_dictionary):
        """Test that words don't use more letters than available"""
        letters = "abc"  # Available: one 'a', one 'b', one 'c'
        words = find_valid_words(letters, test_dictionary, min_length=2)
        
        # From test_dictionary: {"cat", "act", "tac", "bat", "tab", "cab", "ace", "beach", "each", "ache", "gird"}
        # With letters "abc", only "cab" can be made (uses c,a,b)
        # Other words need letters not in "abc":
        # - "cat", "act", "tac" need 't'  
        # - "bat", "tab" need 't'
        # - "ace" needs 'e'
        # - longer words need other letters
        
        assert "cab" in words  # Should be found - uses c,a,b
        assert "ace" not in words  # Should NOT be found - needs 'e' which isn't available
        assert "cat" not in words  # Should NOT be found - needs 't' which isn't available
    
    def test_get_anagrams_basic(self, test_dictionary):
        """Test anagram finding functionality"""
        letters = "tac"
        anagrams = get_anagrams(letters, test_dictionary, min_length=3)
        
        expected = ["act", "cat", "tac"]  # All permutations of 'tac'
        assert set(anagrams) == set(expected)
        
        # Test sorting
        assert anagrams == sorted(expected, key=lambda x: (len(x), x))
    
    def test_get_anagrams_no_partial_matches(self, test_dictionary):
        """Test that anagrams don't include partial words"""
        letters = "beach"
        anagrams = get_anagrams(letters, test_dictionary, min_length=3)
        
        # Only "beach" uses all 5 letters exactly
        assert anagrams == ["beach"]
        
        # "each" and "ache" are not anagrams because they don't use all letters
        assert "each" not in anagrams
        assert "ache" not in anagrams
    
    def test_is_valid_word_length_filter(self):
        """Test word length filtering"""
        assert is_valid_word("a", min_length=2) == False
        assert is_valid_word("ab", min_length=2) == True
        assert is_valid_word("abc", min_length=3) == True
        assert is_valid_word("ab", min_length=3) == False
    
    def test_is_valid_word_quality_filter(self):
        """Test word quality filtering"""
        # Test repeated letters
        assert is_valid_word("aaa") == False
        assert is_valid_word("bbb") == False
        
        # Test non-words
        assert is_valid_word("aa") == False
        assert is_valid_word("zz") == False
        
        # Test valid words
        assert is_valid_word("cat") == True
        assert is_valid_word("beach") == True
    
    def test_is_valid_word_comprehensive_filtering(self):
        """Test enhanced filtering for comprehensive dictionary"""
        # Test Latin terms filtering for comprehensive dict
        assert is_valid_word("haec", dictionary_type="comprehensive") == False
        assert is_valid_word("hic", dictionary_type="comprehensive") == False
        
        # Test consonant clustering
        assert is_valid_word("bcdfg", dictionary_type="comprehensive") == False
        
        # Test multiple x/z
        assert is_valid_word("xxxx", dictionary_type="comprehensive") == False
        assert is_valid_word("zzzz", dictionary_type="comprehensive") == False
        
        # Test valid words still pass
        assert is_valid_word("beach", dictionary_type="comprehensive") == True
        assert is_valid_word("ache", dictionary_type="comprehensive") == True

class TestIntegration:
    """Integration tests using real dictionaries"""
    
    def test_word_cookies_bhace_scenario(self):
        """Test the specific Word Cookies scenario that revealed missing words"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        dictionary = load_specific_dictionary("scowl-large.txt")
        
        letters = "bhace"
        words = find_valid_words(letters, dictionary, min_length=3)
        
        # Must include the critical words
        assert "ache" in words, "Missing 'ache' - critical for Word Cookies"
        assert "beach" in words, "Missing 'beach'"
        assert "each" in words, "Missing 'each'"
        
        # Test sorting
        assert len(words) > 0
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            # Either shorter word comes first, or same length and alphabetically first
            assert (len(current_word) < len(next_word) or 
                   (len(current_word) == len(next_word) and current_word <= next_word))
    
    def test_word_cookies_grindk_scenario(self):
        """Test the GRINDK scenario that revealed 'gird' was missing"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        dictionary = load_specific_dictionary("scowl-large.txt")
        
        letters = "grindk"
        words = find_valid_words(letters, dictionary, min_length=4)
        
        # Must include the critical words
        assert "gird" in words, "Missing 'gird' - critical for Word Cookies"
        assert "grid" in words, "Missing 'grid'"
        assert "grin" in words, "Missing 'grin'"
        assert "grind" in words, "Missing 'grind'"
        assert "drink" in words, "Missing 'drink'"
    
    def test_dictionary_size_expectations(self):
        """Test that dictionaries meet size expectations"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        
        # SCOWL Large should be substantial
        scowl_large = load_specific_dictionary("scowl-large.txt")
        assert len(scowl_large) > 120000, f"SCOWL Large too small: {len(scowl_large)} words"
        
        # SCOWL Medium should be smaller
        scowl_medium = load_specific_dictionary("scowl-medium.txt")
        assert 50000 < len(scowl_medium) < 70000, f"SCOWL Medium unexpected size: {len(scowl_medium)} words"
        
        # Google 10k should be smallest
        google_10k = load_specific_dictionary("google-10000-english.txt")
        assert 9000 < len(google_10k) < 12000, f"Google 10k unexpected size: {len(google_10k)} words" 