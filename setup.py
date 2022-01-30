import os
import pathlib
from wheel.bdist_wheel import bdist_wheel
from distutils.command.build_py import build_py
import setuptools.command.build_py as _build_py
from grpc_tools import protoc
from setuptools import setup, find_packages

# Resolve the current file location.
root = pathlib.Path(__file__).parent.resolve()
client_root = root / "src" / "python" / "simplegrpcble"
proto_root = root / "proto"

def generate_proto(source, require=True):
    """Invokes the Protocol Compiler to generate a _pb2.py from the given
    .proto file.  Does nothing if the output already exists and is newer than
    the input."""

    if not require and not os.path.exists(source):
        return

    # output = source.replace(".proto", "_pb2.py").replace("../src/", "")

    protoc.main(
        ["grpc_tools.protoc", f"-I{proto_root}", f"--python_out={client_root}", f"--grpc_python_out={client_root}", f"{source}"]
    )


class BuildPyCommand(build_py):
    """
    Generate GRPC code before building the package.
    """

    def run(self):
        print("Running build_py command")
        # Generate necessary .proto file if it doesn't exist.
        generate_proto(proto_root / "simplegrpcble.proto")
        build_py.run(self)


class BDistWheelCommand(bdist_wheel):
    """
    Generate GRPC code before building a wheel.
    """

    def run(self):
        print("Running bdist_wheel command")
        # Generate necessary .proto file if it doesn't exist.
        generate_proto(proto_root / "simplegrpcble.proto")
        bdist_wheel.run(self)


# Get the long description from the README file

# long_description = (here / "README.md").read_text(encoding="utf-8")
long_description = ""

print(find_packages(where="src/python"))

# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    name="simplegrpcble",
    version="0.0.1",  # ! Ensure it matches the intended release version!
    author="Kevin Dewald",
    author_email="kevin@dewald.me",
    description="The ultimate fully-fledged cross-platform BLE library, designed for simplicity and ease of use.",
    long_description=long_description,
    zip_safe=True,
    cmdclass={"build_py": BuildPyCommand, "bdist_wheel": BDistWheelCommand},
    packages=find_packages(where="src/python"),
    package_dir = {'': 'src/python'},
    extras_require={},
    setup_requires=["grpcio_tools"],
    install_requires=["grpcio"],
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
