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
            "run_id TEXT NOT NULL, "
            "measurement_id TEXT NOT NULL, "
            "name TEXT NOT NULL, "
            "unit TEXT NOT NULL"
            ")"
        ),
        (
            "CREATE TABLE IF NOT EXISTS samples ("
            "row_index INTEGER PRIMARY KEY AUTOINCREMENT, "
            "run_id TEXT NOT NULL, "
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
    def _insert_measurement(cls, conn, run_id, measurement_id, item_name, item_unit):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO measurements (run_id, measurement_id, name, unit) VALUES (?, ?, ?, ?)",
                (run_id, measurement_id, item_name, item_unit)
            )
        finally:
            cursor.close()

    @classmethod
    def _insert_samples(cls, conn, samples):
        cursor = conn.cursor()
        try:
            cursor.executemany(
                "INSERT INTO samples (run_id, measurement_id, timestamp, value) "
                "VALUES (?, ?, ?, ?)",
                samples
            )
        finally:
            cursor.close()

    @classmethod
    def _get_run_ids(cls, conn):
        results = []
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT run_id FROM measurements GROUP BY run_id")
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
        finally:
            cursor.close()
        return results

    @classmethod
    def _get_measurements(cls, conn, run_id):
        results = []
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM measurements WHERE run_id = ?",
                (run_id,)
            )
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
        finally:
            cursor.close()
        return results

    @classmethod
    def _get_samples(cls, conn, run_id, measurement_id):
        results = []
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM samples WHERE run_id = ? AND measurement_id = ?",
                (run_id, measurement_id,)
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
    def export_test_runs(cls, data_filename, test_runs):
        if os.path.isfile(data_filename):
            os.remove(data_filename)
        conn = sqlite3.connect(data_filename)
        try:
            cls._create_tables(conn)
            conn.commit()
            for test_run in test_runs:
                timestamps = test_run["timestamps"]
                for measurement in test_run["measurements"]:
                    cls._insert_measurement(conn, test_run["id"], measurement["id"],
                                            measurement["name"], measurement["unit"])
                    conn.commit()
                    samples = []
                    for i, value in enumerate(measurement["values"]):
                        # Order: (run_id, measurement_id, timestamp, value)
                        samples.append((test_run["id"], measurement["id"], timestamps[i], value))
                    cls._insert_samples(conn, samples)
                    conn.commit()
        finally:
            conn.close()

    @classmethod
    def import_test_runs(cls, data_filename):
        test_runs = []
        conn = sqlite3.connect(data_filename)
        conn.row_factory = sqlite3.Row
        try:
            test_run_ids = cls._get_run_ids(conn)
            for test_run_id in test_run_ids:
                timestamps = set()
                test_run = {
                    "id": "",
                    "timestamps": [],
                    "measurements": []
                }
                measurements = cls._get_measurements(conn, test_run_id["run_id"])
                for measurement in measurements:
                    data = {
                        "id": measurement["measurement_id"],
                        "name": measurement["name"],
                        "unit": measurement["unit"],
                        "values": []
                    }
                    samples = cls._get_samples(conn, test_run_id["run_id"],
                                               measurement["measurement_id"])
                    for sample in samples:
                        timestamps.add(sample["timestamp"])
                        data["values"].append(sample["value"])
                    test_run["measurements"].append(data)
                test_run["timestamps"] = sorted(timestamps)
                test_runs.append(test_run)
        finally:
            conn.close()
        return test_runs


if __name__ == "__main__":

    from tests.unit_tests.model_tests.test_runs_test import TestRunsTest

    TestRunsTest().run(True)
