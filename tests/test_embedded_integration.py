#!/usr/bin/env python3
"""
Ludwig Embedded Systems Integration Test

Tests all embedded commands and framework functionality to ensure
everything works together properly.
"""

import subprocess
import sys
import os
import tempfile
import shutil

def run_command(command, cwd=None):
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_embedded_framework_import():
    """Test that the embedded framework can be imported."""
    print("🧪 Testing embedded framework import...")
    
    test_code = """
import sys
sys.path.append('src/frameworks')
import embedded_framework as ef

# Test basic classes
device = ef.EmbeddedDevice('TestDevice')
sensor = ef.TemperatureSensor()
display = ef.Display('Test Display')
smart_home = ef.SmartHomeSystem()
robot = ef.RoboticsSystem()
pos = ef.POSSystem()

print('✅ All embedded classes imported and instantiated successfully')
"""
    
    success, stdout, stderr = run_command(f'python -c "{test_code}"')
    if success:
        print("✅ Embedded framework import test passed")
        return True
    else:
        print(f"❌ Embedded framework import test failed: {stderr}")
        return False

def test_embedded_cli_commands():
    """Test all embedded CLI commands."""
    print("🧪 Testing embedded CLI commands...")
    
    commands = [
        "make:embedded TestDevice",
        "make:pos TestPOS", 
        "make:kiosk TestKiosk",
        "make:scanner TestScanner",
        "make:smarthome TestHome",
        "make:robotics TestRobot"
    ]
    
    all_passed = True
    
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        # Copy ludwig binary and framework to temp directory
        ludwig_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        
        for command in commands:
            print(f"  Testing: {command}")
            success, stdout, stderr = run_command(f'python {ludwig_path}/bin/ludwig {command}')
            
            if success:
                print(f"  ✅ {command} - passed")
                
                # Check that file was created
                expected_files = [
                    "testdevice_embedded.ludwig",
                    "testpos_pos.ludwig", 
                    "testkiosk_kiosk.ludwig",
                    "testscanner_scanner.ludwig",
                    "testhome_smarthome.ludwig",
                    "testrobot_robot.ludwig"
                ]
                
                # Find the expected file for this command
                for expected_file in expected_files:
                    if os.path.exists(expected_file):
                        print(f"    ✅ Generated file: {expected_file}")
                        break
                        
            else:
                print(f"  ❌ {command} - failed: {stderr}")
                all_passed = False
    
    return all_passed

def test_help_command():
    """Test that help shows all embedded commands."""
    print("🧪 Testing help command includes embedded commands...")
    
    ludwig_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    success, stdout, stderr = run_command(f'python {ludwig_path}/bin/ludwig help')
    
    required_commands = [
        "make:embedded",
        "make:pos", 
        "make:kiosk",
        "make:scanner", 
        "make:smarthome",
        "make:robotics"
    ]
    
    all_found = True
    for command in required_commands:
        if command in stdout:
            print(f"  ✅ {command} found in help")
        else:
            print(f"  ❌ {command} missing from help")
            all_found = False
    
    return all_found

def test_examples_exist():
    """Test that embedded examples exist and are valid."""
    print("🧪 Testing embedded examples exist...")
    
    examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "examples", "embedded")
    
    if not os.path.exists(examples_dir):
        print(f"❌ Examples directory missing: {examples_dir}")
        return False
        
    expected_examples = [
        "testiot_embedded.ludwig",
        "testpos_pos.ludwig",
        "testkiosk_kiosk.ludwig", 
        "warehousescanner_scanner.ludwig",
        "smarthouse_smarthome.ludwig",
        "myrobot_robot.ludwig",
        "README.md"
    ]
    
    all_found = True
    for example in expected_examples:
        example_path = os.path.join(examples_dir, example)
        if os.path.exists(example_path):
            print(f"  ✅ {example} exists")
        else:
            print(f"  ❌ {example} missing")
            all_found = False
    
    return all_found

def test_documentation():
    """Test that embedded documentation exists."""
    print("🧪 Testing embedded documentation...")
    
    docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
    
    required_docs = [
        "EMBEDDED_GUIDE.md",
        "FINAL_SUMMARY.md"
    ]
    
    all_found = True
    for doc in required_docs:
        doc_path = os.path.join(docs_dir, doc)
        if os.path.exists(doc_path):
            print(f"  ✅ {doc} exists")
            
            # Check if embedded content is in FINAL_SUMMARY.md
            if doc == "FINAL_SUMMARY.md":
                with open(doc_path, 'r') as f:
                    content = f.read()
                    if "Embedded Systems & IoT" in content:
                        print(f"    ✅ {doc} contains embedded content")
                    else:
                        print(f"    ❌ {doc} missing embedded content")
                        all_found = False
        else:
            print(f"  ❌ {doc} missing")
            all_found = False
    
    return all_found

def main():
    """Run all integration tests."""
    print("🚀 Ludwig Embedded Systems Integration Test")
    print("=" * 50)
    
    tests = [
        ("Framework Import", test_embedded_framework_import),
        ("CLI Commands", test_embedded_cli_commands),
        ("Help Command", test_help_command),
        ("Examples", test_examples_exist),
        ("Documentation", test_documentation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Ludwig embedded systems are ready! 🚀")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
