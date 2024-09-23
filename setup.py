from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext
from pybind11.setup_helpers import Pybind11Extension
import shutil
import os
import platform
import numpy

module_name = "nvjpeg"

# CUDA 경로 설정
cuda_include = os.path.join(os.environ["CUDA_PATH"], "include")
cuda_lib = os.path.join(
    os.environ["CUDA_PATH"],
    "lib",
    "x64" if platform.machine().endswith("64") else "Win32"
)

nvjpeg_sources = ["src/nvjpeg-python.cpp", "src/x86/JpegCoder.cpp"]
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

class CustomBuildExtCommand(_build_ext):

    def run(self):
        # 원래의 build_ext 명령어 실행
        super().run()
        # .pyd 파일 복사
        ext_filename = self.get_ext_filename(module_name)
        build_lib = self.build_lib
        source_path = os.path.join(build_lib, ext_filename)
        dest_dir = os.path.join(build_lib, "nvjpeg")
        dest_path = os.path.join(dest_dir, os.path.basename(ext_filename))
        print(f"Copying {source_path} to {dest_path}")
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copyfile(source_path, dest_path)

setup(
    ext_modules=[extension_nvjpeg],
    cmdclass={"build_ext": CustomBuildExtCommand},
)
