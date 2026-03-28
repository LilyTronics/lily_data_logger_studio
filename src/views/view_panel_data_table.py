"""
View for the data table.
"""

import wx.grid


class ViewPanelDataTable(wx.Panel):

    _HEADER_HEIGHT = 40
    _TIME_COL_WIDTH = 100
    _COL_EXTRA_WIDTH = 8

    def __init__(self, parent):
        super().__init__(parent)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_data_table(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(box)

    ###########
    # Private #
    ###########

    def _create_data_table(self):
        self._data_table = wx.grid.Grid(self, wx.ID_ANY)
        self._data_table.CreateGrid(0, 1)
        self._data_table.SetColLabelValue(0, "Time\n[s]")
        self._data_table.SetColLabelSize(self._HEADER_HEIGHT)
        self._data_table.SetColSize(0, self._TIME_COL_WIDTH)
        self._data_table.EnableEditing(False)
        self._data_table.EnableDragRowSize(False)
        self._data_table.EnableDragColMove(False)
        self._data_table.EnableDragColSize(False)
        return self._data_table

    def _auto_size_columns(self):
        for col in range(self._data_table.GetNumberCols()):
            # Time column is fixed
            if col == 0:
                continue
            self._data_table.AutoSizeColumn(col)
            size = self._data_table.GetColSize(col) + self._COL_EXTRA_WIDTH
            self._data_table.SetColSize(col, size)

    ##########
    # Public #
    ##########

    def update(self, configuration):
        measurements = configuration.get_measurements()
        measurements.sort(key=lambda x: x["name"])
        if self._data_table.GetNumberCols() > 1:
            self._data_table.DeleteCols(1, self._data_table.GetNumberCols() - 1)
        if self._data_table.GetNumberRows() > 0:
            self._data_table.DeleteRows(0, self._data_table.GetNumberRows())
        for i, measurement in enumerate(measurements):
            label = f"{measurement["name"]}\n[{measurement["unit"]}]"
            self._data_table.AppendCols(1)
            self._data_table.SetColLabelValue(i + 1, label)
        self._auto_size_columns()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
