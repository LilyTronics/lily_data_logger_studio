"""
View for checking instruments.
"""

import wx

import src.views.gui_sizes as GuiSizes

from src.views.view_list_autosize import ListAutosize


class ViewDialogCheckInstruments(wx.Dialog):

    _COLOUR = {
        False: "#ff8000",
        True: "#00ff80"
    }

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, "Check instruments")

        self._lst_instruments = ListAutosize(self, wx.ID_ANY, wx.LC_VRULES | wx.LC_HRULES)
        self._lst_instruments.add_cols(
            ["Name", "Status"],
            [200, 300]
        )
        self._lst_instruments.id_map = {}

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._lst_instruments, 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        self.SetSizer(box)
        self.SetInitialSize((550, 300))
        self.CenterOnParent()

    ##########
    # Public #
    ##########

    def add_instruments(self, instruments):
        self._lst_instruments.DeleteAllItems()
        self._lst_instruments.id_map.clear()
        for instrument in sorted(instruments, key=lambda x: x["name"]):
            index = self._lst_instruments.InsertItem(self._lst_instruments.GetItemCount(),
                                                     instrument["name"])
            self._lst_instruments.id_map[instrument["id"]] = index
        self._lst_instruments.autosize()

    def update_instrument(self, instrument_id, result, message):
        index = self._lst_instruments.id_map.get(instrument_id, -1)
        if index >= 0:
            self._lst_instruments.SetItemBackgroundColour(index, self._COLOUR[result])
            self._lst_instruments.SetItem(index, 1, message)
        self._lst_instruments.autosize()
        self.Refresh()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
