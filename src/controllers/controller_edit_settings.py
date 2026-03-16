"""
Controller for editing the settings.
"""

import wx

from src.views.view_edit_settings import ViewEditSettings
from src.views.view_dialogs import ViewDialogs


class ControllerEditSettings:

    def __init__(self, parent_view, configuration, logger):
        logger.info("Edit settings")
        settings = configuration.get_settings()
        logger.debug(f"Current settings: {settings}")
        dlg = ViewEditSettings(parent_view, settings)
        if dlg.ShowModal() == wx.ID_OK:
            try:
                settings = dlg.get_settings()
                logger.debug(f"New settings: {settings}")
                configuration.update_settings(settings)
            except Exception as e:
                logger.error(f"Error updating settings: {e}")
                ViewDialogs.show_message(parent_view, f"Error updating settings: {e}",
                                         "Update settings", wx.ICON_EXCLAMATION)
        dlg.Destroy()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_edit_settings = True

    run_data_logger(TestOptions)
