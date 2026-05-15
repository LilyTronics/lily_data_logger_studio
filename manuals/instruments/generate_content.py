"""
Generate the content for the manual, based on the content of the instruments package.
"""

import inspect
import os

from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

import src.app_data as AppData

from src.models.drivers import Drivers


_THIS_FOLDER = os.path.dirname(__file__)
_SKIP_FILES = ["driver_base.py", "driver_channel.py", "driver_setting.py"]


def _generate_table():
    print("Generate instruments table")
    Drivers.load()
    drivers = Drivers.get_drivers()
    manufacturer_width = len("Manufacturer")
    model_width = len("Model")
    for d in drivers:
        manufacturer_width = max(manufacturer_width, len(d.manufacturer))
        model_width = max(model_width, len(d.model))
    description_width = 90 - manufacturer_width - model_width
    # Create header
    line = "=" * manufacturer_width + " "
    line += "=" * model_width + " "
    line += "=" * description_width + "\n"
    output = line
    output += "Manufacturer".ljust(manufacturer_width + 1)
    output += "Model".ljust(model_width + 1)
    output += "Description\n"
    output += line
    manufacturer = ""
    for d in drivers:
        if manufacturer != d.manufacturer:
            output += d.manufacturer.ljust(manufacturer_width + 1)
            manufacturer = d.manufacturer
        else:
            output += "\\".ljust(manufacturer_width + 1)
        output += d.model.ljust(model_width + 1)
        description = d.description
        while len(description) > description_width:
            i = description.rfind(" ", 0, description_width)
            if i == -1:
                break
            output += description[:i] + "\n\n"
            output += " " * (manufacturer_width + model_width + 2)
            description = description[i + 1:]
        output += description + "\n"
    output += line + "\n"
    with open(os.path.join(_THIS_FOLDER, "index.rst"), "w", encoding="utf-8") as fp:
        fp.write("Supported instruments\n")
        fp.write("=====================\n\n")
        fp.write("The table below lists all supported instrumnets.\n\n")
        fp.write(output)
        fp.write(".. toctree::\n")
        fp.write("    :maxdepth: 2\n")
        fp.write("    :caption: Contents:\n\n")
        fp.write("    instruments.rst\n")

def _generate_instruments_references():
    print("Generate instruments references")

    driver_files = []
    for current_folder, sub_folders, filenames in os.walk(AppData.DRIVERS_PATH):
        if "__pycache__" in current_folder:
            continue

        sub_folders.sort()
        driver_files.extend([
            os.path.join(current_folder, f) for f in filenames if (
                f.endswith(".py") and
                f != "__init__.py" and
                f not in _SKIP_FILES
            )
        ])

    instruments = []
    simulators = []
    for filename in driver_files:
        name = os.path.basename(filename).split(".")[0]
        spec = spec_from_file_location(name, str(filename))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        for cls_name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ == module.__name__:
                data = {
                    "filename": filename,
                    "class_name": cls_name,
                    "manufacturer": cls.manufacturer,
                    "model": cls.model
                }
                if "simulator" in filename:
                    simulators.append(data)
                else:
                    instruments.append(data)

    manufacturer = ""
    with open(os.path.join(_THIS_FOLDER, "instruments.rst"), "w", encoding="utf-8") as fp:
        fp.write("Instruments class reference\n")
        fp.write("===========================\n\n")
        fp.write("The following chapters list all instrument classes.\n\n")
        for instrument in instruments + simulators:
            rel_path = instrument["filename"][len(AppData.INSTRUMENTS_PATH) + 1:]
            rel_path = rel_path.replace("\\", "/")
            if manufacturer != instrument["manufacturer"]:
                manufacturer = instrument["manufacturer"]
                fp.write(f"{manufacturer}\n")
                fp.write("-" * len(manufacturer))
                fp.write("\n\n")
            fp.write(f"{instrument["model"]}\n")
            fp.write("^" * len(instrument["model"]))
            fp.write("\n\n")
            fp.write(f".. literalinclude:: ../../instruments/{rel_path}\n")
            fp.write(f"    :pyobject: {instrument["class_name"]}\n\n")

def generate():
    print("Generate content")
    _generate_table()
    _generate_instruments_references()


if __name__ == "__main__":

    generate()
