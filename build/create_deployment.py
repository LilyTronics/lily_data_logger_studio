"""
Creates a deployment package.
"""

import os
import platform
import shutil
import zipfile
import PyInstaller.__main__
import src

import src.app_data as AppData
from manuals.build import build_manuals


def _clean_output_folder(output_folder):
    print("Clean output folder . . .")
    if os.path.isdir(output_folder):
        for item in os.listdir(output_folder):
            full_path = os.path.join(output_folder, item)
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
    else:
        os.makedirs(output_folder)


def _create_version_file(version_file, artifacts_path, app_name, exe_name):
    print("Create version file . . .")
    version_template = os.path.join(artifacts_path, "version.template")
    version_tuple = []
    # Version can contain 'rc1', 'beta1', ... Tuple can only contain integers
    for part in AppData.VERSION.split('.'):
        try:
            version_tuple.append(int(part))
        except (Exception, ):
            pass
    while len(version_tuple) < 4:
        version_tuple.append(0)
    with open(version_template, "r", encoding="utf-8") as fp:
        version_template = fp.read()
        version_template = version_template.replace("{app_name}", app_name)
        version_template = version_template.replace("{version_tuple}", str(version_tuple))
        version_template = version_template.replace("{version_string}", AppData.VERSION)
        version_template = version_template.replace("{exe_name}", exe_name)
        version_template = version_template.replace("{company_name}", AppData.COMPANY)

    with open(version_file, "w", encoding="utf-8") as fp:
        fp.write(version_template)

def _copy_driver_test(dist_path, app_path):
    source_path = os.path.join(dist_path, AppData.DRIVER_TEST_EXE_NAME)
    exe_sources = [
        # On windows
        os.path.join(source_path, f"{AppData.DRIVER_TEST_EXE_NAME}.exe"),
        # On Ubuntu
        os.path.join(source_path, f"{AppData.DRIVER_TEST_EXE_NAME}")
    ]
    for source in exe_sources:
        if os.path.isfile(source):
            target = os.path.join(app_path, os.path.basename(source))
            print(f"Copy: {source}")
            print(f"To  : {target}")
            shutil.copy2(source, target)

def _copy_drivers(app_path):
    print(f"Copy the drivers from: {AppData.INSTRUMENTS_PATH}")
    output_folder = os.path.join(app_path, "instruments")
    os.makedirs(output_folder)
    print(f"Output folder: {output_folder}")
    for current_path, sub_folders, filenames in os.walk(AppData.INSTRUMENTS_PATH):
        sub_folders.sort()
        for filename in filenames:
            # Skip certain files
            if "__pycache__" in current_path:
                continue
            full_path = os.path.join(current_path, filename)
            target = os.path.join(output_folder, full_path[len(AppData.INSTRUMENTS_PATH) + 1:])
            os.makedirs(os.path.dirname(target), exist_ok=True)
            print(f"Copy: {full_path}")
            print(f"To  : {target}")
            if filename.endswith(".py") and "_template" not in filename:
                # Copy Python files without the test code, the test code will not work
                with open(full_path, "r", encoding="utf-8") as fp:
                    lines = fp.readlines()
                # Remove test code
                output = ""
                with open(target, "w", encoding="utf-8") as fp:
                    for line in lines:
                        if "if __name__ == \"__main__\"" in line:
                            break
                        output += line
                    fp.write(f"{output.strip()}\n")
            else:
                # Just copy the file
                shutil.copy2(full_path, target)

def _copy_manuals(app_path):
    if not build_manuals():
        raise Exception("Error building manuals")

    print("Copy manuals . . .")
    source_folder = os.path.join(AppData.MANUALS_PATH, "build")
    output_folder = os.path.join(app_path, "manuals")
    os.makedirs(output_folder, exist_ok=True)
    shutil.copytree(source_folder, output_folder, dirs_exist_ok=True)

def _create_zip_file(dist_path, app_path):
    print("Create ZIP file for distribution . . .")
    print(platform.system())
    filename = f"{AppData.EXE_NAME}_{AppData.VERSION}_{platform.system()}.zip"
    zip_filename = os.path.join(dist_path, filename)
    with zipfile.ZipFile(zip_filename, "w") as zip_object:
        # Add dist files
        for current_folder, sub_folders, filenames in os.walk(str(app_path)):
            sub_folders.sort()
            for filename in filenames:
                full_path = os.path.join(current_folder, filename)
                target_name = full_path[len(app_path) + 1:]
                print(f"Add: {full_path} to zip as: {target_name}")
                zip_object.write(full_path, target_name)

def _build_executable(output_folder, dist_path, app_id, app_name, exe_name):
    version_file = os.path.join(output_folder, f"{app_id}.version")
    artifacts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "artifacts"))
    init_file = os.path.join(os.path.dirname(src.__file__), f"{app_id}.py")
    icon_file = os.path.join(artifacts_path, f"{app_id}.ico")
    work_path = os.path.join(output_folder, "work")

    horizontal_line = "=" * 120
    print(f"\n{horizontal_line}")
    print("Build settings:")
    print("Output folder   :", output_folder)
    print("Artifacts folder:", artifacts_path)
    print("Version file    :", version_file)
    print("Init file       :", init_file)
    print("Application icon:", icon_file)
    print("Dist folder     :", dist_path)

    print(f"{horizontal_line}\n")

    _create_version_file(version_file, artifacts_path, app_name, exe_name)

    PyInstaller.__main__.run([
        init_file,
        "--clean",
        "--onedir",
        "--noconsole",
        f"--name={exe_name}",
        f"--icon={icon_file}",
        f"--version-file={version_file}",
        "--contents=lib",
        f"--workpath={work_path}",
        f"--specpath={work_path}",
        f"--distpath={dist_path}",
        "--hidden-import=queue",
        "--hidden-import=uuid"
    ])

def create_deployment():

    output_path = os.path.join(os.path.dirname(__file__), "build_output")
    dist_path = os.path.join(output_path, "dist")
    app_path = os.path.join(dist_path, AppData.EXE_NAME)

    _clean_output_folder(output_path)

    _build_executable(output_path, dist_path, "main", AppData.APP_NAME, AppData.EXE_NAME)
    _build_executable(output_path, dist_path, "driver_test", AppData.DRIVER_TEST_APP_NAME,
                      AppData.DRIVER_TEST_EXE_NAME)

    _copy_driver_test(dist_path, app_path)
    _copy_drivers(app_path)
    _copy_manuals(app_path)
    _create_zip_file(dist_path, app_path)

    print("\nBuild done")


if __name__ == "__main__":

    create_deployment()
