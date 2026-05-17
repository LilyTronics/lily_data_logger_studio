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
        self._parent_view = parent_view
        self._logger = logger
        self._selected_id = None

        self._dlg = ViewEditTestRuns(self._parent_view)
        self._dlg.update_test_runs(TestRuns.get_test_runs())

        self._dlg.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_activated,
                       id=IdManager.ID_TEST_RUNS_LIST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_update, id=IdManager.ID_TEST_RUNS_UPDATE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_TEST_RUNS_DELETE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_load, id=IdManager.ID_TEST_RUNS_LOAD)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_export, id=IdManager.ID_TEST_RUNS_EXPORT)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_import, id=IdManager.ID_TEST_RUNS_IMPORT)
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

    def _on_update(self, event):
        run_id = self._dlg.get_selected_test_run()
        if run_id is not None:
            name = self._dlg.get_name()
            if name != "":
                TestRuns.rename_test_run(run_id, name)
                self._dlg.update_test_runs(TestRuns.get_test_runs())
                self._selected_id = run_id
                self._dlg.show_test_run(TestRuns.get_test_run(self._selected_id))
        event.Skip()

    def _on_delete(self, event):
        run_id = self._dlg.get_selected_test_run()
        if run_id is not None:
            dlg_title = "Delete test run"
            btn = ViewDialogs.show_confirm(self._dlg,
                                           "Are you sure you want to delete this test run?",
                                           dlg_title)
            if btn == wx.ID_YES:
                try:
                    TestRuns.delete(run_id)
                    self._selected_id = None
                    self._dlg.update_test_runs(TestRuns.get_test_runs())
                except Exception as e:
                    self._logger.error(f"Error deleting test run: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error deleting test run: {e}",
                                            dlg_title, wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_load(self, event):
        run_id = self._dlg.get_selected_test_run()
        if run_id is not None:
            try:
                self._parent_view.update_test_run_data(TestRuns.get_test_run(run_id))
            except Exception as e:
                self._logger.error(f"Error loading test run: {e}")
                ViewDialogs.show_message(self._dlg, f"Error loading test run: {e}",
                                         "Load test run", wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_export(self, event):
        ids = self._dlg.get_checked_test_runs()
        if len(ids) > 0:
            test_runs = [TestRuns.get_test_run(x) for x in ids]
            if len(test_runs) > 0:
                dlg_title = "Export test runs"
                try:
                    filename = ViewDialogs.show_save_file(self._dlg, dlg_title, "", "",
                                                          "SQLite|*.sqlite|JSON|*.json|"
                                                          "CSV (comma separated)|*.csv|"
                                                          "TSV (tab separated|*.tsv")
                    if filename is not None:
                        TestRuns.export_test_runs(test_runs, filename)
                except Exception as e:
                    self._logger.error(f"Error exporting test runs: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error exporting test runs: {e}",
                                            dlg_title, wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_import(self, event):
        dlg_title = "Import test runs"
        try:
            filename = ViewDialogs.show_open_file(self._dlg, dlg_title, "", "",
                                                  "SQLite, JSON|*.sqlite;*.json")
            if filename is not None:
                TestRuns.import_test_runs(filename)
        except Exception as e:
            self._logger.error(f"Error importing test runs: {e}")
            ViewDialogs.show_message(self._dlg, f"Error importing test runs: {e}",
                                    dlg_title, wx.ICON_EXCLAMATION)
        self._dlg.update_test_runs(TestRuns.get_test_runs())
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
    TestOptions.show_edit_test_runs = True

    run_data_logger(TestOptions)
