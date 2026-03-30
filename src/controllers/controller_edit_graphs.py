"""
Controller for editing the graphs.
"""

import wx

import src.models.id_manager as IdManager

from src.views.view_dialogs import ViewDialogs
from src.views.view_edit_graphs import ViewEditGraphs


class ControllerEditGraphs:

    def __init__(self, parent_view, logger, configuration):
        self._logger = logger
        self._configuration = configuration
        self._logger.info("Edit graphs")
        self._selected_index = None

        self._dlg = ViewEditGraphs(parent_view)
        self._dlg.set_measurements(self._configuration.get_measurements())
        self._update_graphs()

        self._dlg.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_activated,
                       id=IdManager.ID_GRAPH_LIST)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_down_up, id=IdManager.ID_GRAPH_DOWN,
                       id2=IdManager.ID_GRAPH_UP)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_new, id=IdManager.ID_GRAPH_NEW)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_delete, id=IdManager.ID_GRAPH_DELETE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_save, id=IdManager.ID_GRAPH_SAVE)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_cancel, id=IdManager.ID_GRAPH_CANCEL)
        self._dlg.Bind(wx.EVT_BUTTON, self._on_close, id=IdManager.ID_GRAPH_CLOSE)

        self._dlg.ShowModal()
        self._dlg.Destroy()

    ###########
    # Private #
    ###########

    def _update_graphs(self, selected_index=-1):
        self._dlg.set_graphs(self._configuration.get_graphs(), selected_index)

    def _get_graph_from_view(self):
        settings = self._dlg.get_settings()
        if settings["name"] == "":
            raise Exception("The name cannot be empty")
        if len(settings["measurements"]) == 0:
            raise Exception("There must be one or more measurements")
        measurements = []
        for name in settings["measurements"]:
            measurement = self._configuration.get_measurement(name)
            if measurement is not None:
                measurements.append(measurement["id"])

        graph = self._configuration.get_new_graph()
        graph["name"] = settings["name"]
        graph["measurements"] = measurements
        graph["settings"] = settings["settings"]
        return graph

    def _show_graph_data(self, index):
        self._selected_index = None
        graphs = self._configuration.get_graphs()
        if 0 <= index  < len(graphs):
            graph = graphs[0]
            measurements = self._configuration.get_measurements()
            names = []
            for measurement_id in graph["measurements"]:
                matches = [x for x in measurements if x["id"] == measurement_id]
                if len(matches) == 1:
                    names.append(matches[0]["name"])
            graph["measurements"] = names
            self._dlg.update_settings(graph)
            self._selected_index = index


    ##################
    # Event handlers #
    ##################

    def _on_activated(self, event):
        self._show_graph_data(event.GetIndex())
        event.Skip()

    def _on_new(self, event):
        graph = self._configuration.get_new_graph()
        self._dlg.update_settings(graph)
        self._selected_index = None
        event.Skip()

    def _on_save(self, event):
        try:
            graph = self._get_graph_from_view()
            self._logger.debug(f"Save graph: {graph}")
            if self._selected_index is None:
                self._configuration.add_graph(graph["name"], graph["measurements"],
                                              graph["settings"])
                graphs = self._configuration.get_graphs()
                self._selected_index = len(graphs) - 1
            else:
                self._configuration.update_graph(self._selected_index, graph["name"],
                                                 graph["measurements"], graph["settings"])
        except Exception as e:
            self._logger.error(f"Error saving graph: {e}")
            ViewDialogs.show_message(self._dlg, f"Error saving graph: {e}",
                                     "Save graph", wx.ICON_EXCLAMATION)
            return
        self._update_graphs()
        event.Skip()

    def _on_down_up(self, event):
        index = self._dlg.get_selected_index()
        if index >= 0:
            btn_id = event.GetId()
            direction = 1 if btn_id == IdManager.ID_GRAPH_DOWN else -1
            self._configuration.move_graph(index, direction)
            self._update_graphs(index + direction)
        event.Skip()

    def _on_cancel(self, event):
        if self._selected_index is not None:
            self._show_graph_data(self._selected_index)
        event.Skip()

    def _on_delete(self, event):
        index = self._dlg.get_selected_index()
        if index >= 0:
            graphs = self._configuration.get_graphs()
            dlg_title = "Delete graph"
            btn = ViewDialogs.show_confirm(
                self._dlg,
                f"Are you sure you want to delete the graph '{graphs[index]["name"]}'?",
                dlg_title
            )
            if btn == wx.ID_YES:
                try:
                    self._configuration.delete_graph(index)
                    self._selected_index = None
                    self._update_graphs()
                except Exception as e:
                    self._logger.error(f"Error deleting graph: {e}")
                    ViewDialogs.show_message(self._dlg, f"Error deleting graph: {e}",
                                            dlg_title, wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_close(self, event):
        self._dlg.Close()
        event.Skip()


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.load_test_configuration = True
    TestOptions.log_to_stdout = True
    TestOptions.suppress_loading_drivers = True
    TestOptions.show_edit_graphs = True

    run_data_logger(TestOptions)
