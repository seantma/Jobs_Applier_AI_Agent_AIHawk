import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def valid_secrets_data():
    """Valid secrets YAML data."""
    return {
        "llm_api_key": "sk-test-key-12345"
    }


@pytest.fixture
def valid_config_data():
    """Valid configuration YAML data."""
    return {
        "remote": True,
        "experience_level": {
            "internship": False,
            "entry": True,
            "associate": True,
            "mid_senior_level": True,
            "director": False,
            "executive": False
        },
        "job_types": {
            "full_time": True,
            "contract": False,
            "part_time": False,
            "temporary": False,
            "internship": False,
            "other": False,
            "volunteer": False
        },
        "date": {
            "all_time": False,
            "month": False,
            "week": True,
            "24_hours": False
        },
        "positions": ["Software Engineer", "Python Developer"],
        "locations": ["San Francisco", "Remote"],
        "location_blacklist": ["New York"],
        "distance": 25,
        "company_blacklist": ["BadCompany"],
        "title_blacklist": ["Senior Manager"]
    }


@pytest.fixture
def invalid_config_data():
    """Invalid configuration YAML data (missing required keys)."""
    return {
        "remote": True,
        "positions": ["Software Engineer"]
    }


@pytest.fixture
def sample_resume_data():
    """Sample resume YAML data."""
    return {
        "personal_information": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-0123"
        },
        "summary": "Experienced software engineer with 5 years of experience.",
        "experience": [
            {
                "company": "Tech Corp",
                "position": "Software Engineer",
                "duration": "2020-2023"
            }
        ]
    }


@pytest.fixture
def create_yaml_file():
    """Factory fixture to create YAML files."""
    def _create_yaml_file(path: Path, data: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            yaml.dump(data, f)
        return path
    return _create_yaml_file


@pytest.fixture
def mock_selenium_driver():
    """Mock Selenium WebDriver."""
    driver = Mock()
    driver.quit = Mock()
    driver.get = Mock()
    driver.find_element = Mock()
    return driver


@pytest.fixture
def mock_inquirer_prompt():
    """Mock inquirer.prompt function."""
    def _mock_prompt(questions):
        # Default responses for different question types
        if questions[0].message.startswith("Select a style"):
            return {"style": "Default Style"}
        elif "job description" in questions[0].message.lower():
            return {"job_url": "https://example.com/job"}
        elif "action you want to perform" in questions[0].message:
            return {"action": "Generate Resume"}
        return {}
    return _mock_prompt