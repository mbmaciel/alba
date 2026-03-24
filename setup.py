from cx_Freeze import Executable, setup

# Equivalent to:
# cxfreeze.exe .\main.py --target-dir .\dist\ --base-name=gui
build_exe_options = {
    "build_exe": "dist",
    "include_msvcr": True,
    #"include_files": [
    #    ("database/alba.db", "database/alba.db"),
    #],
}

setup(
    name="alba",
    version="1.4",
    description="Alba application",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="main.py",
            base="gui",
        )
    ],
)
