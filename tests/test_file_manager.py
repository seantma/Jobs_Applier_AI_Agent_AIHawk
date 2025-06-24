import pytest
from pathlib import Path
from main import FileManager
from src.utils.constants import (
    PLAIN_TEXT_RESUME_YAML,
    SECRETS_YAML,
    WORK_PREFERENCES_YAML,
)


class TestFileManager:
    """Test cases for FileManager class."""

    def test_validate_data_folder_success(self, temp_dir, create_yaml_file, valid_config_data, valid_secrets_data, sample_resume_data):
        """Test successful validation of data folder with all required files."""
        data_folder = temp_dir / "data_folder"
        
        # Create required files
        create_yaml_file(data_folder / SECRETS_YAML, valid_secrets_data)
        create_yaml_file(data_folder / WORK_PREFERENCES_YAML, valid_config_data)
        create_yaml_file(data_folder / PLAIN_TEXT_RESUME_YAML, sample_resume_data)
        
        secrets_file, config_file, resume_file, output_folder = FileManager.validate_data_folder(data_folder)
        
        assert secrets_file == data_folder / SECRETS_YAML
        assert config_file == data_folder / WORK_PREFERENCES_YAML
        assert resume_file == data_folder / PLAIN_TEXT_RESUME_YAML
        assert output_folder == data_folder / "output"
        assert output_folder.exists()
        assert output_folder.is_dir()

    def test_validate_data_folder_not_exists(self, temp_dir):
        """Test validation when data folder doesn't exist."""
        non_existent_folder = temp_dir / "non_existent"
        
        with pytest.raises(FileNotFoundError, match="Data folder not found"):
            FileManager.validate_data_folder(non_existent_folder)

    def test_validate_data_folder_missing_secrets(self, temp_dir, create_yaml_file, valid_config_data, sample_resume_data):
        """Test validation when secrets.yaml is missing."""
        data_folder = temp_dir / "data_folder"
        
        # Create only some of the required files
        create_yaml_file(data_folder / WORK_PREFERENCES_YAML, valid_config_data)
        create_yaml_file(data_folder / PLAIN_TEXT_RESUME_YAML, sample_resume_data)
        
        with pytest.raises(FileNotFoundError, match="Missing files in data folder"):
            FileManager.validate_data_folder(data_folder)

    def test_validate_data_folder_missing_config(self, temp_dir, create_yaml_file, valid_secrets_data, sample_resume_data):
        """Test validation when work_preferences.yaml is missing."""
        data_folder = temp_dir / "data_folder"
        
        # Create only some of the required files
        create_yaml_file(data_folder / SECRETS_YAML, valid_secrets_data)
        create_yaml_file(data_folder / PLAIN_TEXT_RESUME_YAML, sample_resume_data)
        
        with pytest.raises(FileNotFoundError, match="Missing files in data folder"):
            FileManager.validate_data_folder(data_folder)

    def test_validate_data_folder_missing_resume(self, temp_dir, create_yaml_file, valid_secrets_data, valid_config_data):
        """Test validation when plain_text_resume.yaml is missing."""
        data_folder = temp_dir / "data_folder"
        
        # Create only some of the required files
        create_yaml_file(data_folder / SECRETS_YAML, valid_secrets_data)
        create_yaml_file(data_folder / WORK_PREFERENCES_YAML, valid_config_data)
        
        with pytest.raises(FileNotFoundError, match="Missing files in data folder"):
            FileManager.validate_data_folder(data_folder)

    def test_validate_data_folder_missing_multiple_files(self, temp_dir, create_yaml_file, valid_secrets_data):
        """Test validation when multiple files are missing."""
        data_folder = temp_dir / "data_folder"
        
        # Create only one required file
        create_yaml_file(data_folder / SECRETS_YAML, valid_secrets_data)
        
        with pytest.raises(FileNotFoundError, match="Missing files in data folder"):
            FileManager.validate_data_folder(data_folder)

    def test_validate_data_folder_creates_output_directory(self, temp_dir, create_yaml_file, valid_config_data, valid_secrets_data, sample_resume_data):
        """Test that validation creates output directory if it doesn't exist."""
        data_folder = temp_dir / "data_folder"
        
        # Create required files
        create_yaml_file(data_folder / SECRETS_YAML, valid_secrets_data)
        create_yaml_file(data_folder / WORK_PREFERENCES_YAML, valid_config_data)
        create_yaml_file(data_folder / PLAIN_TEXT_RESUME_YAML, sample_resume_data)
        
        # Ensure output directory doesn't exist initially
        output_dir = data_folder / "output"
        assert not output_dir.exists()
        
        _, _, _, output_folder = FileManager.validate_data_folder(data_folder)
        
        # Output directory should be created
        assert output_folder.exists()
        assert output_folder.is_dir()

    def test_validate_data_folder_output_directory_exists(self, temp_dir, create_yaml_file, valid_config_data, valid_secrets_data, sample_resume_data):
        """Test validation when output directory already exists."""
        data_folder = temp_dir / "data_folder"
        
        # Create required files
        create_yaml_file(data_folder / SECRETS_YAML, valid_secrets_data)
        create_yaml_file(data_folder / WORK_PREFERENCES_YAML, valid_config_data)
        create_yaml_file(data_folder / PLAIN_TEXT_RESUME_YAML, sample_resume_data)
        
        # Pre-create output directory
        output_dir = data_folder / "output"
        output_dir.mkdir(parents=True)
        
        _, _, _, output_folder = FileManager.validate_data_folder(data_folder)
        
        # Should still work and return existing directory
        assert output_folder == output_dir
        assert output_folder.exists()

    def test_get_uploads_success(self, temp_dir, create_yaml_file, sample_resume_data):
        """Test successful creation of uploads dictionary."""
        resume_file = temp_dir / "resume.yaml"
        create_yaml_file(resume_file, sample_resume_data)
        
        uploads = FileManager.get_uploads(resume_file)
        
        assert "plainTextResume" in uploads
        assert uploads["plainTextResume"] == resume_file

    def test_get_uploads_file_not_found(self, temp_dir):
        """Test get_uploads when resume file doesn't exist."""
        non_existent_file = temp_dir / "non_existent.yaml"
        
        with pytest.raises(FileNotFoundError, match="Plain text resume file not found"):
            FileManager.get_uploads(non_existent_file)

    def test_get_uploads_returns_path_object(self, temp_dir, create_yaml_file, sample_resume_data):
        """Test that get_uploads returns Path objects."""
        resume_file = temp_dir / "resume.yaml"
        create_yaml_file(resume_file, sample_resume_data)
        
        uploads = FileManager.get_uploads(resume_file)
        
        assert isinstance(uploads["plainTextResume"], Path)
        assert uploads["plainTextResume"].exists()

    def test_required_files_constant(self):
        """Test that REQUIRED_FILES contains expected files."""
        expected_files = [SECRETS_YAML, WORK_PREFERENCES_YAML, PLAIN_TEXT_RESUME_YAML]
        assert FileManager.REQUIRED_FILES == expected_files

    def test_validate_data_folder_is_file_not_directory(self, temp_dir):
        """Test validation when data_folder path points to a file instead of directory."""
        data_file = temp_dir / "data_folder.txt"
        data_file.write_text("not a directory")
        
        with pytest.raises(FileNotFoundError, match="Data folder not found"):
            FileManager.validate_data_folder(data_file)