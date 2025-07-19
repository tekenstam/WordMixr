#!/usr/bin/env python3
"""
Test runner script for WordMixr backend tests.
This script demonstrates the comprehensive testing suite.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run all tests and generate reports"""
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print("🧪 WordMixr Backend Testing Suite")
    print("=" * 50)
    
    # Check if pytest is available
    try:
        import pytest
        print("✅ pytest found")
    except ImportError:
        print("❌ pytest not found. Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run different test categories
    test_commands = [
        {
            "name": "🔬 Unit Tests (Solver Functions)",
            "command": ["python", "-m", "pytest", "tests/test_solver.py::TestSolverFunctions", "-v"],
            "description": "Testing core word solving algorithms"
        },
        {
            "name": "📊 Data Quality Tests", 
            "command": ["python", "-m", "pytest", "tests/test_solver.py::TestDataQuality", "-v"],
            "description": "Testing dictionary quality and critical word coverage"
        },
        {
            "name": "🔧 Dictionary Loading Tests",
            "command": ["python", "-m", "pytest", "tests/test_solver.py::TestDictionaryLoading", "-v"],
            "description": "Testing dictionary loading and size expectations"
        },
        {
            "name": "🌐 API Integration Tests",
            "command": ["python", "-m", "pytest", "tests/test_api.py::TestAPIEndpoints", "-v"],
            "description": "Testing API endpoints and responses"
        },
        {
            "name": "⚙️ Configuration Tests",
            "command": ["python", "-m", "pytest", "tests/test_config.py", "-v"],
            "description": "Testing configuration management"
        },
        {
            "name": "🎯 Critical Word Coverage Tests",
            "command": ["python", "-m", "pytest", "tests/test_solver.py::TestIntegration", "-v"],
            "description": "Testing Word Cookies scenarios (ache, gird, etc.)"
        }
    ]
    
    results = []
    
    for test_suite in test_commands:
        print(f"\n{test_suite['name']}")
        print(f"📋 {test_suite['description']}")
        print("-" * 40)
        
        try:
            result = subprocess.run(
                test_suite["command"],
                capture_output=True,
                text=True,
                cwd=backend_dir
            )
            
            if result.returncode == 0:
                print("✅ PASSED")
                results.append(("PASS", test_suite["name"]))
            else:
                print("❌ FAILED")
                print("Error output:")
                print(result.stdout)
                print(result.stderr)
                results.append(("FAIL", test_suite["name"]))
                
        except Exception as e:
            print(f"⚠️  ERROR: {e}")
            results.append(("ERROR", test_suite["name"]))
    
    # Summary
    print("\n" + "=" * 50)
    print("📈 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for status, _ in results if status == "PASS")
    failed = sum(1 for status, _ in results if status == "FAIL")
    errors = sum(1 for status, _ in results if status == "ERROR")
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Errors: {errors}")
    print(f"📊 Total: {len(results)}")
    
    # List results
    for status, name in results:
        status_icon = {"PASS": "✅", "FAIL": "❌", "ERROR": "⚠️"}[status]
        print(f"  {status_icon} {name}")
    
    # Run specific data quality demonstration
    print("\n" + "=" * 50)
    print("🎯 CRITICAL WORD VERIFICATION")
    print("=" * 50)
    
    try:
        # Change to app directory for dictionary access
        os.chdir(backend_dir / "app")
        
        # Import and test critical words
        sys.path.insert(0, str(backend_dir / "app"))
        from solver import load_dictionary, find_valid_words
        
        print("Loading dictionary...")
        dictionary, dict_info = load_dictionary()
        print(f"✅ Loaded {len(dictionary):,} words from {dict_info['type']} dictionary")
        
        # Test critical scenarios
        test_cases = [
            {
                "letters": "bhace",
                "critical_words": ["ache", "beach", "each"],
                "description": "Word Cookies BHACE scenario"
            },
            {
                "letters": "grindk", 
                "critical_words": ["gird", "grid", "grind", "drink"],
                "description": "Word Cookies GRINDK scenario"
            }
        ]
        
        for case in test_cases:
            print(f"\n🎮 Testing: {case['description']}")
            words = find_valid_words(case["letters"], dictionary, min_length=3)
            
            print(f"  📝 Input: {case['letters']}")
            print(f"  📊 Found: {len(words)} words")
            
            for critical_word in case["critical_words"]:
                if critical_word in words:
                    print(f"  ✅ '{critical_word}' found")
                else:
                    print(f"  ❌ '{critical_word}' MISSING")
        
        print(f"\n✅ Data quality verification complete")
        
    except Exception as e:
        print(f"❌ Data quality verification failed: {e}")
    
    print("\n🎉 Testing complete!")
    return failed == 0 and errors == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 