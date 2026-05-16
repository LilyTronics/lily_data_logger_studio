"""
Test the temperature chamber driver for the simulator.
"""

from src.models.drivers import Drivers
from src.simulators.run_simulators import start_simulators
from src.simulators.run_simulators import stop_simulators
from src.simulators.simulator_settings import SimulatorSettings
from tests.lib.test_suite import TestSuite


class DriverTemperatureChamberTest(TestSuite):

    driver = None
    async_response = [False]

    def _callback(self, *response):
        self.log.debug(f"Async response: {response}")
        self.async_response[0] = True
        self.fail_if(not isinstance(response[0], response[1]),
                     "The type is incorrect")

    def setup(self):
        self.log.debug("Start simulators")
        start_simulators()
        Drivers.load()
        driver_class = Drivers.get_driver("TemperatureChamber")
        self.fail_if(driver_class is None, "The driver is not found")
        self.driver = driver_class(SimulatorSettings.TemperatureChamber, "DPT")

    def teardown(self):
        self.log.debug("Stop simulators")
        stop_simulators()

    def test_driver_test(self):
        self.driver.test_driver()

    def test_get_id(self):
        self.log.debug("Get ID")
        response = self.driver.process_channel("get_id")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "Simulator Temperature Chamber", "The ID is not correct")

    def test_get_actual_temperature(self):
        self.log.debug("Get actual temperature")
        response = self.driver.process_channel("get_act_temp")
        self.log.debug(f"Response: {response}")
        self.fail_if(not isinstance(response, float), "The response is not a float")

    def test_temperature_setpoint(self):
        self.log.debug("Get temperature setpoint")
        set_point = self.driver.process_channel("get_temp_set")
        self.log.debug(f"Response: {set_point}")
        self.fail_if(not isinstance(set_point, float), "The response is not a float")
        set_point += 5
        response = self.driver.process_channel("set_temp_set", {"value": set_point})
        self.log.debug(f"Response: {response}")
        self.fail_if(response != "ok", "The response is not 'ok'")
        response = self.driver.process_channel("get_temp_set")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != set_point, "The setpoint was not updated correctly")

    def test_power_state(self):
        self.log.debug("Get power state")
        state = self.driver.process_channel("get_pwr_state")
        self.log.debug(f"Response: {state}")
        self.fail_if(not isinstance(state, int), "The response is not an int")
        state = 1 - state
        response = self.driver.process_channel("set_pwr_state", {"value": state})
        self.log.debug(f"Response: {response}")
        self.fail_if(response is not None, "The response is not None")
        response = self.driver.process_channel("get_pwr_state")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != state, "The power state was not updated correctly")

    def test_get_id_async(self):
        self.async_response[0] = False
        self.log.debug("Get ID")
        response = self.driver.process_channel("get_id", callback=self._callback,
                                               callback_params=str)
        self.fail_if(response is not None, f"No response expected, got: {response}")
        if not self.wait_for(self.async_response, True, 2, 0.1):
            self.fail("No async response received")

    def test_get_temperature_async(self):
        self.async_response[0] = False
        self.log.debug("Get ID")
        response = self.driver.process_channel("get_act_temp", callback=self._callback,
                                               callback_params=float)
        self.fail_if(response is not None, f"No response expected, got: {response}")
        if not self.wait_for(self.async_response, True, 2, 0.1):
            self.fail("No async response received")

    def test_custom_command_string(self):
        custom_command = {"command": "id?", "response type": "string"}
        self.log.debug("Process custom command")
        response = self.driver.process_channel("custom_command", custom_command)
        self.log.debug(f"Response: {response}")
        self.fail_if(not isinstance(response, str),
                     f"Response type string expected, got: {type(response)}")
        self.fail_if(response != "Simulator Temperature Chamber", "Invalid response")

    def test_custom_command_float(self):
        custom_command = {"command": "temp?", "response type": "float"}
        self.log.debug("Process custom command")
        response = self.driver.process_channel("custom_command", custom_command)
        self.log.debug(f"Response: {response}")
        self.fail_if(not isinstance(response, float),
                     f"Response type float expected, got: {type(response)}")

    def test_custom_command_int(self):
        custom_command = {"command": "pwr?", "response type": "int"}
        self.log.debug("Process custom command")
        response = self.driver.process_channel("custom_command", custom_command)
        self.log.debug(f"Response: {response}")
        self.fail_if(not isinstance(response, int),
                     f"Response type int expected, got: {type(response)}")

    def test_custom_command_none(self):
        custom_command = {"command": "pwr=0", "response type": "none"}
        self.log.debug("Process custom command")
        response = self.driver.process_channel("custom_command", custom_command)
        self.log.debug(f"Response: {response}")
        self.fail_if(response is not None,
                     f"Response None expected, got: {type(response)}")

    def test_custom_command_async(self):
        self.async_response[0] = False
        custom_command = {"command": "temp?", "response type": "float"}
        self.log.debug("Process custom command")
        response = self.driver.process_channel("custom_command", custom_command,
                                               callback=self._callback,
                                               callback_params=float)
        self.fail_if(response is not None, f"No response expected, got: {response}")
        if not self.wait_for(self.async_response, True, 2, 0.1):
            self._fail("No async response received")


if __name__ == "__main__":

    DriverTemperatureChamberTest().run()
