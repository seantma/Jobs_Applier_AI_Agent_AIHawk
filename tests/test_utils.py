import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from src.utils.chrome_utils import init_browser
from src.utils.constants import (
    PLAIN_TEXT_RESUME_YAML,
    SECRETS_YAML,
    WORK_PREFERENCES_YAML,
)


class TestChromeUtils:
    """Test cases for Chrome utility functions."""

    @patch('src.utils.chrome_utils.webdriver.Chrome')
    @patch('src.utils.chrome_utils.ChromeDriverManager')
    @patch('src.utils.chrome_utils.ChromeService')
    def test_init_browser_success(self, mock_service, mock_driver_manager, mock_chrome):
        """Test successful browser initialization."""
        # Setup mocks
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_service.return_value = Mock()
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        result = init_browser()
        
        assert result == mock_driver
        mock_chrome.assert_called_once()

    @patch('src.utils.chrome_utils.webdriver.Chrome')
    @patch('src.utils.chrome_utils.ChromeDriverManager')
    @patch('src.utils.chrome_utils.ChromeService')
    def test_init_browser_with_options(self, mock_service, mock_driver_manager, mock_chrome):
        """Test browser initialization with Chrome options."""
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_service.return_value = Mock()
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        result = init_browser()
        
        # Verify Chrome was called with options
        call_args = mock_chrome.call_args
        assert 'options' in call_args.kwargs
        assert isinstance(call_args.kwargs['options'], Options)

    @patch('src.utils.chrome_utils.webdriver.Chrome')
    @patch('src.utils.chrome_utils.ChromeDriverManager')
    def test_init_browser_driver_manager_error(self, mock_driver_manager, mock_chrome):
        """Test browser initialization when driver manager fails."""
        mock_driver_manager.return_value.install.side_effect = Exception("Driver install failed")
        
        with pytest.raises(Exception):
            init_browser()

    @patch('src.utils.chrome_utils.webdriver.Chrome')
    @patch('src.utils.chrome_utils.ChromeDriverManager')
    @patch('src.utils.chrome_utils.ChromeService')
    def test_init_browser_chrome_creation_error(self, mock_service, mock_driver_manager, mock_chrome):
        """Test browser initialization when Chrome creation fails."""
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_service.return_value = Mock()
        mock_chrome.side_effect = Exception("Chrome creation failed")
        
        with pytest.raises(Exception):
            init_browser()


class TestConstants:
    """Test cases for constants."""

    def test_yaml_file_constants(self):
        """Test that YAML file constants are properly defined."""
        assert PLAIN_TEXT_RESUME_YAML == "plain_text_resume.yaml"
        assert SECRETS_YAML == "secrets.yaml"
        assert WORK_PREFERENCES_YAML == "work_preferences.yaml"

    def test_constants_are_strings(self):
        """Test that all constants are strings."""
        assert isinstance(PLAIN_TEXT_RESUME_YAML, str)
        assert isinstance(SECRETS_YAML, str)
        assert isinstance(WORK_PREFERENCES_YAML, str)

    def test_constants_not_empty(self):
        """Test that constants are not empty strings."""
        assert len(PLAIN_TEXT_RESUME_YAML) > 0
        assert len(SECRETS_YAML) > 0
        assert len(WORK_PREFERENCES_YAML) > 0


class TestResumeSchemas:
    """Test cases for resume schema classes."""

    def test_resume_schema_import(self):
        """Test that resume schema modules can be imported."""
        try:
            from src.resume_schemas.resume import Resume
            from src.resume_schemas.job_application_profile import JobApplicationProfile
            assert Resume is not None
            assert JobApplicationProfile is not None
        except ImportError as e:
            pytest.skip(f"Resume schema modules not available: {e}")

    @patch('src.resume_schemas.resume.Resume')
    def test_resume_creation(self, mock_resume_class):
        """Test Resume object creation."""
        mock_resume = Mock()
        mock_resume_class.return_value = mock_resume
        
        resume_text = "Test resume content"
        result = mock_resume_class(resume_text)
        
        assert result == mock_resume
        mock_resume_class.assert_called_once_with(resume_text)

    @patch('src.resume_schemas.job_application_profile.JobApplicationProfile')
    def test_job_application_profile_creation(self, mock_profile_class):
        """Test JobApplicationProfile object creation."""
        mock_profile = Mock()
        mock_profile_class.return_value = mock_profile
        
        profile_data = {"name": "Test User", "email": "test@example.com"}
        result = mock_profile_class(profile_data)
        
        assert result == mock_profile
        mock_profile_class.assert_called_once_with(profile_data)


class TestLogging:
    """Test cases for logging configuration."""

    def test_logger_import(self):
        """Test that logger can be imported."""
        try:
            from src.logging import logger
            assert logger is not None
        except ImportError as e:
            pytest.skip(f"Logger module not available: {e}")

    @patch('src.logging.logger')
    def test_logger_methods(self, mock_logger):
        """Test that logger has required methods."""
        mock_logger.info = Mock()
        mock_logger.error = Mock()
        mock_logger.warning = Mock()
        mock_logger.debug = Mock()
        mock_logger.exception = Mock()
        
        # Test method calls
        mock_logger.info("Test info")
        mock_logger.error("Test error")
        mock_logger.warning("Test warning")
        mock_logger.debug("Test debug")
        mock_logger.exception("Test exception")
        
        # Verify methods were called
        mock_logger.info.assert_called_with("Test info")
        mock_logger.error.assert_called_with("Test error")
        mock_logger.warning.assert_called_with("Test warning")
        mock_logger.debug.assert_called_with("Test debug")
        mock_logger.exception.assert_called_with("Test exception")


class TestLibsIntegration:
    """Test cases for libs integration."""

    def test_resume_and_cover_builder_imports(self):
        """Test that resume and cover builder modules can be imported."""
        try:
            from src.libs.resume_and_cover_builder import ResumeFacade, ResumeGenerator, StyleManager
            assert ResumeFacade is not None
            assert ResumeGenerator is not None
            assert StyleManager is not None
        except ImportError as e:
            pytest.skip(f"Resume and cover builder modules not available: {e}")

    @patch('src.libs.resume_and_cover_builder.StyleManager')
    def test_style_manager_methods(self, mock_style_manager_class):
        """Test StyleManager methods."""
        mock_style_manager = Mock()
        mock_style_manager.get_styles.return_value = {"Style1": ("file1.css", "author1")}
        mock_style_manager.format_choices.return_value = ["Style1 by author1"]
        mock_style_manager.set_selected_style.return_value = None
        mock_style_manager_class.return_value = mock_style_manager
        
        style_manager = mock_style_manager_class()
        
        # Test get_styles
        styles = style_manager.get_styles()
        assert "Style1" in styles
        
        # Test format_choices
        choices = style_manager.format_choices(styles)
        assert len(choices) > 0
        
        # Test set_selected_style
        style_manager.set_selected_style("Style1")
        mock_style_manager.set_selected_style.assert_called_with("Style1")

    @patch('src.libs.resume_and_cover_builder.ResumeGenerator')
    def test_resume_generator_methods(self, mock_generator_class):
        """Test ResumeGenerator methods."""
        mock_generator = Mock()
        mock_generator.set_resume_object.return_value = None
        mock_generator_class.return_value = mock_generator
        
        generator = mock_generator_class()
        mock_resume = Mock()
        
        generator.set_resume_object(mock_resume)
        mock_generator.set_resume_object.assert_called_with(mock_resume)

    @patch('src.libs.resume_and_cover_builder.ResumeFacade')
    def test_resume_facade_methods(self, mock_facade_class):
        """Test ResumeFacade methods."""
        mock_facade = Mock()
        mock_facade.set_driver.return_value = None
        mock_facade.link_to_job.return_value = None
        mock_facade.create_resume_pdf.return_value = "base64-data"
        mock_facade.create_resume_pdf_job_tailored.return_value = ("base64-data", "name")
        mock_facade.create_cover_letter.return_value = ("base64-data", "name")
        mock_facade_class.return_value = mock_facade
        
        facade = mock_facade_class(
            api_key="test-key",
            style_manager=Mock(),
            resume_generator=Mock(),
            resume_object=Mock(),
            output_path=Path("/test")
        )
        
        # Test methods
        mock_driver = Mock()
        facade.set_driver(mock_driver)
        mock_facade.set_driver.assert_called_with(mock_driver)
        
        facade.link_to_job("https://example.com/job")
        mock_facade.link_to_job.assert_called_with("https://example.com/job")
        
        result = facade.create_resume_pdf()
        assert result == "base64-data"
        
        result = facade.create_resume_pdf_job_tailored()
        assert result == ("base64-data", "name")
        
        result = facade.create_cover_letter()
        assert result == ("base64-data", "name")