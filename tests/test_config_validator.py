import pytest
import yaml
from pathlib import Path
from main import ConfigValidator, ConfigError


class TestConfigValidator:
    """Test cases for ConfigValidator class."""

    def test_validate_email_valid(self):
        """Test email validation with valid emails."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@456.com"
        ]
        for email in valid_emails:
            assert ConfigValidator.validate_email(email) is True

    def test_validate_email_invalid(self):
        """Test email validation with invalid emails."""
        invalid_emails = [
            "invalid.email",
            "@example.com",
            "user@",
            "user@domain",
            "user name@example.com",
            ""
        ]
        for email in invalid_emails:
            assert ConfigValidator.validate_email(email) is False

    def test_load_yaml_valid_file(self, temp_dir, create_yaml_file, valid_config_data):
        """Test loading a valid YAML file."""
        yaml_file = temp_dir / "config.yaml"
        create_yaml_file(yaml_file, valid_config_data)
        
        result = ConfigValidator.load_yaml(yaml_file)
        assert result == valid_config_data

    def test_load_yaml_file_not_found(self, temp_dir):
        """Test loading a non-existent YAML file."""
        yaml_file = temp_dir / "nonexistent.yaml"
        
        with pytest.raises(ConfigError, match="YAML file not found"):
            ConfigValidator.load_yaml(yaml_file)

    def test_load_yaml_invalid_yaml(self, temp_dir):
        """Test loading an invalid YAML file."""
        yaml_file = temp_dir / "invalid.yaml"
        yaml_file.write_text("invalid: yaml: content: [")
        
        with pytest.raises(ConfigError, match="Error reading YAML file"):
            ConfigValidator.load_yaml(yaml_file)

    def test_validate_config_valid(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validating a valid configuration file."""
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, valid_config_data)
        
        result = ConfigValidator.validate_config(config_file)
        assert result == valid_config_data

    def test_validate_config_missing_required_key(self, temp_dir, create_yaml_file):
        """Test validation with missing required keys."""
        incomplete_config = {"remote": True}
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, incomplete_config)
        
        with pytest.raises(ConfigError, match="Missing required key"):
            ConfigValidator.validate_config(config_file)

    def test_validate_config_invalid_type(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validation with invalid data types."""
        invalid_config = valid_config_data.copy()
        invalid_config["remote"] = "not_a_boolean"
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, invalid_config)
        
        with pytest.raises(ConfigError, match="Invalid type for key"):
            ConfigValidator.validate_config(config_file)

    def test_validate_config_invalid_experience_level(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validation with invalid experience level values."""
        invalid_config = valid_config_data.copy()
        invalid_config["experience_level"]["entry"] = "not_boolean"
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, invalid_config)
        
        with pytest.raises(ConfigError, match="Experience level .* must be a boolean"):
            ConfigValidator.validate_config(config_file)

    def test_validate_config_invalid_job_type(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validation with invalid job type values."""
        invalid_config = valid_config_data.copy()
        invalid_config["job_types"]["full_time"] = "not_boolean"
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, invalid_config)
        
        with pytest.raises(ConfigError, match="Job type .* must be a boolean"):
            ConfigValidator.validate_config(config_file)

    def test_validate_config_invalid_date_filter(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validation with invalid date filter values."""
        invalid_config = valid_config_data.copy()
        invalid_config["date"]["week"] = "not_boolean"
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, invalid_config)
        
        with pytest.raises(ConfigError, match="Date filter .* must be a boolean"):
            ConfigValidator.validate_config(config_file)

    def test_validate_config_invalid_distance(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validation with invalid distance values."""
        invalid_config = valid_config_data.copy()
        invalid_config["distance"] = 99  # Not in approved distances
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, invalid_config)
        
        with pytest.raises(ConfigError, match="Invalid distance value"):
            ConfigValidator.validate_config(config_file)

    def test_validate_config_invalid_positions_list(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validation with invalid positions list."""
        invalid_config = valid_config_data.copy()
        invalid_config["positions"] = ["valid", 123]  # Contains non-string
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, invalid_config)
        
        with pytest.raises(ConfigError, match="'positions' must be a list of strings"):
            ConfigValidator.validate_config(config_file)

    def test_validate_config_null_blacklists(self, temp_dir, create_yaml_file, valid_config_data):
        """Test validation with null blacklist values."""
        config_with_nulls = valid_config_data.copy()
        config_with_nulls["company_blacklist"] = None
        config_with_nulls["title_blacklist"] = None
        config_with_nulls["location_blacklist"] = None
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, config_with_nulls)
        
        result = ConfigValidator.validate_config(config_file)
        assert result["company_blacklist"] == []
        assert result["title_blacklist"] == []
        assert result["location_blacklist"] == []

    def test_validate_secrets_valid(self, temp_dir, create_yaml_file, valid_secrets_data):
        """Test validating valid secrets file."""
        secrets_file = temp_dir / "secrets.yaml"
        create_yaml_file(secrets_file, valid_secrets_data)
        
        result = ConfigValidator.validate_secrets(secrets_file)
        assert result == valid_secrets_data["llm_api_key"]

    def test_validate_secrets_missing_key(self, temp_dir, create_yaml_file):
        """Test validation with missing API key."""
        invalid_secrets = {}
        secrets_file = temp_dir / "secrets.yaml"
        create_yaml_file(secrets_file, invalid_secrets)
        
        with pytest.raises(ConfigError, match="Missing secret 'llm_api_key'"):
            ConfigValidator.validate_secrets(secrets_file)

    def test_validate_secrets_empty_key(self, temp_dir, create_yaml_file):
        """Test validation with empty API key."""
        invalid_secrets = {"llm_api_key": ""}
        secrets_file = temp_dir / "secrets.yaml"
        create_yaml_file(secrets_file, invalid_secrets)
        
        with pytest.raises(ConfigError, match="Secret 'llm_api_key' cannot be empty"):
            ConfigValidator.validate_secrets(secrets_file)

    def test_validate_config_missing_optional_blacklists(self, temp_dir, create_yaml_file):
        """Test validation when optional blacklist fields are missing."""
        minimal_config = {
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
            "positions": ["Software Engineer"],
            "locations": ["Remote"],
            "distance": 25
        }
        config_file = temp_dir / "config.yaml"
        create_yaml_file(config_file, minimal_config)
        
        result = ConfigValidator.validate_config(config_file)
        assert result["company_blacklist"] == []
        assert result["title_blacklist"] == []
        assert result["location_blacklist"] == []