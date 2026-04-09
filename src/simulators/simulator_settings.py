"""
Container for simulator settings.
"""


class SimulatorSettings:

    TemperatureChamber = {
        "host": "localhost",
        "port": 51000
    }

    AnalogIo = {
        "host": "localhost",
        "port": 51100
    }

if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulators_test import SimulatorsTest

    SimulatorsTest().run(True)
