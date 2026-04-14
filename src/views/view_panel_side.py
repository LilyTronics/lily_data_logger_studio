"""
View side panel.
"""

import wx

import src.models.images as Images

from src.models.time_converter import TimeConverter


class ViewPanelSide(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_configuration_tree(), 2, wx.EXPAND | wx.ALL, 1)
        box.Add(self._create_test_runs_tree(), 1, wx.EXPAND | wx.ALL, 1)

        self.SetSizer(box)

    ###########
    # Private #
    ###########

    def _create_configuration_tree(self):
        image_list = wx.ImageList(16, 16)
        image_list.Add(Images.settings_16.GetBitmap())
        image_list.Add(Images.instruments_16.GetBitmap())
        image_list.Add(Images.data_table_16.GetBitmap())
        image_list.Add(Images.process_16.GetBitmap())
        image_list.Add(Images.graphs_16.GetBitmap())
        image_list.Add(Images.time_16.GetBitmap())
        image_list.Add(Images.switch_16.GetBitmap())
        image_list.Add(Images.instrument_16.GetBitmap())
        image_list.Add(Images.measurement_16.GetBitmap())
        image_list.Add(Images.step_16.GetBitmap())
        image_list.Add(Images.graph_16.GetBitmap())
        image_list.Add(Images.configuration_16.GetBitmap())

        self._config_tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_HAS_BUTTONS)
        self._config_tree.AssignImageList(image_list)
        self._config_tree.AddRoot("Configuration:", image=11)
        return self._config_tree

    def _create_test_runs_tree(self):
        image_list = wx.ImageList(16, 16)
        image_list.Add(Images.configuration_16.GetBitmap())
        image_list.Add(Images.start_16.GetBitmap())
        image_list.Add(Images.time_16.GetBitmap())
        image_list.Add(Images.graph_16.GetBitmap())

        self._test_runs_tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_HAS_BUTTONS)
        self._test_runs_tree.AssignImageList(image_list)
        self._test_runs_tree.AddRoot("Test runs:", image=0)
        return self._test_runs_tree

    ##########
    # Public #
    ##########

    def update_configuration(self, configuration):
        root = self._config_tree.GetRootItem()
        self._config_tree.DeleteChildren(root)
        image_index = 0
        for i, main_group in enumerate(configuration.get_main_groups()):
            main_item = self._config_tree.AppendItem(root, main_group, image=i)
            sub_items = configuration.get_sub_items(main_group)
            for sub_item in sub_items:
                if main_group == "settings":
                    if "time" in sub_item:
                        image_index = 5
                    else:
                        image_index = 6
                elif main_group == "instruments":
                    image_index = 7
                elif main_group == "measurements":
                    image_index = 8
                elif main_group == "process":
                    image_index = 9
                elif main_group == "graphs":
                    image_index = 10
                self._config_tree.AppendItem(main_item, sub_item, image_index)
        self._config_tree.ExpandAll()

    def update_test_runs(self, test_runs):
        root = self._test_runs_tree.GetRootItem()
        self._test_runs_tree.DeleteChildren(root)
        for test_run in test_runs:
            if len(test_run["timestamps"]) > 0:
                timestamps = test_run["timestamps"]
                timestamp = TimeConverter.get_time_string(timestamps[0])
                item = self._test_runs_tree.AppendItem(root, str(timestamp), image=1)
                duration = TimeConverter.create_duration_time_string(timestamps[-1] - timestamps[0])
                self._config_tree.AppendItem(item, f"duration: {duration}", 2)
                self._config_tree.AppendItem(item, f"samples: {len(timestamps)}", 3)

        self._test_runs_tree.ExpandAll()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.load_test_configuration = True

    run_data_logger(TestOptions)
