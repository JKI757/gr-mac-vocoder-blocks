cmake_minimum_required(VERSION 3.16)
project(solo_vocoder CXX C)

# Select the release build type by default to get optimization flags
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "")
endif()

# Enable testing
enable_testing()

# Set build options
option(BUILD_SHARED_LIBS "Build shared libraries" ON)
option(ENABLE_PYTHON "Enable Python bindings" ON)
option(ENABLE_GRC "Enable GRC support" ON)
option(ENABLE_EXAMPLES "Enable examples" OFF)
option(ENABLE_CTRLPORT "Enable ControlPort" OFF)
option(ENABLE_PERFORMANCE_COUNTERS "Enable Performance Counters" OFF)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Add CMake modules path
list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_SOURCE_DIR}/cmake/Modules)

# Version information (needed by some components)
set(VERSION_MAJOR 3)
set(VERSION_API 10)
set(VERSION_ABI 0)
set(VERSION_PATCH 0)
include(GrVersion)

# Include important GNU Radio CMake utilities
include(GrPlatform)
include(GrMiscUtils)
include(GrComponent)

# Setup Boost
include(GrBoost)

# Find other dependencies
find_package(PkgConfig)
find_package(SWIG)
find_package(Python3 COMPONENTS Interpreter Development)
find_package(FFTW3f)
find_package(Volk)
find_package(Codec2)
find_package(GSM)

# Set Python variables
set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE})
set(PYTHON_INCLUDE_PATH ${Python3_INCLUDE_DIRS})
set(PYTHON_LIBRARIES ${Python3_LIBRARIES})

# Set install directories
include(GrPlatform) #define LIB_SUFFIX
include(GNUInstallDirs)

set(GR_RUNTIME_DIR      ${CMAKE_INSTALL_BINDIR})
set(GR_LIBRARY_DIR      ${CMAKE_INSTALL_LIBDIR})
set(GR_INCLUDE_DIR      ${CMAKE_INSTALL_INCLUDEDIR})
set(GR_DATA_DIR         ${CMAKE_INSTALL_DATADIR})
set(GR_PKG_DATA_DIR     ${CMAKE_INSTALL_DATADIR}/gnuradio)
set(GR_DOC_DIR          ${CMAKE_INSTALL_DOCDIR})
set(GR_PKG_DOC_DIR      ${CMAKE_INSTALL_DOCDIR}/gnuradio)
set(GR_CONF_DIR         ${CMAKE_INSTALL_SYSCONFDIR})
set(GR_PKG_CONF_DIR     ${CMAKE_INSTALL_SYSCONFDIR}/gnuradio/conf.d)
set(GR_LIBEXEC_DIR      ${CMAKE_INSTALL_LIBEXECDIR})
set(GR_PKG_LIBEXEC_DIR  ${CMAKE_INSTALL_LIBEXECDIR}/gnuradio)
set(GR_GRC_DIR          ${CMAKE_INSTALL_DATADIR}/gnuradio/grc/blocks)
set(GR_CMAKE_DIR        ${CMAKE_INSTALL_LIBDIR}/cmake/gnuradio)

# Additional configuration
set(SYSCONFDIR ${CMAKE_INSTALL_PREFIX}/${GR_CONF_DIR})
set(GR_PREFSDIR ${SYSCONFDIR}/gnuradio/conf.d)

# Enable GNU Radio components
set(ENABLE_GNURADIO_RUNTIME ON)
set(ENABLE_GR_FFT ON)
set(ENABLE_GR_BLOCKS ON)
set(ENABLE_GR_FILTER ON)
set(ENABLE_GR_ANALOG ON)
set(ENABLE_GR_VOCODER ON)

# Add compiler flags
add_compile_definitions(_GLIBCXX_USE_CXX11_ABI=0)

# Add GNU Radio components
add_subdirectory(gnuradio-runtime)
add_subdirectory(gr-fft)
add_subdirectory(gr-blocks)
add_subdirectory(gr-filter)
add_subdirectory(gr-analog)
add_subdirectory(gr-vocoder)

# Create pkg-config file
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/gr-vocoder/gnuradio-vocoder.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-vocoder.pc
    @ONLY)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-vocoder.pc
    DESTINATION ${GR_LIBRARY_DIR}/pkgconfig
)
