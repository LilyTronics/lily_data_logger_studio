"""
List with autosizing columns.
"""

import wx


class ListAutosize(wx.ListCtrl):

    _DEFAULT_STYLE = wx.LC_REPORT | wx.LC_SINGLE_SEL

    def __init__(self, parent, control_id=wx.ID_ANY, style=0):
        super().__init__(parent, control_id, style=self._DEFAULT_STYLE | style)
        self._min_col_widths = []

    def add_cols(self, col_names, min_col_widths):
        self._min_col_widths = min_col_widths
        for i, name in enumerate(col_names):
            self.InsertColumn(i, name, width=self._min_col_widths[i])
        self.autosize()

    def autosize(self):
        for i, min_width in enumerate(self._min_col_widths):
            widths = []
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            widths.append(self.GetColumnWidth(i))
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            widths.append(self.GetColumnWidth(i))
            self.SetColumnWidth(i, max(widths))
            if max(widths) < min_width:
                self.SetColumnWidth(i, min_width)


if __name__ == "__main__":

    app = wx.App(redirect=False)

    f = wx.Frame(None, title="List autosize test")
    lst = ListAutosize(f)

    lst.add_cols(
        ["col 1", "col with a long name", "column 2"],
        [50, 100, 80]
    )
    item = wx.ListItem()
    item.SetId(lst.GetItemCount())
    item.SetText("Some text 1")
    lst.InsertItem(item)
    lst.SetItem(0, 1, "Some text 2")
    lst.SetItem(0, 2, "Some very very very very long text")
    lst.autosize()

    f.Show()

    app.MainLoop()
