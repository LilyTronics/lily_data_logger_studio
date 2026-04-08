"""
Build the documents
"""

import os
import shutil
import subprocess


def build_manual(doc_name):

    print(f"*** Build documentation {doc_name} ***")
    manual_dir = os.path.abspath(os.path.dirname(__file__))
    source_dir = os.path.join(manual_dir, doc_name)
    build_dir = os.path.join(manual_dir, "build", doc_name)

    print(f"Manuals: {manual_dir}")
    print(f"Source : {source_dir}")
    print(f"Output : {build_dir}")

    try:
        shutil.rmtree(build_dir, True)
        subprocess.run(
            [
                "sphinx-build",
                "-b", "html",
                "-c", manual_dir,
                source_dir,
                build_dir
            ],
            check=True,
            capture_output=True,
            text=True
        )
        print("Documentation built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building documentation: {e.stderr}")

if __name__ == "__main__":

    build_manual("main")
    build_manual("driver_test")
