"""
Run all simulators.
"""

import time

from src.simulators.temperature_chamber import TemperatureChamber

_RUNNING_SIMULATORS = []
_AVAILABLE_SIMULATORS = [
    TemperatureChamber
]

def start_simulators():
    for sim_class in _AVAILABLE_SIMULATORS:
        # Check if a simulator is already running
        matches = list(filter(lambda x, cls=sim_class : isinstance(x, cls), _RUNNING_SIMULATORS))
        if len(matches) == 0:
            try:
                sim = sim_class()
                sim.start()
                t = 2
                while t > 0 and not sim.is_running():
                    time.sleep(0.1)
                    t -= 0.1
                if not sim.is_running():
                    raise Exception(f"Simulator {sim_class} is not running")
                _RUNNING_SIMULATORS.append(sim)
            except Exception as e:
                print(f"Could not start simulator {sim_class}\n{e}")
        else:
            print(f"Simulator {sim_class} is already running")

def stop_simulators():
    for sim in _RUNNING_SIMULATORS:
        try:
            sim.stop()
            t = 2
            while t > 0 and sim.is_running():
                time.sleep(0.1)
                t -= 0.1
            if sim.is_running():
                raise Exception(f"Simulator {sim} is still running")
        except Exception as e:
            print(f"Could not stop simulator {sim}\n{e}")

    del _RUNNING_SIMULATORS[:]


if __name__ == "__main__":

    from tests.unit_tests.simulator_tests.simulators_test import SimulatorsTest

    SimulatorsTest().run(True)
