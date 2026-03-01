"""
Unit test for the ID managers.
"""

import wx

import src.models.id_manager as IdManager

from tests.lib.test_suite import TestSuite


class IdManagerTest(TestSuite):

    def test_ids(self):
        ids = [x for x in dir(IdManager) if x.startswith("ID_")]
        values = []
        n_errors = 0
        for id_name in ids:
            value = int(getattr(IdManager, id_name))
            self.log.debug(f"Value for {id_name:<20}: {value}")
            if value in values:
                self.log.error(f"The value {value} already exists")
                n_errors += 1
            if value < wx.ID_AUTO_LOWEST or value > wx.ID_AUTO_HIGHEST:
                self.log.error(f"The value {value} is out of range "
                               f"({wx.ID_AUTO_LOWEST} to {wx.ID_AUTO_HIGHEST})")
                n_errors += 1
            values.append(value)
        self.fail_if(n_errors > 0, "One or more values are in correct")


if __name__ == "__main__":

    IdManagerTest().run(True)
