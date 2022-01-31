import os
import pathlib
from grpc_tools import protoc
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

# Resolve the current file location.
root = pathlib.Path(__file__).parent.resolve()
client_root = root / "src" / "python" / "simplegrpcble"
proto_root = root / "proto"


class BuildPyWithProtobuf(build_py):
    """
    Generate GRPC code before building the package.
    """

    def generate_proto(source):
        """Invokes the Protocol Compiler to generate a _pb2.py from the given
        .proto file."""

        protoc.main(
            [
                "grpc_tools.protoc",
                f"-I{proto_root}",
                f"--python_out={client_root}",
                f"--grpc_python_out={client_root}",
                f"{source}",
            ]
        )

    def run(self):
        print("Running build_py command")
        # Generate necessary .proto file if it doesn't exist.
        self.generate_proto(proto_root / "simplegrpcble.proto")
        build_py.run(self)


# Get the long description from the README file

long_description = (root / "README.md").read_text(encoding="utf-8")

setup(
    name="simplegrpcble",
    version="0.0.1",  # ! Ensure it matches the intended release version!
    author="Kevin Dewald",
    author_email="kevin@dewald.me",
    description="The ultimate fully-fledged cross-platform BLE library, designed for simplicity and ease of use.",
    long_description=long_description,
    zip_safe=True,
    cmdclass={"build_py": BuildPyWithProtobuf},
    packages=find_packages(where="src/python"),
    package_dir={"": "src/python"},
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
