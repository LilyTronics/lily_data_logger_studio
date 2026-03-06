"""
Controller for the data table.
"""

from src.views.view_data_table import ViewDataTable


class ControllerDataTable:

    def __init__(self, parent_view, configuration, logger):
        logger.info("Show data table")
        parent_view.show_child_window(ViewDataTable)


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_data_table = True

    run_data_logger(TestOptions)
