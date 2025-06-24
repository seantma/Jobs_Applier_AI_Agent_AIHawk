# AIHawk Test Suite

This directory contains comprehensive test cases for the AIHawk Jobs Applier AI Agent application.

## Test Structure

### Test Files

- **`conftest.py`** - Pytest fixtures and test configuration
- **`test_config_validator.py`** - Unit tests for ConfigValidator class
- **`test_file_manager.py`** - Unit tests for FileManager class
- **`test_main_integration.py`** - Integration tests for main workflow functions
- **`test_utils.py`** - Tests for utility modules and helper functions

### Test Categories

#### Unit Tests
- **ConfigValidator Tests**: Email validation, YAML loading, configuration validation
- **FileManager Tests**: Data folder validation, file operations, uploads handling
- **Utility Tests**: Chrome browser initialization, constants validation, logging

#### Integration Tests
- **Main Workflow Tests**: End-to-end testing of resume/cover letter generation
- **User Interaction Tests**: CLI prompt handling and action processing
- **Error Handling Tests**: Exception handling and error recovery

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_config_validator.py

# Run specific test class
pytest tests/test_config_validator.py::TestConfigValidator

# Run specific test method
pytest tests/test_config_validator.py::TestConfigValidator::test_validate_email_valid
```

### Coverage Reports
```bash
# Run tests with coverage
pytest --cov=src --cov=main

# Generate HTML coverage report
pytest --cov=src --cov=main --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Markers
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Configuration

The test suite is configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--tb=short",
    "--cov=src",
    "--cov=main",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--cov-fail-under=80"
]
```

## Test Fixtures

### Common Fixtures (conftest.py)

- **`temp_dir`** - Temporary directory for test files
- **`valid_secrets_data`** - Valid secrets YAML structure
- **`valid_config_data`** - Valid configuration YAML structure
- **`sample_resume_data`** - Sample resume data for testing
- **`create_yaml_file`** - Factory for creating YAML test files
- **`mock_selenium_driver`** - Mock WebDriver for browser tests
- **`mock_inquirer_prompt`** - Mock user prompt responses

## Test Coverage Areas

### Configuration Management
- ✅ YAML file loading and parsing
- ✅ Configuration validation rules
- ✅ Email format validation
- ✅ Required field checking
- ✅ Data type validation
- ✅ Error handling for invalid configs

### File Operations
- ✅ Data folder structure validation
- ✅ Required file existence checking
- ✅ Output directory creation
- ✅ File upload handling
- ✅ Path resolution and validation

### Main Application Flow
- ✅ User action prompting
- ✅ Resume PDF generation
- ✅ Job-tailored resume creation
- ✅ Cover letter generation
- ✅ Error handling and logging
- ✅ CLI interaction flow

### Utility Functions
- ✅ Chrome browser initialization
- ✅ Constants definition and usage
- ✅ Logging configuration
- ✅ Schema imports and object creation

## Mocking Strategy

The test suite uses extensive mocking to:

- **Isolate units under test** - Each test focuses on specific functionality
- **Avoid external dependencies** - No actual file I/O, web requests, or browser automation
- **Speed up execution** - Tests run quickly without real operations
- **Control test conditions** - Predictable inputs and outputs for reliable testing

## Adding New Tests

When adding new functionality to the application:

1. **Create corresponding test files** - Follow the `test_*.py` naming convention
2. **Use appropriate fixtures** - Leverage existing fixtures or create new ones
3. **Mock external dependencies** - Use unittest.mock for external calls
4. **Test both success and failure cases** - Include error handling tests
5. **Update test markers** - Add appropriate unit/integration/slow markers
6. **Maintain coverage** - Ensure new code is covered by tests

## Test Dependencies

The test suite requires:

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Enhanced mocking capabilities
- **unittest.mock** - Built-in mocking (Python standard library)

## Known Limitations

- **External API calls** - Not tested (mocked instead)
- **Browser automation** - Uses mock WebDriver
- **File system operations** - Use temporary directories
- **Network requests** - Mocked to avoid external dependencies

## Troubleshooting

### Common Issues

1. **Import errors** - Ensure PYTHONPATH includes project root
2. **Missing fixtures** - Check conftest.py for available fixtures
3. **Mock assertions failing** - Verify mock setup and expected calls
4. **Coverage below threshold** - Add tests for uncovered code paths

### Debug Tips

```bash
# Run tests with debug output
pytest -s -vv

# Run single test with full traceback
pytest --tb=long tests/test_config_validator.py::TestConfigValidator::test_validate_email_valid

# Run tests without coverage for cleaner output
pytest --no-cov
```