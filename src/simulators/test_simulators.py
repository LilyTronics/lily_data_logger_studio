"""
Test for testing the simulators.
"""

import time

from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from src.simulators.udp_client import UdpClient


def test_simulators():
    print("Start threads the first time")
    start_simulators()
    print("Start threads the second time time")
    start_simulators()

    try:
        print("Connect to temperature chamber")
        tc = UdpClient(SimulatorSettings.TemperatureChamber.IP,
                    SimulatorSettings.TemperatureChamber.PORT,
                    SimulatorSettings.TemperatureChamber.RX_TIME_OUT)
        print("ID  :", tc.send_command("id?"))
        print("Temp:", tc.send_command("temp?"))
        print("Set temperature to 30")
        print("Set :", tc.send_command("temp=30"))
        while True:
            t = float(tc.send_command("temp?"))
            print("Temp:", t)
            if 29.5 < t < 30.5:
                break
            time.sleep(1)
        print("Temp:", tc.send_command("temp?"))

    except Exception as e:
        print(f"ERROR: {e}")

    print("\nStop simulators")
    stop_simulators()


if __name__ == "__main__":

    test_simulators()
