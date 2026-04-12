"""
Unit test for the configuration.
"""

from src.models.configuration import Configuration
from src.models.drivers import Drivers
from tests.lib.test_suite import TestSuite


class ConfigurationTest(TestSuite):

    _EXPECTED_GROUPS = ["settings", "instruments", "measurements", "process", "graphs"]
    _configuration = Configuration()

    def _log_list(self, name, items):
        self.log.debug(f"{name}:")
        for item in items:
            self.log.debug(f"- {item}")

    def setup(self):
        Drivers.load()
        drivers = Drivers.get_drivers()
        self.fail_if(len(drivers) == 0, "No driver available, test cannot run")

    def test_default_config(self):
        groups = self._configuration.get_main_groups()
        self.log.debug(f"Main groups: {groups}")
        self.fail_if(sorted(list(groups)) != sorted(self._EXPECTED_GROUPS),
                     f"Invalid main groups. Expected: {self._EXPECTED_GROUPS}")
        for group in groups:
            sub_items = self._configuration.get_sub_items(group)
            self.log.debug(f"Sub items for group '{group}': {sub_items}")

    ###############
    # Instruments #
    ###############

    def test_add_instrument(self):
        drivers = Drivers.get_drivers()
        driver_id = drivers[0].id
        settings = {"ip": "1.2.3.4"}
        instruments = self._configuration.get_instruments()

        self._log_list("Instruments", instruments)
        self.fail_if(len(instruments) != 0, "There should be no instruments")

        self.log.debug("Add instrument")
        self._configuration.add_instrument("test instrument 1", driver_id, settings)
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)
        self.fail_if(len(instruments) != 1, "Instrument was not added")

        self.log.debug("Add instrument with same name")
        try:
            self._configuration.add_instrument("test instrument 1", driver_id, settings)
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "An instrument with this name already exists",
                         "Invalid exception message")
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)
        self.fail_if(len(instruments) != 1, "There should be one instrument")

    def test_edit_instrument(self):
        drivers = Drivers.get_drivers()
        driver_id = drivers[0].id
        settings = {"ip": "1.2.3.4"}
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)
        self.fail_if(len(instruments) != 1, "There should be one instrument")

        self.log.debug("Add another instrument")
        self._configuration.add_instrument("test instrument 2", driver_id, settings)
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)
        self.fail_if(len(instruments) != 2, "Instrument was not added")

        self.log.debug("Update instrument name")
        instrument = instruments[0]
        self._configuration.update_instrument(instrument["id"], "Test instrument 3",
                                              instrument["driver_id"], instrument["settings"])
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)

        self.log.debug("Update setting")
        instrument = instruments[0]
        settings = {"ip": "5.6.7.8"}
        self._configuration.update_instrument(instrument["id"], instrument["name"],
                                              instrument["driver_id"], settings)
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)

        self.log.debug("Update with an existing name")
        instrument = instruments[0]
        try:
            self._configuration.update_instrument(instrument["id"], instruments[1]["name"],
                                                instrument["driver_id"], instrument["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "An instrument with this name already exists",
                         "Invalid exception message")
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)

        self.log.debug("Update with an invallid ID")
        instrument = instruments[0]
        try:
            self._configuration.update_instrument("invalid ID", instrument["name"],
                                                instrument["driver_id"], instrument["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No instrument found for this ID",
                         "Invalid exception message")

    def test_delete_instrument(self):
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)
        n_instruments = len(instruments)
        self.fail_if(n_instruments < 1, "There should be at least one instrument")

        self.log.debug("Delete instrument")
        self._configuration.delete_instrument(instruments[0]["id"])
        instruments = self._configuration.get_instruments()
        self._log_list("Instruments", instruments)
        self.fail_if(len(instruments) != n_instruments - 1, "Instrument was not deleted")

        self.log.debug("Delete instrument with invalid ID")
        try:
            self._configuration.delete_instrument("invalid ID")
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No instrument found for this ID",
                         "Invalid exception message")

    ################
    # Measurements #
    ################

    def test_add_measurement(self):
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)
        self.fail_if(len(measurements) != 0, "There should be no measurements")

        self.log.debug("Add measurement")
        self._configuration.add_measurement("test measurement 1", "instr-1234", "ch-1",
                                            "V", 1.0, 0.0, {})
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)
        self.fail_if(len(measurements) != 1, "Measurement was not added")

        self.log.debug("Add measurement with same name")
        try:
            self._configuration.add_measurement("test measurement 1", "instr-1234", "ch-1",
                                                "V", 1.0, 0.0, {})
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A measurement with this name already exists",
                         "Invalid exception message")
        measurements = self._configuration.get_measurements()
        self.log.debug(f"Measurements: {measurements}")
        self.fail_if(len(measurements) != 1, "There should be one measurement")

    def test_edit_measurements(self):
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)
        self.fail_if(len(measurements) != 1, "There should be one measurement")

        self.log.debug("Add another measurement")
        self._configuration.add_measurement("test measurement 2", "instr-1234", "ch-2",
                                            "V", 1.0, 0.0, {})
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)
        self.fail_if(len(measurements) != 2, "Measurement was not added")

        self.log.debug("Update measurement name")
        measurement = measurements[0]
        self._configuration.update_measurement(measurement["id"], "Test measurement 3",
                                               measurement["instrument_id"],
                                               measurement["channel_id"], measurement["unit"],
                                               measurement["gain"], measurement["offset"],
                                               measurement["params"])
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)

        self.log.debug("Update with an existing name")
        measurement = measurements[0]
        try:
            self._configuration.update_measurement(measurement["id"], measurements[1]["name"],
                                                   measurement["instrument_id"],
                                                   measurement["channel_id"], measurement["unit"],
                                                   measurement["gain"], measurement["offset"],
                                                   measurement["params"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A measurement with this name already exists",
                         "Invalid exception message")
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)

        self.log.debug("Update with an invallid ID")
        measurement = measurements[0]
        try:
            self._configuration.update_measurement("invalid ID", measurement["name"],
                                                   measurement["instrument_id"],
                                                   measurement["channel_id"], measurement["unit"],
                                                   measurement["gain"], measurement["offset"],
                                                   measurement["params"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No measurement found for this ID",
                         "Invalid exception message")

    def test_delete_measurement(self):
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)
        n_measurements = len(measurements)
        self.fail_if(n_measurements < 1, "There should be at least one measurement")

        self.log.debug("Delete measurement")
        self._configuration.delete_measurement(measurements[0]["id"])
        measurements = self._configuration.get_measurements()
        self._log_list("Measurements", measurements)
        self.fail_if(len(measurements) != n_measurements - 1, "Measurement was not deleted")

        self.log.debug("Delete measurement with invalid ID")
        try:
            self._configuration.delete_measurement("invalid ID")
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "No measurement found for this ID",
                         "Invalid exception message")

    #################
    # Process steps #
    #################

    def test_add_process_step(self):
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != 0, "There should be no steps")

        self.log.debug("Add step")
        settings = {"time": 10}
        self._configuration.add_process_step("test step 1", "label 1", "ProcessStepWait", settings)
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != 1, "Step was not added")

        self.log.debug("Add step with same label")
        try:
            self._configuration.add_process_step("test step 1", "label 1",
                                                 "ProcessStepWait", settings)
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A step with this label already exists",
                         "Invalid exception message")
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != 1, "There should be one step")

        self.log.debug("Add another step")
        self._configuration.add_process_step("test step 3", "label 3", "ProcessStepWait", settings)
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != 2, "Step was not added")

        self.log.debug("Insert a step")
        self._configuration.add_process_step("test step 2", "label 2", "ProcessStepWait",
                                             settings, 1)
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != 3, "Step was not added")


    def test_edit_process_step(self):
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != 3, "There should be 3 steps")

        self.log.debug("Update label")
        step = steps[0]
        self._configuration.update_process_step(0, step["name"], "label 4", step["type"],
                                                step["settings"])
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)

        self.log.debug("Update step with same label")
        try:
            self._configuration.update_process_step(0, step["name"], "label 2", step["type"],
                                                    step["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A step with this label already exists",
                         "Invalid exception message")
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)

        self.log.debug("Update with an invalid index")
        try:
            self._configuration.update_process_step(len(steps), step["name"], "",
                                                    step["type"], step["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "The step index is invalid",
                         "Invalid exception message")

    def test_move_process_step(self):
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != 3, "There should be 3 steps")

        self.log.debug("Move first step up, should not be possible")
        org_step = self._configuration.get_process_step(0)
        self._configuration.move_process_step(0, -1)
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        new_step = self._configuration.get_process_step(0)
        self.fail_if(new_step != org_step, "Step is not supposed to move")

        self.log.debug("Move first step down")
        org_step0 = self._configuration.get_process_step(0)
        org_step1 = self._configuration.get_process_step(1)
        self._configuration.move_process_step(0, 1)
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        new_step0 = self._configuration.get_process_step(0)
        new_step1 = self._configuration.get_process_step(1)
        self.fail_if(new_step0 != org_step1, "Step did not move")
        self.fail_if(new_step1 != org_step0, "Step did not move")

        self.log.debug("Move last step down, should not be possible")
        org_step = self._configuration.get_process_step(2)
        self._configuration.move_process_step(2, 1)
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        new_step = self._configuration.get_process_step(2)
        self.fail_if(new_step != org_step, "Step is not supposed to move")

        self.log.debug("Move last step up")
        org_step2 = self._configuration.get_process_step(2)
        org_step1 = self._configuration.get_process_step(1)
        self._configuration.move_process_step(2, -1)
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        new_step2 = self._configuration.get_process_step(2)
        new_step1 = self._configuration.get_process_step(1)
        self.fail_if(new_step2 != org_step1, "Step did not move")
        self.fail_if(new_step1 != org_step2, "Step did not move")

    def test_delete_process_step(self):
        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        n_steps = len(steps)
        self.fail_if(n_steps < 2, "There should be at least two step")

        self.log.debug("Delete process step")
        self._configuration.delete_process_step(0)

        steps = self._configuration.get_process_steps()
        self._log_list("Steps", steps)
        self.fail_if(len(steps) != n_steps - 1, "Step was not deleted")

        self.log.debug("Delete step with invalid index")
        try:
            self._configuration.delete_process_step(len(steps))
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "The step index is invalid",
                         "Invalid exception message")

    ##########
    # Graphs #
    ##########

    def test_add_graph(self):
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != 0, "There should be no graphs")

        self.log.debug("Add graph")
        settings = {"log_scale": False}
        self._configuration.add_graph("graph 1", ["measuremnt-1"], settings)
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != 1, "Graph was not added")

        self.log.debug("Add graph with same name")
        try:
            self._configuration.add_graph("graph 1", ["measurement-2"], settings)
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A graph with this name already exists",
                         "Invalid exception message")
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != 1, "There should only be one graph")

    def test_edit_graph(self):
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != 1, "There should be one graph")

        self.log.debug("Add another graph")
        settings = {"log_scale": False}
        self._configuration.add_graph("graph 2", ["measuremnt-2"], settings)
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != 2, "Graph was not added")

        self.log.debug("Update graph name")
        graph = graphs[0]
        self._configuration.update_graph(0, "graph 3", graph["measurements"], graph["settings"])
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(graphs[0]["name"] != "graph 3", "Graph name was not updated")

        self.log.debug("Update graph name with an existing name")
        graph = graphs[0]
        try:
            self._configuration.update_graph(0, graphs[1]["name"], graph["measurements"],
                                             graph["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "A graph with this name already exists",
                         "Invalid exception message")
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)

        self.log.debug("Update with an invallid index")
        graph = graphs[0]
        try:
            self._configuration.update_graph(len(graphs), graph["name"], graph["measurements"],
                                             graph["settings"])
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "The graph index is invalid",
                         "Invalid exception message")

    def test_move_graph(self):
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != 2, "There should be 2 graphs")

        self.log.debug("Add another graph")
        settings = {"log_scale": False}
        self._configuration.add_graph("graph 1", ["measuremnt-3"], settings)
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != 3, "Graph was not added")

        self.log.debug("Move first graph up, should not be possible")
        org_graph = graphs[0]
        self._configuration.move_graph(0, -1)
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        new_graph = graphs[0]
        self.fail_if(new_graph != org_graph, "Graph is not supposed to move")

        self.log.debug("Move first graph down")
        org_graph0 = graphs[0]
        org_graph1 = graphs[1]
        self._configuration.move_graph(0, 1)
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        new_graph0 = graphs[0]
        new_graph1 = graphs[1]
        self.fail_if(new_graph0 != org_graph1, "Graph did not move")
        self.fail_if(new_graph1 != org_graph0, "Graph did not move")

        self.log.debug("Move last graph down, should not be possible")
        org_graph = graphs[2]
        self._configuration.move_graph(2, 1)
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        new_graph = graphs[2]
        self.fail_if(new_graph != org_graph, "Graph is not supposed to move")

        self.log.debug("Move last graph up")
        org_graph2 = graphs[2]
        org_graph1 = graphs[1]
        self._configuration.move_graph(2, -1)
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        new_graph2 = graphs[2]
        new_graph1 = graphs[1]
        self.fail_if(new_graph2 != org_graph1, "Graph did not move")
        self.fail_if(new_graph1 != org_graph2, "Graph did not move")

    def test_delete_graph(self):
        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        n_graphs = len(graphs)
        self.fail_if(n_graphs < 2, "There should be at least two graphs")

        self.log.debug("Delete graph")
        self._configuration.delete_graph(0)

        graphs = self._configuration.get_graphs()
        self._log_list("Graphs", graphs)
        self.fail_if(len(graphs) != n_graphs - 1, "Graph was not deleted")

        self.log.debug("Delete graph with invalid index")
        try:
            self._configuration.delete_graph(len(graphs))
            self.fail("Expected an exception, but was not raised")
        except Exception as e:
            self.log.debug("Exception was raised, as expected")
            self.log.debug(f"Message: {e}")
            self.fail_if(str(e) != "The graph index is invalid",
                         "Invalid exception message")


if __name__ == "__main__":

    ConfigurationTest().run()
