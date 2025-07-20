import pytest
import os
import sys
from unittest.mock import patch

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from config import Config, DictionaryType

class TestConfiguration:
    """Test configuration management"""
    
    def test_dictionary_type_enum(self):
        """Test DictionaryType enum values"""
        assert DictionaryType.GOOGLE_10K.value == "google_10k"
        assert DictionaryType.SCOWL_MEDIUM.value == "scowl_medium"
        assert DictionaryType.SCOWL_LARGE.value == "scowl_large"
        assert DictionaryType.COMPREHENSIVE.value == "comprehensive"
        assert DictionaryType.AUTO.value == "auto"
    
    def test_default_configuration(self):
        """Test default configuration values"""
        # Default should be SCOWL Large
        assert Config.DICTIONARY_TYPE == DictionaryType.SCOWL_LARGE
    
    def test_dictionary_file_mappings(self):
        """Test dictionary file mappings are properly configured"""
        mappings = Config.DICTIONARY_FILES
        
        # Check all dictionary types have file mappings
        for dict_type in DictionaryType:
            if dict_type != DictionaryType.AUTO:
                assert dict_type in mappings
                assert isinstance(mappings[dict_type], list)
                assert len(mappings[dict_type]) > 0
        
        # Check AUTO has empty list (special case)
        assert mappings[DictionaryType.AUTO] == []
    
    def test_get_dictionary_paths_specific_types(self):
        """Test getting dictionary paths for specific types"""
        # Test SCOWL Large
        with patch.object(Config, 'DICTIONARY_TYPE', DictionaryType.SCOWL_LARGE):
            paths = Config.get_dictionary_paths()
            assert "scowl-large.txt" in paths[0]
        
        # Test SCOWL Medium
        with patch.object(Config, 'DICTIONARY_TYPE', DictionaryType.SCOWL_MEDIUM):
            paths = Config.get_dictionary_paths()
            assert "scowl-medium.txt" in paths[0]
        
        # Test Google 10k
        with patch.object(Config, 'DICTIONARY_TYPE', DictionaryType.GOOGLE_10K):
            paths = Config.get_dictionary_paths()
            assert "google-10000-english.txt" in paths[0]
    
    def test_get_dictionary_paths_auto_mode(self):
        """Test auto mode priority order"""
        with patch.object(Config, 'DICTIONARY_TYPE', DictionaryType.AUTO):
            paths = Config.get_dictionary_paths()
            
            # Should include all dictionary types in priority order
            path_string = " ".join(paths)
            
            # SCOWL Large should come first
            scowl_large_pos = path_string.find("scowl-large.txt")
            scowl_medium_pos = path_string.find("scowl-medium.txt")
            google_10k_pos = path_string.find("google-10000-english.txt")
            comprehensive_pos = path_string.find("words_alpha.txt")
            
            # All should be found
            assert scowl_large_pos != -1
            assert scowl_medium_pos != -1
            assert google_10k_pos != -1
            assert comprehensive_pos != -1
            
            # Check priority order
            assert scowl_large_pos < scowl_medium_pos
            assert scowl_medium_pos < google_10k_pos
            assert google_10k_pos < comprehensive_pos
    
    def test_get_dictionary_info(self):
        """Test dictionary info generation"""
        info = Config.get_dictionary_info()
        
        assert "type" in info
        assert "description" in info
        assert isinstance(info["type"], str)
        assert isinstance(info["description"], str)
        assert len(info["description"]) > 0
    
    def test_dictionary_descriptions(self):
        """Test all dictionary types have descriptions"""
        for dict_type in DictionaryType:
            description = Config._get_dictionary_description(dict_type)
            assert isinstance(description, str)
            assert len(description) > 0
            assert description != "Unknown dictionary type"
    
    def test_description_content_quality(self):
        """Test that descriptions contain relevant information"""
        # SCOWL Large should mention it's good for word games
        scowl_large_desc = Config._get_dictionary_description(DictionaryType.SCOWL_LARGE)
        assert "word games" in scowl_large_desc.lower()
        assert "ache" in scowl_large_desc.lower()
        assert "gird" in scowl_large_desc.lower()
        
        # SCOWL Medium should mention it's missing some words
        scowl_medium_desc = Config._get_dictionary_description(DictionaryType.SCOWL_MEDIUM)
        assert "missing" in scowl_medium_desc.lower()
        assert "gird" in scowl_medium_desc.lower()
        
        # Google 10k should mention limitations
        google_10k_desc = Config._get_dictionary_description(DictionaryType.GOOGLE_10K)
        assert "limited" in google_10k_desc.lower() or "missing" in google_10k_desc.lower()
        
        # Comprehensive should mention noise/filtering
        comprehensive_desc = Config._get_dictionary_description(DictionaryType.COMPREHENSIVE)
        assert "obscure" in comprehensive_desc.lower() or "noise" in comprehensive_desc.lower()

class TestEnvironmentConfiguration:
    """Test environment variable configuration"""
    
    def test_environment_variable_override(self):
        """Test that environment variables override defaults"""
        # Test each dictionary type
        test_cases = [
            ("google_10k", DictionaryType.GOOGLE_10K),
            ("scowl_medium", DictionaryType.SCOWL_MEDIUM),
            ("scowl_large", DictionaryType.SCOWL_LARGE),
            ("comprehensive", DictionaryType.COMPREHENSIVE),
            ("auto", DictionaryType.AUTO),
        ]
        
        for env_value, expected_type in test_cases:
            with patch.dict(os.environ, {'WORDMIXR_DICTIONARY': env_value}):
                # Need to reload the config to pick up env var
                from importlib import reload
                import config
                reload(config)
                
                assert config.Config.DICTIONARY_TYPE.value == expected_type.value
    
    def test_invalid_environment_variable(self):
        """Test handling of invalid environment variable values"""
        with patch.dict(os.environ, {'WORDMIXR_DICTIONARY': 'invalid_value'}):
            with pytest.raises(ValueError):
                # Should raise ValueError for invalid enum value
                from importlib import reload
                import config
                reload(config)
    
    def test_missing_environment_variable(self):
        """Test default when environment variable is not set"""
        with patch.dict(os.environ, {}, clear=True):
            # Remove the environment variable
            if 'WORDMIXR_DICTIONARY' in os.environ:
                del os.environ['WORDMIXR_DICTIONARY']
            
            from importlib import reload
            import config
            reload(config)
            
            # Should default to SCOWL Large
            assert config.Config.DICTIONARY_TYPE.value == DictionaryType.SCOWL_LARGE.value

class TestConfigurationConstants:
    """Test configuration constants and structure"""
    
    def test_all_file_paths_exist_in_mapping(self):
        """Test that all expected file paths are in the mapping"""
        expected_files = {
            DictionaryType.GOOGLE_10K: "google-10000-english.txt",
            DictionaryType.SCOWL_MEDIUM: "scowl-medium.txt", 
            DictionaryType.SCOWL_LARGE: "scowl-large.txt",
            DictionaryType.COMPREHENSIVE: "words_alpha.txt"
        }
        
        for dict_type, expected_file in expected_files.items():
            paths = Config.DICTIONARY_FILES[dict_type]
            assert any(expected_file in path for path in paths)
    
    def test_file_path_variations(self):
        """Test that each dictionary type has multiple path variations"""
        for dict_type in DictionaryType:
            if dict_type != DictionaryType.AUTO:
                paths = Config.DICTIONARY_FILES[dict_type]
                
                # Should have at least 3 variations (relative, /app/, app/)
                assert len(paths) >= 3
                
                # Should include different path prefixes
                path_variations = {
                    "relative": any(not path.startswith("/") and not path.startswith("app/") for path in paths),
                    "absolute": any(path.startswith("/app/") for path in paths),
                    "app_prefix": any(path.startswith("app/") for path in paths)
                }
                
                # At least 2 variations should be present
                assert sum(path_variations.values()) >= 2

class TestConfigIntegration:
    """Test configuration integration with the application"""
    
    def test_config_compatibility_with_solver(self):
        """Test that configuration works with solver module"""
        os.chdir(os.path.join(os.path.dirname(__file__), '..', 'app'))
        
        # Test that we can load dictionary using config paths
        for dict_type in [DictionaryType.SCOWL_LARGE, DictionaryType.SCOWL_MEDIUM, DictionaryType.GOOGLE_10K]:
            with patch.object(Config, 'DICTIONARY_TYPE', dict_type):
                paths = Config.get_dictionary_paths()
                
                # Try to load using the first path that exists
                dictionary = None
                for path in paths:
                    if os.path.exists(path):
                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                dictionary = set(word.strip().lower() for word in f if word.strip())
                        except Exception:
                            continue
                        break
                
                if dictionary is not None:
                    assert isinstance(dictionary, set)
                    assert len(dictionary) > 1000  # Should have substantial word count
    
    def test_config_provides_complete_info(self):
        """Test that config provides all necessary information for API"""
        info = Config.get_dictionary_info()
        
        # Should provide type and description
        assert "type" in info
        assert "description" in info
        
        # Type should be valid
        assert info["type"] in [dt.value for dt in DictionaryType]
        
        # Description should be non-empty and informative
        assert len(info["description"]) > 20  # Substantial description
        assert any(keyword in info["description"].lower() 
                  for keyword in ["word", "dictionary", "game", "quality"]) 