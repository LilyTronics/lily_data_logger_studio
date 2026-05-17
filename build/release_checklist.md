# Release checklist

## Pre-release
* Set correct version in app_data.py (consistent across project)
* Update changelog.md
* Update manuals and screenshots
  * driver development:
    * driver_test.png
  * main:
    * graphs_main_window_empty.png
    * graphs_main_window_running.png
    * main_window.png
    * main_window_layout.png
    * process_finished.png
* Update readme.md

## Build
* Commit and push changes
* Ensure GitHub tests and builds pass (CI green)

## Validation
* Download build artifacts
* Rename zip files: LilyDataLoggerStudio_<version>_<os>.zip
* Verify contents of builds
* Test builds on a clean test system

## Release
* Create Git tag, is same as version from app_data.py
* Add new GitHub release
* Add release notes
* Upload zip files

## Post-release
* Update LilyTonics website (downloads + version info)
