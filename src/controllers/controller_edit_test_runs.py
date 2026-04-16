"""
Controller for editing the test runs.
"""

import wx

import src.models.id_manager as IdManager

from src.models.test_runs import TestRuns
from src.views.view_dialogs import ViewDialogs
from src.views.view_edit_test_runs import ViewEditTestRuns


class ControllerEditTestRuns:

    def __init__(self, parent_view, logger):
        self._logger = logger
        self._logger.info("Edit test runs")
        self._selected_id = None

        self._dlg = ViewEditTestRuns(parent_view)
        self._dlg.update_test_runs(TestRuns.get_test_runs())

        self._dlg.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_activated,
                       id=IdManager.ID_TEST_RUNS_LIST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_TEST_RUNS_DELETE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_export, id=IdManager.ID_TEST_RUNS_EXPORT)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_close, id=IdManager.ID_TEST_RUNS_CLOSE)

        self._dlg.ShowModal()
        self._dlg.Destroy()

    ###########
    # Private #
    ###########

    ##################
    # Event handlers #
    ##################

    def _on_activated(self, event):
        run_id = event.GetEventObject().id_map.get(event.GetIndex(), None)
        if run_id is not None:
            self._selected_id = run_id
            self._dlg.show_test_run(TestRuns.get_test_run(self._selected_id))
        event.Skip()

    def _on_delete(self, event):
        if self._selected_id is not None:
            dlg_title = "Delete test run"
            btn = ViewDialogs.show_confirm(self._dlg,
                                           "Are you sure you want to delete this test run?",
                                           dlg_title)
            if btn == wx.ID_YES:
                try:
                    TestRuns.delete(self._selected_id)
                    self._selected_id = None
                    self._dlg.update_test_runs(TestRuns.get_test_runs())
                except Exception as e:
                    self._logger.error(f"Error deleting test run: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error deleting test run: {e}",
                                            dlg_title, wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_export(self, event):
        ids = self._dlg.get_checked_test_runs()
        if len(ids) > 0:
            test_runs = [TestRuns.get_test_run(x) for x in ids]
            if len(test_runs) > 0:
                dlg_title = "Export test runs"
                try:
                    filename = ViewDialogs.show_save_file(self._dlg, dlg_title, "", "",
                                                        "SQLite|*.sqlite|JSON|*.json|CSV|*.csv")
                    if filename is not None:
                        TestRuns.export_test_runs(test_runs, filename)
                except Exception as e:
                    self._logger.error(f"Error exporting test runs: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error exporting test runs: {e}",
                                            dlg_title, wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_close(self, event):
        self._dlg.Close()
        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
