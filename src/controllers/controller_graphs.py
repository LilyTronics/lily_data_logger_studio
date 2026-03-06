"""
Controller for the graphs.
"""

from src.views.view_graphs import ViewGraphs


class ControllerGraphs:

    def __init__(self, parent_view, configuration, logger):
        logger.info("Show graphs")
        parent_view.show_child_window(ViewGraphs)


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_graphs = True

    run_data_logger(TestOptions)
