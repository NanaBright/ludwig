#!/usr/bin/env python3
"""
Ludwig CI Test Runner - Local Verification

This script runs the same tests that GitHub Actions will run,
allowing you to verify everything works before pushing.
"""

import subprocess
import sys
import os

def run_test(name, command, expected_success=True):
    """Run a test command and report results."""
    print(f"\n🧪 {name}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        
        if result.returncode == 0:
            print("✅ PASSED")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print("❌ FAILED")
            print(f"Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all CI tests locally."""
    print("🚀 Ludwig CI Test Runner - Local Verification")
    print("=" * 60)
    
    tests = [
        ("Python Environment Check", "python -c 'import collections.abc; print(\"Collections module OK\")'"),
        ("Ludwig Collections Check", "python -c 'import sys; sys.path.append(\"src/frameworks\"); import ludwig_collections; print(\"Ludwig collections OK\")'"),
        ("Embedded Framework Import", "python -c 'import sys; sys.path.append(\"src/frameworks\"); import embedded_framework; print(\"Embedded framework OK\")'"),
        ("Web Framework Import", "python -c 'import web_framework; print(\"Web framework OK\")'"),
        ("Desktop Framework Import", "python -c 'import sys; sys.path.append(\"src/frameworks\"); import desktop_framework; print(\"Desktop framework OK\")'"),
        ("CLI Help Command", "python bin/ludwig help"),
        ("CLI Embedded Command", "python bin/ludwig make:embedded CITestDevice"),
        ("CLI POS Command", "python bin/ludwig make:pos CITestPOS"),
        ("CLI Smart Home Command", "python bin/ludwig make:smarthome CITestHome"),
        ("Integration Tests", "python tests/test_embedded_integration.py"),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, command in tests:
        if run_test(test_name, command):
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Ready for GitHub CI! 🚀")
        
        # Clean up test files
        cleanup_commands = [
            "rm -f citestdevice_embedded.ludwig",
            "rm -f citestpos_pos.ludwig", 
            "rm -f citesthome_smarthome.ludwig"
        ]
        
        for cmd in cleanup_commands:
            subprocess.run(cmd, shell=True, capture_output=True)
            
        print("🧹 Cleaned up test files")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before pushing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
