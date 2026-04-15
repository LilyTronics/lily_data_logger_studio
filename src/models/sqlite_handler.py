"""
Handles SQLite export and import.
"""

import os
import sqlite3


class SQLiteHandler:

    _TABLE_DEFS = [
        (
            "CREATE TABLE IF NOT EXISTS measurements ("
            "row_index INTEGER PRIMARY KEY AUTOINCREMENT, "
            "id TEXT NOT NULL, "
            "name TEXT NOT NULL, "
            "unit TEXT NOT NULL"
            ")"
        ),
        (
            "CREATE TABLE IF NOT EXISTS samples ("
            "row_index INTEGER PRIMARY KEY AUTOINCREMENT, "
            "measurement_id TEXT NOT NULL, "
            "timestamp INTEGER NOT NULL, "
            "value REAL"
            ")"
        )
    ]

    ###########
    # Private #
    ###########

    @classmethod
    def _create_tables(cls, conn):
        cursor = conn.cursor()
        try:
            for table_def in cls._TABLE_DEFS:
                cursor.execute(table_def)
        finally:
            cursor.close()

    @classmethod
    def _insert_item(cls, conn, item_id, item_name, item_unit):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO measurements (id, name, unit) VALUES (?, ?, ?)",
                (item_id, item_name, item_unit)
            )
        finally:
            cursor.close()

    @classmethod
    def _insert_measurement(cls, conn, measurement_id, timestamp, value):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO samples (measurement_id, timestamp, value) VALUES (?, ?, ?)",
                (measurement_id, timestamp, value)
            )
        finally:
            cursor.close()

    @classmethod
    def _get_measurements(cls, conn):
        results = []
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM measurements")
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
        finally:
            cursor.close()
        return results

    @classmethod
    def _get_samples(cls, conn, measurement_id):
        results = []
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM samples WHERE measurement_id = ?",
                (measurement_id,)
            )
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
        finally:
            cursor.close()
        return results

    ##########
    # Public #
    ##########

    @classmethod
    def export_test_run(cls, data_filename, test_run):
        if os.path.isfile(data_filename):
            os.remove(data_filename)
        conn = sqlite3.connect(data_filename)
        try:
            cls._create_tables(conn)
            conn.commit()
            timestamps = test_run["timestamps"]
            for measurement in test_run["measurements"]:
                cls._insert_item(conn, measurement["id"], measurement["name"], measurement["unit"])
                conn.commit()
                for i, value in enumerate(measurement["values"]):
                    cls._insert_measurement(conn, measurement["id"], timestamps[i], value)
                    conn.commit()
        finally:
            conn.close()

    @classmethod
    def import_test_run(cls, data_filename):
        test_run = {
            "id": "",
            "timestamps": [],
            "measurements": []
        }
        conn = sqlite3.connect(data_filename)
        conn.row_factory = sqlite3.Row
        timestamps = set()
        try:
            measurements = cls._get_measurements(conn)
            for measurement in measurements:
                data = {
                    "id": measurement["id"],
                    "name": measurement["name"],
                    "unit": measurement["unit"],
                    "values": []
                }
                samples = cls._get_samples(conn, measurement["id"])
                for sample in samples:
                    timestamps.add(sample["timestamp"])
                    data["values"].append(sample["value"])
                test_run["measurements"].append(data)
            test_run["timestamps"] = sorted(timestamps)
        finally:
            conn.close()
        return test_run


if __name__ == "__main__":

    from tests.unit_tests.model_tests.test_runs_test import TestRunsTest

    TestRunsTest().run(True)
