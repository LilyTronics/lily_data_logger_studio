"""
Build the documents
"""

import os
import shutil
import subprocess


def build_manual(src_name, doc_name):

    print(f"*** Build documentation {doc_name} ***")
    manual_dir = os.path.abspath(os.path.dirname(__file__))
    source_dir = os.path.join(manual_dir, src_name)
    build_dir = os.path.join(manual_dir, "build", doc_name)

    print(f"Manuals: {manual_dir}")
    print(f"Source : {source_dir}")
    print(f"Output : {build_dir}")

    try:
        shutil.rmtree(build_dir, True)
        subprocess.run(
            [
                "sphinx-build",
                "-b", "singlehtml",
                "-c", manual_dir,
                source_dir,
                build_dir
            ],
            check=True,
            capture_output=True,
            text=True
        )
        # Remove files that are not needed
        shutil.rmtree(os.path.join(build_dir, ".doctrees"), True)
        os.remove(os.path.join(build_dir, ".buildinfo"))
        os.remove(os.path.join(build_dir, "objects.inv"))
        print("Documentation built successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building documentation: {e.stderr}")
    return False

def build_manuals():
    print("*** Build manuals ***")
    results = [
        build_manual("main", "Data Logger Studio"),
        build_manual("driver_dev", "Driver Development")
    ]
    print(f"Build results: {results}")
    return False not in results


if __name__ == "__main__":

    print(build_manuals())
