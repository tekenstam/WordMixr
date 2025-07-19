import pytest
import os
import sys
from fastapi.testclient import TestClient

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import app

class TestAPIEndpoints:
    """Test API endpoint functionality"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        # Change to app directory for dictionary file access
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["dictionary_loaded"] == True
        assert data["dictionary_size"] > 0
        assert "dictionary_info" in data
        assert "configuration" in data
        
        # Check configuration structure
        config = data["configuration"]
        assert "dictionary_type" in config
        assert "environment_var" in config
        assert "available_types" in config
        assert isinstance(config["available_types"], list)
    
    def test_solve_endpoint_basic(self, client):
        """Test basic word solving functionality"""
        response = client.get("/solve?letters=bhace&min_word_length=3")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] == True
        assert data["input_letters"] == "bhace"
        assert data["word_count"] > 0
        assert isinstance(data["words"], list)
        
        # Check that critical words are present
        words = data["words"]
        assert "ache" in words, "Missing 'ache' - critical for Word Cookies"
        assert "beach" in words, "Missing 'beach'"
        assert "each" in words, "Missing 'each'"
        
        # Check sorting (shortest to longest, then alphabetical)
        for i in range(len(words) - 1):
            current = words[i]
            next_word = words[i + 1]
            assert (len(current) < len(next_word) or 
                   (len(current) == len(next_word) and current <= next_word))
    
    def test_solve_endpoint_min_length_filter(self, client):
        """Test minimum length filtering"""
        # Test with 4+ letters
        response = client.get("/solve?letters=bhace&min_word_length=4")
        assert response.status_code == 200
        data = response.json()
        
        words = data["words"]
        assert all(len(word) >= 4 for word in words)
        assert "ache" in words
        assert "beach" in words
        
        # Test with 5+ letters
        response = client.get("/solve?letters=bhace&min_word_length=5")
        assert response.status_code == 200
        data = response.json()
        
        words = data["words"]
        assert all(len(word) >= 5 for word in words)
        assert "beach" in words
    
    def test_solve_endpoint_grindk_scenario(self, client):
        """Test the GRINDK scenario that revealed missing 'gird'"""
        response = client.get("/solve?letters=grindk&min_word_length=4")
        
        assert response.status_code == 200
        data = response.json()
        
        words = data["words"]
        assert "gird" in words, "Missing 'gird' - critical for Word Cookies"
        assert "grid" in words
        assert "grin" in words
        assert "grind" in words
        assert "drink" in words
    
    def test_anagrams_endpoint_basic(self, client):
        """Test anagram finding functionality"""
        response = client.get("/anagrams?letters=listen&min_word_length=6")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] == True
        assert data["input_letters"] == "listen"
        assert data["word_count"] > 0
        
        words = data["words"]
        # All words should be exactly 6 letters (anagrams)
        assert all(len(word) == 6 for word in words)
        
        # Should include common anagrams
        expected_anagrams = {"listen", "silent", "enlist", "tinsel", "inlets"}
        found_anagrams = set(words)
        
        # At least some of these should be present
        assert len(expected_anagrams & found_anagrams) >= 3
    
    def test_solve_endpoint_validation(self, client):
        """Test input validation"""
        # Test missing letters parameter
        response = client.get("/solve")
        assert response.status_code == 422  # Validation error
        
        # Test empty letters
        response = client.get("/solve?letters=")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "error" in data or "errors" in data
        
        # Test invalid min_word_length
        response = client.get("/solve?letters=abc&min_word_length=0")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "error" in data or "errors" in data
    
    def test_anagrams_endpoint_validation(self, client):
        """Test anagram endpoint validation"""
        # Test missing letters parameter
        response = client.get("/anagrams")
        assert response.status_code == 422  # Validation error
        
        # Test empty letters
        response = client.get("/anagrams?letters=")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "error" in data or "errors" in data
    
    def test_solve_endpoint_edge_cases(self, client):
        """Test edge cases for solve endpoint"""
        # Test single letter
        response = client.get("/solve?letters=a&min_word_length=1")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        
        # Test repeated letters
        response = client.get("/solve?letters=aaa&min_word_length=2")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        
        # Test mixed case
        response = client.get("/solve?letters=BeAcH&min_word_length=3")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "beach" in data["words"]
        
        # Test special characters (should be cleaned)
        response = client.get("/solve?letters=b-e_a@c#h&min_word_length=3")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    def test_response_structure(self, client):
        """Test API response structure consistency"""
        response = client.get("/solve?letters=test&min_word_length=3")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = ["success", "input_letters", "word_count", "words"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(data["success"], bool)
        assert isinstance(data["input_letters"], str)
        assert isinstance(data["word_count"], int)
        assert isinstance(data["words"], list)
        
        # Check consistency
        assert len(data["words"]) == data["word_count"]

class TestPerformance:
    """Test API performance with various loads"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        return TestClient(app)
    
    def test_solve_performance_large_input(self, client):
        """Test performance with large input"""
        # Test with many letters
        response = client.get("/solve?letters=abcdefghijklmnop&min_word_length=3")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        
        # Should complete in reasonable time (tested by pytest timeout if configured)
        # Just verify it returns a result
        assert data["word_count"] >= 0
    
    def test_solve_performance_short_words(self, client):
        """Test performance with minimum length requirements"""
        response = client.get("/solve?letters=programming&min_word_length=2")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        
        # Should find many words
        assert data["word_count"] > 10

class TestCoverage:
    """Test specific coverage scenarios that were problematic"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        return TestClient(app)
    
    def test_missing_words_coverage(self, client):
        """Test that previously missing words are now covered"""
        test_cases = [
            ("bhace", ["ache", "beach", "each"]),
            ("grindk", ["gird", "grid", "grind", "drink"]),
            ("listen", ["listen", "silent"]),  # For anagram test
        ]
        
        for letters, expected_words in test_cases:
            response = client.get(f"/solve?letters={letters}&min_word_length=3")
            assert response.status_code == 200
            data = response.json()
            
            found_words = set(data["words"])
            for expected_word in expected_words:
                assert expected_word in found_words, f"Missing '{expected_word}' from letters '{letters}'"
    
    def test_dictionary_quality_via_api(self, client):
        """Test dictionary quality through API calls"""
        # Test that problematic words are filtered out
        response = client.get("/solve?letters=haecbch&min_word_length=3")
        assert response.status_code == 200
        data = response.json()
        
        words = data["words"]
        
        # These problematic words should not appear
        problematic_words = ["haec", "bch", "ech", "hae"]
        for word in problematic_words:
            assert word not in words, f"Problematic word '{word}' found in results"
        
        # But good words should appear
        good_words = ["ace", "cab", "each", "beach"]
        found_good_words = [word for word in good_words if word in words]
        assert len(found_good_words) > 0, "No good words found in results" 