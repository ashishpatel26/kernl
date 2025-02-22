#  Copyright 2022 Lefebvre Sarrut
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import os
import pathlib

import pkg_resources
from setuptools import find_packages, setup


try:
    import torch

    assert torch.__version__ >= "1.12.0"
    if not os.environ.get("SKIP_CUDA_ASSERT", False):
        assert torch.cuda.is_available(), "CUDA is required to install kernl"
        major, _ = torch.cuda.get_device_capability()
        if major < 8:
            raise RuntimeError("GPU compute capability 8.0 (Ampere) or higher is required to install kernl")
except ImportError:
    raise ImportError("Please install torch before installing kernl")


with pathlib.Path("requirements.txt").open() as f:
    install_requires = [str(requirement) for requirement in pkg_resources.parse_requirements(f)]

with pathlib.Path("requirements-benchmark.txt").open() as f:
    extra_benchmark = [str(requirement) for requirement in pkg_resources.parse_requirements(f)]


setup(
    name="kernl",
    version="0.1.0",
    license="Apache License 2.0",
    license_files=("LICENSE",),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
    ],
    description="Accelerate deep learning inference with custom GPU kernels written in Triton",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    keywords=["Deep Learning"],
    long_description_content_type="text/markdown",
    url="https://github.com/ELS-RD/kernl",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=install_requires,
    extras_require={
        "benchmark": extra_benchmark,
    },
    python_requires="==3.9.*",
)
