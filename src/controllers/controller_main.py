"""
Main controller.
"""

from src.views.view_main import MainView


class MainController:

    def __init__(self, title):
        self._child_windows = []

        self._view = MainView(title)
        self._view.Show()


if __name__ == "__main__":

    from src.main import run_data_logger

    run_data_logger()
