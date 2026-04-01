"""
View for the process.
"""

import wx

from src.models.process_steps import STEP_CLASSES
from src.views.view_list_autosize import ListAutosize


class ViewPanelProcess(wx.Panel):

    _ACTIVE_COLOR = "#99ccff"
    _DEFAULT_COLOR = "#ffffff"

    def __init__(self, parent):
        super().__init__(parent)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_process_list(), 1, wx.EXPAND)
        self.SetSizer(box)

    ###########
    # Private #
    ###########

    def _create_process_list(self):
        self._lst_process = ListAutosize(self, wx.ID_ANY,
                                         wx.LC_HRULES | wx.LC_VRULES)
        self._lst_process.add_cols(
            ["#", "Label", "Name", "Step", "Settings"],
            [30, 100, 100, 100, 200]
        )
        self._lst_process.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_select)

        return self._lst_process

    ##################
    # Event handlers #
    ##################

    def _on_select(self, event):
        # Preven selecting items
        self._lst_process.Select(-1, 0)
        event.Skip()

    ##########
    # Public #
    ##########

    def update(self, configuration):
        steps = configuration.get_process_steps()
        self._lst_process.DeleteAllItems()
        for step in steps:
            matches = [x for x in STEP_CLASSES if x.get_class_name() == step["type"]]
            step_name = "unknown" if len(matches) != 1 else matches[0].name
            index = self._lst_process.GetItemCount()
            self._lst_process.InsertItem(index, str(index + 1))
            self._lst_process.SetItem(index, 1, step["label"])
            self._lst_process.SetItem(index, 2, step["name"])
            self._lst_process.SetItem(index, 3, step_name)
            # Build settings string
            settings = []
            for key, value in step.get("settings", {}).items():
                if key in ["instrument_id", "channel_id", "measurement_id"]:
                    continue
                settings.append(f"{key.replace("_", " ")}: {value}")
            self._lst_process.SetItem(index, 4, ", ".join(settings))
        self._lst_process.autosize()

    def update_progress(self, step_index):
        for i in range(self._lst_process.GetItemCount()):
            if i == step_index - 1:
                self._lst_process.SetItemBackgroundColour(i, wx.Colour(self._ACTIVE_COLOR))
            else:
                self._lst_process.SetItemBackgroundColour(i, wx.Colour(self._DEFAULT_COLOR))

if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
