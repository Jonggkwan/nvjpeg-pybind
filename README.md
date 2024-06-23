# NvJpeg - pybind11

This project is based on the [nvjpeg-python](https://github.com/UsingNet/nvjpeg-python) repository. It has been extended to use `pybind11` to create Python bindings for the `nvjpeg` library, allowing for efficient JPEG encoding and decoding using Nvidia's GPU acceleration.

## Requirements

- CUDA
- numpy
- Python >= 3.6
- Visual Studio with C++ desktop development tools

## Supported System

- Windows

## Installation

```shell
pip install git+https://github.com/jonggkwan/nvjpeg-pybind.git
```

## Usage

### 0. Init PyNvJpeg

```python
from nvjpeg import NvJpeg
nj = NvJpeg()
```

### 1. Use PyNvJpeg

#### Read Jpeg File to Numpy

```python
img = nj.read("_JPEG_FILE_PATH_")
# like cv2.imread("_JPEG_FILE_PATH_")
```

#### Write Numpy to Jpeg File

```python
nj.write("_JPEG_FILE_PATH_", img)
# or nj.write("_JPEG_FILE_PATH_", quality)
# int quality default 70, mean jpeg quality
# like cv2.imwrite("_JPEG_FILE_PATH_", img)
```

#### Decode Jpeg bytes in variable

```python
img = nj.decode(jpeg_bytes)
# like cv2.imdecode(variable)
```

#### Encode image numpy array to bytes

```python
jpeg_bytes = nj.encode(img)
# or with jpeg quality
# jpeg_bytes = nj.encode(img, 70)
# int quality default 70, mean jpeg quality

# like cv2.imencode(".jpg", variable)[1]
```

## Notes

Visual Studio Requirement: Ensure you have Visual Studio with C++ desktop development tools installed, as it is necessary for building the extension.
CUDA Toolkit: Make sure the CUDA Toolkit is installed and properly configured on your system.
