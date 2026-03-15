"""
Dialog views.
"""

import wx


class ViewDialogs:

    @staticmethod
    def show_message(parent, message, title, icon=wx.ICON_INFORMATION, check_box_text=""):
        ret_value = None
        dlg = wx.RichMessageDialog(parent, message, title, wx.OK | icon)
        if check_box_text != "":
            dlg.ShowCheckBox(check_box_text)
        dlg.ShowModal()
        if check_box_text != "":
            ret_value = dlg.IsCheckBoxChecked()
        dlg.Destroy()
        return ret_value

    @staticmethod
    def show_confirm(parent, message, title, buttons=wx.YES | wx.NO):
        dlg = wx.RichMessageDialog(parent, message, title, buttons | wx.ICON_QUESTION)
        button = dlg.ShowModal()
        dlg.Destroy()
        return button

    @staticmethod
    def show_open_file(parent, message, default_folder="", default_file="",
                       file_filter="All files|*.*"):
        selected_file = None
        dlg = wx.FileDialog(parent, message, default_folder, default_file, file_filter,
                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            selected_file = dlg.GetPath()
        dlg.Destroy()
        return selected_file

    @staticmethod
    def show_save_file(parent, message, default_folder="", default_file="",
                       file_filter="All files|*.*"):
        selected_file = None
        dlg = wx.FileDialog(parent, message, default_folder, default_file, file_filter,
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            selected_file = dlg.GetPath()
        dlg.Destroy()
        return selected_file


if __name__ == "__main__":

    app = wx.App(redirect=False)

    filename = ViewDialogs.show_save_file(None, "Save file")
    print(ViewDialogs.show_message(None, f"Save to: {filename}", "Test",
                                   check_box_text="Don't show again"))
    filename = ViewDialogs.show_open_file(None, "Open file")
    ViewDialogs.show_confirm(None, f"Did you just opened: {filename}?", "Test")

    app.MainLoop()
