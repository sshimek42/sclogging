# tests/test_custom_logging_with_colorama.py

import unittest
from unittest.mock import patch

from src.sclogging.custom_logging_with_colorama import clear_logs, set_log_path


class TestClearLogs(unittest.TestCase):
    @patch("src.sclogging.custom_logging_with_colorama.os.listdir")
    @patch("src.sclogging.custom_logging_with_colorama.base_logger")
    def test_clear_logs_no_files(self, mock_logger, mock_listdir):
        mock_listdir.return_value = []
        clear_logs(force=True)
        mock_logger.warning.assert_called_once_with("No files to delete")

    @patch("src.sclogging.custom_logging_with_colorama.shutil.rmtree")
    @patch("src.sclogging.custom_logging_with_colorama.os.listdir")
    @patch("src.sclogging.custom_logging_with_colorama.set_log_path")
    @patch("src.sclogging.custom_logging_with_colorama.base_logger")
    def test_clear_logs_force_delete(
        self, mock_logger, mock_set_log_path, mock_listdir, mock_rmtree
    ):
        mock_listdir.return_value = ["log1.txt", "log2.txt"]
        clear_logs(force=True)
        mock_rmtree.assert_called_once()
        mock_set_log_path.assert_called_once_with(auto_create=True)
        mock_logger.info.assert_called_once_with("Log directory cleared")
        mock_logger.warning.assert_not_called()

    @patch("src.sclogging.custom_logging_with_colorama.py_option.inputYesNo")
    @patch("src.sclogging.custom_logging_with_colorama.shutil.rmtree")
    @patch("src.sclogging.custom_logging_with_colorama.os.listdir")
    @patch("src.sclogging.custom_logging_with_colorama.set_log_path")
    @patch("src.sclogging.custom_logging_with_colorama.base_logger")
    def test_clear_logs_prompt_confirm_delete(
        self, mock_logger, mock_set_log_path, mock_listdir, mock_rmtree, mock_inputYesNo
    ):
        mock_listdir.return_value = ["log1.txt", "log2.txt"]
        mock_inputYesNo.return_value = "yes"
        clear_logs(force=False)
        mock_rmtree.assert_called_once()
        mock_set_log_path.assert_called_once_with(auto_create=True)
        mock_logger.info.assert_called_once_with("Log directory cleared")
        mock_logger.warning.assert_not_called()

    @patch("src.sclogging.custom_logging_with_colorama.py_option.inputYesNo")
    @patch("src.sclogging.custom_logging_with_colorama.base_logger")
    @patch("src.sclogging.custom_logging_with_colorama.os.listdir")
    def test_clear_logs_prompt_cancel_delete(
        self, mock_listdir, mock_logger, mock_inputYesNo
    ):
        mock_listdir.return_value = ["log1.txt", "log2.txt"]
        mock_inputYesNo.return_value = "no"
        clear_logs(force=False)
        mock_logger.warning.assert_called_once_with("Delete cancelled")

    @patch("src.sclogging.custom_logging_with_colorama.shutil.rmtree")
    @patch("src.sclogging.custom_logging_with_colorama.os.listdir")
    @patch("src.sclogging.custom_logging_with_colorama.set_log_path")
    @patch("src.sclogging.custom_logging_with_colorama.base_logger")
    def test_clear_logs_error_handler(
        self, mock_logger, mock_set_log_path, mock_listdir, mock_rmtree
    ):
        mock_listdir.return_value = ["log1.txt", "log2.txt"]
        mock_rmtree.side_effect = OSError("Mock rmtree error")
        with self.assertRaises(OSError):
            clear_logs(force=True)
        mock_logger.error.assert_called()


if __name__ == "__main__":
    unittest.main()
