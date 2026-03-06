"""
Controller for the configuration.
"""

import wx

from src.models.configuration import Configuration
from src.views.view_dialogs import ViewDialogs


class ControllerConfiguration:

    @staticmethod
    def new(logger):
        logger.info("Create new configuration")
        return Configuration()

    @staticmethod
    def load(parent_view, configuration, logger):
        dlg_title = "Open configuration"
        filename = ViewDialogs.show_open_file(parent_view, dlg_title,
                                              file_filter="Configuration files (JSON)|*.json")
        if filename is not None:
            try:
                logger.info(f"Load configuration from: {filename}")
                configuration.load(filename)
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
                ViewDialogs.show_message(parent_view, f"Error loading configuration: {e}",
                                         dlg_title, wx.ICON_EXCLAMATION)

    @staticmethod
    def save(parent_view, configuration, logger):
        dlg_title = "Save configuration"
        filename = ViewDialogs.show_save_file(parent_view, dlg_title,
                                              file_filter="Configuration files (JSON)|*.json")
        if filename is not None:
            try:
                logger.info(f"Save configuration to: {filename}")
                configuration.save(filename)
            except Exception as e:
                logger.error(f"Error saving configuration: {e}")
                ViewDialogs.show_message(parent_view, f"Error saving configuration: {e}", dlg_title,
                                         wx.ICON_EXCLAMATION)


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
