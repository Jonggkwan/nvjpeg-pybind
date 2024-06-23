from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools.command.build_ext import build_ext as _build_ext
import shutil
import os
import platform
import numpy

module_name = "nvjpeg"

cuda_include = os.path.join(os.environ["CUDA_PATH"], "include")
cuda_lib = os.path.join(os.environ["CUDA_PATH"], "lib", "x64" if platform.machine().endswith("64") else "Win32")
nvjpeg_sources = ["nvjpeg-python.cpp", "src/x86/JpegCoder.cpp"]
nvjpeg_include_dirs = ["include", numpy.get_include(), cuda_include]
nvjpeg_library_dirs = [cuda_lib]
nvjpeg_libraries = ["cudart", "nvjpeg"]

extension_nvjpeg = Pybind11Extension(
    module_name,
    sources=nvjpeg_sources,
    include_dirs=nvjpeg_include_dirs,
    library_dirs=nvjpeg_library_dirs,
    libraries=nvjpeg_libraries,
    define_macros=[("JPEGCODER_ARCH", "x86")],
)


class CustomBuildExtCommand(build_ext):
    """Custom build_ext command to copy the .pyd file to the package directory."""

    def run(self):
        # First, run the original build_ext command
        _build_ext.run(self)
        # Then, copy the compiled .pyd file to the nvjpeg package directory
        ext_filename = self.get_ext_filename(module_name)
        build_lib = self.build_lib
        source_path = os.path.join(build_lib, ext_filename)
        dest_dir = os.path.join(build_lib, "nvjpeg")
        dest_path = os.path.join(dest_dir, os.path.basename(ext_filename))
        print(f"Copying {source_path} to {dest_path}")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copyfile(source_path, dest_path)


setup(
    name="nvjpeg",
    version="0.1.0",
    ext_modules=[extension_nvjpeg],
    cmdclass={"build_ext": CustomBuildExtCommand},
    author="JK",
    author_email="skekdnzm1994@gmail.com",
    license="MIT",
    description="Python interface for nvjpeg. Encode/Decode Jpeg with Nvidia GPU Hardware Acceleration.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jonggkwan/nvjpeg-python",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Environment :: GPU :: NVIDIA CUDA :: 11.8",
    ],
    keywords=[
        "pynvjpeg",
        "nvjpeg",
        "jpeg",
        "jpg",
        "encode",
        "decode",
        "jpg encode",
        "jpg decode",
        "jpeg encode",
        "jpeg decode",
        "gpu",
        "nvidia",
    ],
    python_requires=">=3.6",
    project_urls={
        "Source": "https://github.com/jonggkwan/nvjpeg-python",
        "Tracker": "https://github.com/jonggkwan/nvjpeg-python/issues",
    },
    install_requires=["numpy", "pybind11"],
    packages=find_packages(),
    package_data={
        "nvjpeg": ["*.pyi", "*.pyd"],  # Ensure the .pyd file is included
    },
    include_package_data=True,
    zip_safe=False,
)
