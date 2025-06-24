import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import base64
from main import (
    main, 
    prompt_user_action, 
    handle_inquiries,
    create_resume_pdf,
    create_resume_pdf_job_tailored,
    create_cover_letter
)


class TestMainIntegration:
    """Integration tests for main workflow functions."""

    @patch('main.inquirer.prompt')
    def test_prompt_user_action_success(self, mock_prompt):
        """Test successful user action prompt."""
        mock_prompt.return_value = {'action': 'Generate Resume'}
        
        result = prompt_user_action()
        
        assert result == 'Generate Resume'
        mock_prompt.assert_called_once()

    @patch('main.inquirer.prompt')
    def test_prompt_user_action_no_answer(self, mock_prompt):
        """Test user action prompt when no answer provided."""
        mock_prompt.return_value = None
        
        result = prompt_user_action()
        
        assert result == ""

    @patch('main.inquirer.prompt')
    def test_prompt_user_action_exception(self, mock_prompt):
        """Test user action prompt when exception occurs."""
        mock_prompt.side_effect = KeyboardInterrupt()
        
        result = prompt_user_action()
        
        assert result == ""

    @patch('main.create_resume_pdf')
    @patch('main.logger')
    def test_handle_inquiries_generate_resume(self, mock_logger, mock_create_resume):
        """Test handling 'Generate Resume' action."""
        parameters = {"test": "data"}
        llm_api_key = "test-key"
        
        handle_inquiries("Generate Resume", parameters, llm_api_key)
        
        mock_create_resume.assert_called_once_with(parameters, llm_api_key)
        mock_logger.info.assert_called_with("Crafting a standout professional resume...")

    @patch('main.create_resume_pdf_job_tailored')
    @patch('main.logger')
    def test_handle_inquiries_generate_tailored_resume(self, mock_logger, mock_create_tailored):
        """Test handling 'Generate Resume Tailored for Job Description' action."""
        parameters = {"test": "data"}
        llm_api_key = "test-key"
        
        handle_inquiries("Generate Resume Tailored for Job Description", parameters, llm_api_key)
        
        mock_create_tailored.assert_called_once_with(parameters, llm_api_key)
        mock_logger.info.assert_called_with("Customizing your resume to enhance your job application...")

    @patch('main.create_cover_letter')
    @patch('main.logger')
    def test_handle_inquiries_generate_cover_letter(self, mock_logger, mock_create_cover):
        """Test handling 'Generate Tailored Cover Letter for Job Description' action."""
        parameters = {"test": "data"}
        llm_api_key = "test-key"
        
        handle_inquiries("Generate Tailored Cover Letter for Job Description", parameters, llm_api_key)
        
        mock_create_cover.assert_called_once_with(parameters, llm_api_key)
        mock_logger.info.assert_called_with("Designing a personalized cover letter to enhance your job application...")

    @patch('main.logger')
    def test_handle_inquiries_no_action(self, mock_logger):
        """Test handling when no action is selected."""
        handle_inquiries("", {}, "test-key")
        
        mock_logger.warning.assert_called_with("No actions selected. Nothing to execute.")

    @patch('main.create_resume_pdf')
    @patch('main.logger')
    def test_handle_inquiries_exception(self, mock_logger, mock_create_resume):
        """Test handling when function raises exception."""
        mock_create_resume.side_effect = Exception("Test error")
        
        with pytest.raises(Exception):
            handle_inquiries("Generate Resume", {}, "test-key")
        
        mock_logger.exception.assert_called()


class TestCreateResumePdf:
    """Tests for create_resume_pdf function."""

    def setup_method(self):
        """Set up test data."""
        self.mock_parameters = {
            "uploads": {"plainTextResume": Path("/test/resume.yaml")},
            "outputFileDirectory": Path("/test/output")
        }
        self.mock_llm_key = "test-api-key"
        self.mock_resume_content = "Test resume content"

    @patch('main.open')
    @patch('main.StyleManager')
    @patch('main.ResumeGenerator')
    @patch('main.Resume')
    @patch('main.init_browser')
    @patch('main.ResumeFacade')
    @patch('main.base64.b64decode')
    @patch('main.logger')
    def test_create_resume_pdf_success(self, mock_logger, mock_b64decode, mock_facade_class, 
                                     mock_init_browser, mock_resume_class, mock_generator_class,
                                     mock_style_manager_class, mock_open):
        """Test successful resume PDF creation."""
        # Setup mocks
        mock_open.return_value.__enter__.return_value.read.return_value = self.mock_resume_content
        mock_style_manager = Mock()
        mock_style_manager.get_styles.return_value = {}
        mock_style_manager_class.return_value = mock_style_manager
        
        mock_facade = Mock()
        mock_facade.create_resume_pdf.return_value = "base64-encoded-data"
        mock_facade_class.return_value = mock_facade
        
        mock_b64decode.return_value = b"PDF content"
        mock_driver = Mock()
        mock_init_browser.return_value = mock_driver
        
        # Create output directory
        output_dir = Path(self.mock_parameters["outputFileDirectory"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        create_resume_pdf(self.mock_parameters, self.mock_llm_key)
        
        # Verify calls
        mock_facade.set_driver.assert_called_once_with(mock_driver)
        mock_facade.create_resume_pdf.assert_called_once()
        mock_logger.info.assert_called()

    @patch('main.open')
    @patch('main.logger')
    def test_create_resume_pdf_file_read_error(self, mock_logger, mock_open):
        """Test resume PDF creation when file read fails."""
        mock_open.side_effect = FileNotFoundError("File not found")
        
        with pytest.raises(FileNotFoundError):
            create_resume_pdf(self.mock_parameters, self.mock_llm_key)

    @patch('main.open')
    @patch('main.StyleManager')
    @patch('main.ResumeGenerator')
    @patch('main.Resume')
    @patch('main.init_browser')
    @patch('main.ResumeFacade')
    @patch('main.base64.b64decode')
    @patch('main.logger')
    def test_create_resume_pdf_base64_decode_error(self, mock_logger, mock_b64decode, mock_facade_class,
                                                 mock_init_browser, mock_resume_class, mock_generator_class,
                                                 mock_style_manager_class, mock_open):
        """Test resume PDF creation when base64 decode fails."""
        mock_open.return_value.__enter__.return_value.read.return_value = self.mock_resume_content
        mock_style_manager = Mock()
        mock_style_manager.get_styles.return_value = {}
        mock_style_manager_class.return_value = mock_style_manager
        
        mock_facade = Mock()
        mock_facade.create_resume_pdf.return_value = "invalid-base64"
        mock_facade_class.return_value = mock_facade
        
        mock_b64decode.side_effect = base64.binascii.Error("Invalid base64")
        
        with pytest.raises(base64.binascii.Error):
            create_resume_pdf(self.mock_parameters, self.mock_llm_key)
        
        mock_logger.error.assert_called()


class TestCreateResumePdfJobTailored:
    """Tests for create_resume_pdf_job_tailored function."""

    def setup_method(self):
        """Set up test data."""
        self.mock_parameters = {
            "uploads": {"plainTextResume": Path("/test/resume.yaml")},
            "outputFileDirectory": Path("/test/output")
        }
        self.mock_llm_key = "test-api-key"

    @patch('main.inquirer.prompt')
    @patch('main.open')
    @patch('main.StyleManager')
    @patch('main.ResumeGenerator')
    @patch('main.Resume')
    @patch('main.init_browser')
    @patch('main.ResumeFacade')
    @patch('main.base64.b64decode')
    @patch('main.logger')
    def test_create_resume_pdf_job_tailored_success(self, mock_logger, mock_b64decode, 
                                                   mock_facade_class, mock_init_browser,
                                                   mock_resume_class, mock_generator_class,
                                                   mock_style_manager_class, mock_open, mock_prompt):
        """Test successful job-tailored resume PDF creation."""
        # Setup mocks
        mock_open.return_value.__enter__.return_value.read.return_value = "resume content"
        mock_prompt.return_value = {"job_url": "https://example.com/job"}
        
        mock_style_manager = Mock()
        mock_style_manager.get_styles.return_value = {"Style1": ("file1.css", "author1")}
        mock_style_manager_class.return_value = mock_style_manager
        
        mock_facade = Mock()
        mock_facade.create_resume_pdf_job_tailored.return_value = ("base64-data", "suggested_name")
        mock_facade_class.return_value = mock_facade
        
        mock_b64decode.return_value = b"PDF content"
        
        # Create output directory
        output_dir = Path(self.mock_parameters["outputFileDirectory"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        create_resume_pdf_job_tailored(self.mock_parameters, self.mock_llm_key)
        
        # Verify facade methods were called
        mock_facade.link_to_job.assert_called_once_with("https://example.com/job")
        mock_facade.create_resume_pdf_job_tailored.assert_called_once()


class TestCreateCoverLetter:
    """Tests for create_cover_letter function."""

    def setup_method(self):
        """Set up test data."""
        self.mock_parameters = {
            "uploads": {"plainTextResume": Path("/test/resume.yaml")},
            "outputFileDirectory": Path("/test/output")
        }
        self.mock_llm_key = "test-api-key"

    @patch('main.inquirer.prompt')
    @patch('main.open')
    @patch('main.StyleManager')
    @patch('main.ResumeGenerator')
    @patch('main.Resume')
    @patch('main.init_browser')
    @patch('main.ResumeFacade')
    @patch('main.base64.b64decode')
    @patch('main.logger')
    def test_create_cover_letter_success(self, mock_logger, mock_b64decode, mock_facade_class,
                                       mock_init_browser, mock_resume_class, mock_generator_class,
                                       mock_style_manager_class, mock_open, mock_prompt):
        """Test successful cover letter creation."""
        # Setup mocks
        mock_open.return_value.__enter__.return_value.read.return_value = "resume content"
        mock_prompt.return_value = {"job_url": "https://example.com/job"}
        
        mock_style_manager = Mock()
        mock_style_manager.get_styles.return_value = {}
        mock_style_manager_class.return_value = mock_style_manager
        
        mock_facade = Mock()
        mock_facade.create_cover_letter.return_value = ("base64-data", "company_name")
        mock_facade_class.return_value = mock_facade
        
        mock_b64decode.return_value = b"PDF content"
        
        # Create output directory
        output_dir = Path(self.mock_parameters["outputFileDirectory"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        create_cover_letter(self.mock_parameters, self.mock_llm_key)
        
        # Verify facade methods were called
        mock_facade.link_to_job.assert_called_once_with("https://example.com/job")
        mock_facade.create_cover_letter.assert_called_once()


class TestMainFunction:
    """Tests for main function."""

    @patch('main.FileManager.validate_data_folder')
    @patch('main.ConfigValidator.validate_config')
    @patch('main.ConfigValidator.validate_secrets')
    @patch('main.FileManager.get_uploads')
    @patch('main.prompt_user_action')
    @patch('main.handle_inquiries')
    @patch('main.logger')
    def test_main_success(self, mock_logger, mock_handle, mock_prompt, mock_uploads,
                         mock_validate_secrets, mock_validate_config, mock_validate_folder):
        """Test successful main function execution."""
        # Setup mocks
        mock_validate_folder.return_value = (
            Path("secrets.yaml"), Path("config.yaml"), 
            Path("resume.yaml"), Path("output")
        )
        mock_validate_config.return_value = {"remote": True}
        mock_validate_secrets.return_value = "api-key"
        mock_uploads.return_value = {"plainTextResume": Path("resume.yaml")}
        mock_prompt.return_value = "Generate Resume"
        
        main()
        
        # Verify all steps were called
        mock_validate_folder.assert_called_once()
        mock_validate_config.assert_called_once()
        mock_validate_secrets.assert_called_once()
        mock_uploads.assert_called_once()
        mock_prompt.assert_called_once()
        mock_handle.assert_called_once()

    @patch('main.FileManager.validate_data_folder')
    @patch('main.logger')
    def test_main_file_not_found_error(self, mock_logger, mock_validate_folder):
        """Test main function with FileNotFoundError."""
        mock_validate_folder.side_effect = FileNotFoundError("File not found")
        
        main()
        
        mock_logger.error.assert_called()

    @patch('main.FileManager.validate_data_folder')
    @patch('main.ConfigValidator.validate_config')
    @patch('main.logger')
    def test_main_config_error(self, mock_logger, mock_validate_config, mock_validate_folder):
        """Test main function with ConfigError."""
        from main import ConfigError
        mock_validate_folder.return_value = (
            Path("secrets.yaml"), Path("config.yaml"), 
            Path("resume.yaml"), Path("output")
        )
        mock_validate_config.side_effect = ConfigError("Invalid config")
        
        main()
        
        mock_logger.error.assert_called()

    @patch('main.FileManager.validate_data_folder')
    @patch('main.logger')
    def test_main_runtime_error(self, mock_logger, mock_validate_folder):
        """Test main function with RuntimeError."""
        mock_validate_folder.side_effect = RuntimeError("Runtime error")
        
        main()
        
        mock_logger.error.assert_called()
        mock_logger.debug.assert_called()

    @patch('main.FileManager.validate_data_folder')
    @patch('main.logger')
    def test_main_unexpected_error(self, mock_logger, mock_validate_folder):
        """Test main function with unexpected exception."""
        mock_validate_folder.side_effect = ValueError("Unexpected error")
        
        main()
        
        mock_logger.exception.assert_called()