"""
Run all simulators.
"""

import threading
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

    _show_running_threads()


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
    _show_running_threads()


def _show_running_threads():
    print("Running threads:")
    for thread in threading.enumerate():
        print("-", thread.name)
    print("")


if __name__ == "__main__":

    from src.simulators.test_simulators import test_simulators

    test_simulators()
