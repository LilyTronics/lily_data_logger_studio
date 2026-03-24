"""
View for the configuration.
"""

import wx

import src.models.images as Images


class ViewPanelConfiguration(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_tree(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(box)

    ###########
    # Private #
    ###########

    def _create_tree(self):
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

        self._tree = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_HAS_BUTTONS)
        self._tree.AssignImageList(image_list)
        self._tree.AddRoot("Configuration:", image=11)
        return self._tree

    ##########
    # Public #
    ##########

    def update_tree(self, configuration):
        root = self._tree.GetRootItem()
        self._tree.DeleteChildren(root)
        image_index = 0
        for i, main_group in enumerate(configuration.get_main_groups()):
            main_item = self._tree.AppendItem(root, main_group, image=i)
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
                self._tree.AppendItem(main_item, sub_item, image_index)
        self._tree.ExpandAll()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True

    run_data_logger(TestOptions)
