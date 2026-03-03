"""
Dialog views.
"""

import wx


class ViewDialogs:

    @staticmethod
    def show_message(parent, message, title, icon=wx.ICON_INFORMATION):
        dlg = wx.MessageDialog(parent, message, title, wx.OK | icon)
        dlg.ShowModal()
        dlg.Destroy()

    @staticmethod
    def show_confirm(parent, message, title, buttons=wx.YES | wx.NO):
        dlg = wx.MessageDialog(parent, message, title, buttons | wx.ICON_QUESTION)
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
    ViewDialogs.show_message(None, f"Save to: {filename}", "Test")
    filename = ViewDialogs.show_open_file(None, "Open file")
    ViewDialogs.show_confirm(None, f"Did you just opened: {filename}?", "Test")

    app.MainLoop()
