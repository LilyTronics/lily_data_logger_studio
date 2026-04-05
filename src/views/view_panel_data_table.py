"""
View for the data table.
"""

import wx.grid

from src.models.time_converter import TimeConverter


class ViewPanelDataTable(wx.Panel):

    _HEADER_HEIGHT = 40
    _TIME_COL_WIDTH = 100
    _HEADER_WIDTH = 140
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
        self._data_table.SetRowLabelSize(self._HEADER_WIDTH)
        self._data_table.EnableEditing(False)
        self._data_table.EnableDragRowSize(False)
        self._data_table.EnableDragColMove(False)
        self._data_table.EnableDragColSize(False)
        self._auto_size_columns()
        return self._data_table

    def _auto_size_columns(self):
        for col in range(self._data_table.GetNumberCols()):
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

    def update_data(self, table_data):
        self._data_table.Freeze()
        self._data_table.ClearGrid()
        if self._data_table.GetNumberRows() > 0:
            self._data_table.DeleteRows(0, self._data_table.GetNumberRows())
        self._data_table.AppendRows(len(table_data["timestamps"]))
        start_time = 0
        for i, t in enumerate(table_data["timestamps"]):
            self._data_table.SetRowLabelValue(i, TimeConverter.get_time_string(t))
            if i == 0:
                start_time = t
            value = TimeConverter.create_duration_time_string(t - start_time)
            self._data_table.SetCellValue(i, 0, value)
            self._data_table.SetCellAlignment(i, 0, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        n_rows = self._data_table.GetNumberRows()
        if  n_rows > 0:
            for col in range(self._data_table.GetNumberCols()):
                label = self._data_table.GetColLabelValue(col)
                for name, values in table_data["measurements"].items():
                    if label.startswith(f"{name}\n"):
                        for row in range(n_rows):
                            self._data_table.SetCellValue(row, col, str(values[row]))
                            self._data_table.SetCellAlignment(row, col, wx.ALIGN_CENTER,
                                                              wx.ALIGN_CENTER)
        self._auto_size_columns()
        self._data_table.Thaw()
        self._data_table.MakeCellVisible(n_rows - 1, 0)


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
