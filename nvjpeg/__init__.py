import os
import sys

# Ensure CUDA_PATH is set and correct
cuda_path_env = os.getenv("CUDA_PATH")
if cuda_path_env:
    cuda_bin_path = os.path.join(cuda_path_env, "bin")
    os.add_dll_directory(cuda_bin_path)
else:
    print("CUDA_PATH environment variable not set.", file=sys.stderr)

from .nvjpeg import NvJpeg

__all__ = ["NvJpeg"]
