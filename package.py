name = "blender"
version = "5.0.1"

variants = [
    ["platform-linux", "arch-x86_64"],
    ["platform-windows", "arch-x86_64"],
    ["platform-mac", "arch-arm64"],
]

requires = ["~python-3.11"]

build_command = "python {root}/build.py"
build_requires = []
private_build_requires = []


def commands():
    env.PATH.append("{root}")
    