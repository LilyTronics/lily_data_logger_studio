"""
Controller for editing the test runs.
"""

import wx

import src.models.id_manager as IdManager

from src.models.test_runs import TestRuns
# from src.views.view_dialogs import ViewDialogs
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
