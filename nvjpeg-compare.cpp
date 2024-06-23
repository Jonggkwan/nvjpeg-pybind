#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cstddef> // Include this for ssize_t
#include "JpegCoder.hpp"

#ifdef _WIN32
#include <windows.h>
#include <cstdlib>
#include <string>

// Convert std::string to std::wstring
std::wstring string_to_wstring(const std::string &str)
{
    int size_needed = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), (int)str.size(), NULL, 0);
    std::wstring wstr_to(size_needed, 0);
    MultiByteToWideChar(CP_UTF8, 0, str.c_str(), (int)str.size(), &wstr_to[0], size_needed);
    return wstr_to;
}

void add_cuda_directory()
{
    const char *cuda_path_env = std::getenv("CUDA_PATH");
    if (cuda_path_env)
    {
        std::string cuda_path_str = std::string(cuda_path_env) + "\\bin";
        std::wstring cuda_path = string_to_wstring(cuda_path_str);
        AddDllDirectory(cuda_path.c_str());
    }
    else
    {
        fprintf(stderr, "CUDA_PATH environment variable not set.\n");
    }
}
#endif

namespace py = pybind11;

class NvJpeg
{
public:
    NvJpeg()
    {
#ifdef _WIN32
        add_cuda_directory();
#endif
        m_handle = new JpegCoder();
    }

    ~NvJpeg()
    {
        delete m_handle;
    }

    py::array_t<uint8_t> decode(py::bytes jpegData)
    {
        JpegCoderImage *img;
        try
        {
            m_handle->ensureThread(static_cast<long>(PyThread_get_thread_ident()));
            std::string data = jpegData;
            img = m_handle->decode(reinterpret_cast<const unsigned char *>(data.data()), data.size());
        }
        catch (JpegCoderError &e)
        {
            throw std::runtime_error(e.what());
        }

        auto buffer = img->buffer();
        std::vector<ssize_t> shape = {static_cast<ssize_t>(img->height), static_cast<ssize_t>(img->width), 3};
        auto result = py::array_t<uint8_t>(shape, buffer);
        delete img;
        return result;
    }

    py::bytes encode(py::array_t<uint8_t> image, unsigned int quality = 70)
    {
        if (image.ndim() != 3 || image.shape(2) != 3)
        {
            throw std::invalid_argument("Input image must be of shape (height, width, 3)");
        }

        auto img = new JpegCoderImage(image.shape(1), image.shape(0), 3, JPEGCODER_CSS_444);
        img->fill(image.data());

        m_handle->ensureThread(static_cast<long>(PyThread_get_thread_ident()));
        auto data = m_handle->encode(img, quality);

        py::bytes result(reinterpret_cast<const char *>(data->data), data->size);
        delete data;
        delete img;
        return result;
    }

    py::array_t<uint8_t> read(const std::string &jpegFile)
    {
        FILE *fp = fopen(jpegFile.c_str(), "rb");
        if (!fp)
        {
            throw std::runtime_error("Cannot open file " + jpegFile);
        }

        fseek(fp, 0, SEEK_END);
        size_t dataLength = ftell(fp);
        unsigned char *jpegData = (unsigned char *)malloc(dataLength);
        if (!jpegData)
        {
            fclose(fp);
            throw std::runtime_error("Out of memory when reading file " + jpegFile);
        }

        fseek(fp, 0, SEEK_SET);
        fread(jpegData, 1, dataLength, fp);
        fclose(fp);

        m_handle->ensureThread(static_cast<long>(PyThread_get_thread_ident()));
        auto img = m_handle->decode(reinterpret_cast<const unsigned char *>(jpegData), dataLength);
        free(jpegData);

        auto buffer = img->buffer();
        std::vector<ssize_t> shape = {static_cast<ssize_t>(img->height), static_cast<ssize_t>(img->width), 3};
        auto result = py::array_t<uint8_t>(shape, buffer);
        delete img;
        return result;
    }

    void write(const std::string &jpegFile, py::array_t<uint8_t> image, unsigned int quality = 70)
    {
        FILE *fp = fopen(jpegFile.c_str(), "wb");
        if (!fp)
        {
            throw std::runtime_error("Cannot open file " + jpegFile);
        }

        py::bytes encoded_data = encode(image, quality);
        std::string encoded_data_str = static_cast<std::string>(encoded_data);
        const char *jpegData = encoded_data_str.data();
        size_t jpegDataSize = encoded_data_str.size();

        fwrite(jpegData, 1, jpegDataSize, fp);
        fclose(fp);
    }

private:
    JpegCoder *m_handle;
};

PYBIND11_MODULE(nvjpeg, m)
{
    py::class_<NvJpeg>(m, "NvJpeg")
        .def(py::init<>())
        .def("decode", &NvJpeg::decode, "Decode JPEG data to image")
        .def("encode", &NvJpeg::encode, "Encode image to JPEG data", py::arg("image"), py::arg("quality") = 70)
        .def("read", &NvJpeg::read, "Read and decode JPEG file", py::arg("jpegFile"))
        .def("write", &NvJpeg::write, "Encode and write image to JPEG file", py::arg("jpegFile"), py::arg("image"), py::arg("quality") = 70);
}
