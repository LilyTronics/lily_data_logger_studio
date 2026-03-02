"""
Container for simulator settings.
"""


class SimulatorSettings:

    class TemperatureChamber:
        IP = "localhost"
        PORT = 17000
        RX_TIME_OUT = 0.2


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulators_test import SimulatorsTest

    SimulatorsTest().run(True)
