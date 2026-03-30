"""
ID manager for the controls
"""

import wx


# Toolbar icons
ID_NEW_CONFIG = wx.NewIdRef()
ID_OPEN_CONFIG = wx.NewIdRef()
ID_SAVE_CONFIG = wx.NewIdRef()
ID_RELOAD_DRIVERS = wx.NewIdRef()
ID_SHOW_EDIT_SETTINGS = wx.NewIdRef()
ID_SHOW_EDIT_INSTRUMENTS = wx.NewIdRef()
ID_SHOW_EDIT_PROCESS = wx.NewIdRef()
ID_SHOW_EDIT_MEASUREMENTS = wx.NewIdRef()
ID_SHOW_EDIT_GRAPHS = wx.NewIdRef()
ID_START_LOGGER = wx.NewIdRef()
ID_STOP_LOGGER = wx.NewIdRef()
ID_RESTORE_LAYOUT = wx.NewIdRef()

# Edit instruments view
ID_INSTRUMENT_LIST = wx.NewIdRef()
ID_INSTRUMENT_DRIVER = wx.NewIdRef()
ID_INSTRUMENT_NEW = wx.NewIdRef()
ID_INSTRUMENT_DELETE = wx.NewIdRef()
ID_INSTRUMENT_TEST = wx.NewIdRef()
ID_INSTRUMENT_SAVE = wx.NewIdRef()
ID_INSTRUMENT_CANCEL = wx.NewIdRef()
ID_INSTRUMENT_CLOSE = wx.NewIdRef()

# Edit instruments view
ID_MEASUREMENT_LIST = wx.NewIdRef()
ID_MEASUREMENT_INSTRUMENT = wx.NewIdRef()
ID_MEASUREMENT_CHANNEL = wx.NewIdRef()
ID_MEASUREMENT_NEW = wx.NewIdRef()
ID_MEASUREMENT_DELETE = wx.NewIdRef()
ID_MEASUREMENT_TEST = wx.NewIdRef()
ID_MEASUREMENT_SAVE = wx.NewIdRef()
ID_MEASUREMENT_CANCEL = wx.NewIdRef()
ID_MEASUREMENT_CLOSE = wx.NewIdRef()

# Edit process view
ID_PROCESS_LIST = wx.NewIdRef()
ID_PROCESS_NEW = wx.NewIdRef()
ID_PROCESS_DOWN = wx.NewIdRef()
ID_PROCESS_UP = wx.NewIdRef()
ID_PROCESS_DELETE = wx.NewIdRef()
ID_PROCESS_STEP = wx.NewIdRef()
ID_PROCESS_SAVE = wx.NewIdRef()
ID_PROCESS_CANCEL = wx.NewIdRef()
ID_PROCESS_CLOSE = wx.NewIdRef()
ID_PROCESS_INSTRUMENTS = wx.NewIdRef()

# Edit graphs view
ID_GRAPH_LIST = wx.NewIdRef()
ID_GRAPH_NEW = wx.NewIdRef()
ID_GRAPH_DOWN = wx.NewIdRef()
ID_GRAPH_UP = wx.NewIdRef()
ID_GRAPH_DELETE = wx.NewIdRef()
ID_GRAPH_SAVE = wx.NewIdRef()
ID_GRAPH_CANCEL = wx.NewIdRef()
ID_GRAPH_CLOSE = wx.NewIdRef()


if __name__ == "__main__":

    from tests.unit_tests.model_tests.id_manager_test import IdManagerTest

    IdManagerTest().run(True)
