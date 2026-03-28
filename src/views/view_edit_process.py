"""
View for the process.
"""

import wx

import src.models.id_manager as IdManager
import src.models.images as Images
import src.views.gui_sizes as GuiSizes

from src.views.view_list_autosize import ListAutosize
from src.views.view_step_panels import STEP_PANELS


class ViewEditProcess(wx.Dialog):

    _TITLE = "Process"
    _WINDOW_SIZE = (1000, 600)

    def __init__(self, parent):
        super().__init__(parent, title=self._TITLE)
        self._settings_panel = None

        icon = wx.Icon()
        icon.CopyFromBitmap(Images.process_24.GetBitmap())
        self.SetIcon(icon)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_list(), 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_controls(), 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_buttons(), 0, wx.ALIGN_RIGHT | wx.ALL, GuiSizes.BOX_SPACING)

        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def _create_list(self):
        self._lst_process = ListAutosize(self, IdManager.ID_PROCESS_LIST,
                                         wx.LC_HRULES | wx.LC_VRULES)
        self._lst_process.add_cols(
            ["#", "label", "name", "step", "settings"],
            [30, 100, 100, 100, 200]
        )
        btn_add = wx.Button(self, IdManager.ID_PROCESS_NEW, "New")
        btn_down = wx.Button(self, IdManager.ID_PROCESS_DOWN, "Down")
        btn_up = wx.Button(self, IdManager.ID_PROCESS_UP, "Up")
        btn_delete = wx.Button(self, IdManager.ID_PROCESS_DELETE, "Delete")

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(self._lst_process, (0, 0), (1, 6), wx.EXPAND)
        grid.Add(btn_add, (1, 0), wx.DefaultSpan)
        grid.Add(btn_down, (1, 1), wx.DefaultSpan)
        grid.Add(btn_up, (1, 2), wx.DefaultSpan)
        grid.Add(btn_delete, (1, 4), wx.DefaultSpan)
        grid.AddGrowableCol(5)
        grid.AddGrowableRow(0)

        return grid

    def _create_controls(self):
        # Placeholder for step settings
        self._settings_grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        self._settings_grid.Add(wx.Panel(self), (0, 0))

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self._create_general_controls(), 0, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._settings_grid, 1, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        return box

    def _create_general_controls(self):
        lbl_name = wx.StaticText(self, wx.ID_ANY, "Name:")
        self._txt_name = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_XLARGE)
        lbl_label = wx.StaticText(self, wx.ID_ANY, "Label:")
        self._txt_label = wx.TextCtrl(self, wx.ID_ANY, size=GuiSizes.TEXT_LARGE)
        lbl_step = wx.StaticText(self, wx.ID_ANY, "Step:")
        self._cmb_steps = wx.ComboBox(self, IdManager.ID_PROCESS_STEP,
                                      style=wx.CB_READONLY)

        lbl_new_step  = wx.StaticText(self, wx.ID_ANY, "New step:")
        lbl_insert = wx.StaticText(self, wx.ID_ANY, "Insert:")
        self._cmb_position = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_READONLY)

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_label, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_label, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_step, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_steps, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_new_step, (4, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_insert, (5, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_position, (5, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)

        return grid

    def _create_buttons(self):
        btn_save = wx.Button(self, IdManager.ID_PROCESS_SAVE, "Save")
        btn_cancel = wx.Button(self, IdManager.ID_PROCESS_CANCEL, "Cancel")
        btn_close = wx.Button(self, IdManager.ID_PROCESS_CLOSE, "Close")

        grid = wx.GridBagSizer(GuiSizes.GRID_SPACING, GuiSizes.GRID_SPACING)
        grid.Add(btn_save, (0, 0), wx.DefaultSpan)
        grid.Add(btn_cancel, (0, 1), wx.DefaultSpan)
        grid.Add(btn_close, (0, 2), wx.DefaultSpan)

        return grid

    ##########
    # Public #
    ##########

    def get_selected_index(self):
        return self._lst_process.GetFirstSelected()

    def set_step_names(self, step_names):
        self._cmb_steps.SetItems(step_names)
        self.Layout()

    def set_steps(self, steps, selected_index):
        self._lst_process.DeleteAllItems()
        positions = ["at the end"]
        for step in steps:
            index = self._lst_process.GetItemCount()
            positions.append(f"before step {index + 1}")
            self._lst_process.InsertItem(index, str(index + 1))
            self._lst_process.SetItem(index, 1, step["label"])
            self._lst_process.SetItem(index, 2, step["name"])
            self._lst_process.SetItem(index, 3, step["step_name"])
            # Build settings string
            settings = []
            for key, value in step.get("settings", {}).items():
                if key in ["instrument_id", "channel_id", "measurement_id"]:
                    continue
                settings.append(f"{key.replace("_", " ")}: {value}")
            self._lst_process.SetItem(index, 4, ", ".join(settings))
        self._lst_process.Select(selected_index)
        self._cmb_position.SetItems(positions)
        self._cmb_position.SetSelection(0)
        self._lst_process.autosize()

    def show_step_panel(self, step_name):
        matches = [p for p in STEP_PANELS if p.name == step_name]
        if self._settings_grid.IsColGrowable(0):
            self._settings_grid.RemoveGrowableCol(0)
        if self._settings_grid.IsRowGrowable(0):
            self._settings_grid.RemoveGrowableRow(0)
        self._settings_grid.Clear(True)
        self._settings_panel = None
        if len(matches) == 1:
            self._settings_panel = matches[0](self)
            self._settings_grid.Add(self._settings_panel, (0, 0), wx.DefaultSpan, wx.EXPAND)
            self._settings_grid.AddGrowableCol(0)
            self._settings_grid.AddGrowableRow(0)
        else:
            self._settings_grid.Add(wx.Panel(self), (0, 0))
        self.Layout()

    def update_settings(self, settings, clear_step_panel=False):
        if "name" in settings:
            self._txt_name.SetValue(settings["name"])
        if "label" in settings:
            self._txt_label.SetValue(settings["label"])
        if settings.get("step_name") in self._cmb_steps.GetItems():
            self._cmb_steps.SetValue(settings["step_name"])
            self.show_step_panel(settings["step_name"])
        if self._settings_panel is not None:
            self._settings_panel.update_settings(settings)
        if clear_step_panel:
            self._cmb_steps.SetSelection(wx.NOT_FOUND)
            self._cmb_position.SetSelection(0)
            self.show_step_panel("")
        self.Layout()

    def get_settings(self):
        return {
            "insert": self._cmb_position.GetSelection() - 1,
            "name": self._txt_name.GetValue().strip(),
            "label": self._txt_label.GetValue().strip(),
            "step_name": self._cmb_steps.GetValue(),
            "settings" : {} if self._settings_panel is None else self._settings_panel.get_settings()
        }


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.show_edit_process = True
    TestOptions.suppress_loading_drivers = True

    run_data_logger(TestOptions)
