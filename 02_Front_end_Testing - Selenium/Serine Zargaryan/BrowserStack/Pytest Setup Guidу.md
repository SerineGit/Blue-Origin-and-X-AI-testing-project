# Blue Origin Career Website Tests - Pytest Version

Automated tests for Blue Origin career website using pytest framework.

## Project Structure

```
├── test_blueorigin_positive_pytest.py  # Positive test cases
├── test_blueorigin_negative_pytest.py  # Negative test cases  
├── test_helpers_pytest.py              # Helper classes
├── conftest.py                         # Pytest configuration
└── Pytest Setup Guide.md               # Instructions
```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run only positive tests
pytest test_blueorigin_positive_pytest.py

# Run only negative tests
pytest test_blueorigin_negative_pytest.py

# Run specific test
pytest test_blueorigin_positive_pytest.py::TestBlueOriginPositive::test_tc_p_001_navigation_back_to_search
```

### Browser Selection

```bash
# Run with specific browser
pytest --browser=chrome
pytest --browser=firefox  
pytest --browser=edge
```

### Browser Stack
```bash
# PyCharm terminal
$env:BSTACK_USER = "your username"
$env:BSTACK_KEY = "your access key"
$env:USE_BROWSERSTACK = "true"

# command for your terminal
pytest "your test file name.py" #example pytest "test_blueorigin_positive_pytest.py"

# if you want run just one test 
pytest "Your test file namE.py::TestClassName::TestMethod_name for example 002"
# example pytest "test_blueorigin_positive_pytest.py::TestBlueOriginPositive::test_tc_p_002_keyword_search_functionality"
```

### Test Markers

```bash
# Run tests by markers
pytest -m positive  # positive tests only
pytest -m negative  # negative tests only
```

### Verbose Output

```bash
# Detailed output
pytest -v -s

# Stop on first failure
pytest -x

# Re-run last failed tests
pytest --lf
```

### Parallel Execution

```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run tests in parallel
pytest -n auto  # auto-detect number of processes
pytest -n 3     # run with 3 processes
```

## Report Generation

### HTML Report

```bash
# Install pytest-html
pip install pytest-html

# Generate HTML report
pytest --html=report.html --self-contained-html
```

### Allure Report

```bash
# Install allure-pytest
pip install allure-pytest

# Generate Allure results
pytest --alluredir=allure-results

# Serve Allure report (requires Allure CLI installed)
allure serve allure-results

# Generate static Allure report
allure generate allure-results --output allure-report --clean
allure open allure-report
```

#### Installing Allure CLI

**Windows (using Scoop):**
```bash
scoop install allure
```

**macOS (using Homebrew):**
```bash
brew install allure
```

**Linux (manual installation):**
```bash
# Download from GitHub releases
wget https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz
tar -zxvf allure-2.24.0.tgz
export PATH=$PATH:$(pwd)/allure-2.24.0/bin
```

## Test Cases Overview

### Positive Tests (TC_P_001 - TC_P_005)
1. **TC_P_001**: Navigation back to search through job details page
2. **TC_P_002**: Keyword search functionality
3. **TC_P_003**: Search result consistency between systems
4. **TC_P_004**: "Blue Origin Career" logo navigation behavior
5. **TC_P_005**: Keyboard accessibility for job search

### Negative Tests (TC_N_001 - TC_N_005)
1. **TC_N_001**: Job count mismatch between search systems
2. **TC_N_002**: Search logic comparison using numeric keywords
3. **TC_N_003**: Exact job title search consistency verification
4. **TC_N_004**: Search resilience to special characters and spaces
5. **TC_N_005**: Career page functionality with disabled JavaScript

## Configuration Examples

### requirements
```
pytest>=7.0.0
selenium>=4.0.0
pytest-html>=3.0.0
pytest-xdist>=2.0.0
allure-pytest>=2.12.0
webdriver-manager>=3.0.0
```

### pytest.ini
```ini
[tool:pytest]
markers =
    positive: marks tests as positive test cases
    negative: marks tests as negative test cases
    smoke: marks tests as smoke tests
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

## Quick Commands Reference

```bash
# Essential runs
pytest -v --browser=chrome                    # Chrome with verbose output
pytest -m positive --html=report.html         # Positive tests with HTML report
pytest --alluredir=results && allure serve results  # Generate and serve Allure report
pytest -n auto -x                             # Parallel execution, stop on first failure
pytest --lf -v                                # Re-run last failed with verbose output
```