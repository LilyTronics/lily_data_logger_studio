"""
Controller for editing the process.
"""

from src.views.view_process import ViewProcess


class ControllerProcess:

    def __init__(self, parent_view, configuration, logger):
        logger.info("Show process")
        parent_view.show_child_window(ViewProcess)


if __name__ == "__main__":

    from src.main import run_data_logger
    from src.models.test_options import TestOptions

    TestOptions.log_to_stdout = True
    TestOptions.show_view_process = True

    run_data_logger(TestOptions)
