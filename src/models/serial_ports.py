"""
Lists all the available serial ports on the system.
"""

import threading
import time
import re
import serial

from serial.tools.list_ports import comports


def get_available_serial_ports():
    ignore = ["bluetooth link"]
    ports = []
    threads = []
    lock = threading.RLock()

    serial_ports = [
        p.device
        for p in comports()
        if not any(q in (p.description or "").lower() for q in ignore)
    ]
    for port in serial_ports:
        t = threading.Thread(target=_check_serial_port, args=(lock, port, ports))
        t.daemon = True
        t.start()
        threads.append(t)

    while True in list(map(lambda x: x.is_alive(), threads)):
        time.sleep(0.01)

    return sorted(ports, key=lambda s: int(re.search(r'\d+$', s).group()))


def _check_serial_port(lock_object, port_name, port_list):
    try:
        p = serial.Serial(port_name)
        p.close()
        lock_object.acquire()
        try:
            port_list.append(port_name)
        finally:
            lock_object.release()
    except (Exception, ):
        pass


if __name__ == "__main__":

    from tests.unit_tests.model_tests.serial_port_test import SerialPortTest

    SerialPortTest().run()
