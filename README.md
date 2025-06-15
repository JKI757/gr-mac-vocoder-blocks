# Solo Vocoder

This is a standalone build of the GNU Radio vocoder module. It contains all necessary components to build and use the vocoder functionality without requiring the full GNU Radio suite.

Please note this is not really maintained and won't be.  It's simply my fix for the fact that the homebrew version of gnuradio (3.10.12.0_1) doesn't have the codec2 or the freedv blocks installed.  

## Overview

The gr-vocoder module provides various voice codecs for GNU Radio, including:

- Codec2 (low-bitrate speech codec)
- FreeDV (digital voice mode for HF radio)
- GSM (Global System for Mobile Communications codec)
- G.711 μ-law and A-law
- CVSD (Continuously Variable Slope Delta modulation)
- G.721, G.723-24, G.723-40

This standalone version ensures that all codecs, particularly Codec2 and FreeDV, are properly built and installed into the GNU Radio system.

## Dependencies

### Required
- GNU Radio Runtime
- Boost
- SWIG (for Python bindings)
- Python (for Python bindings)

### Optional
- Codec2 (for Codec2 and FreeDV support)
- GSM (for GSM FR support)

## Building

```bash
mkdir build
cd build
cmake ..
make
```

## Optional Components

- Codec2 support: Will be enabled if libcodec2 is found
- GSM support: Will be enabled if libgsm is found
- Python bindings: Can be disabled with -DENABLE_PYTHON=OFF
- GRC support: Can be disabled with -DENABLE_GRC=OFF
- Examples: Can be disabled with -DENABLE_EXAMPLES=OFF

## Installation

### Standard Installation

```bash
make install
```

### Using the Installation Scripts

Convenience scripts are provided to simplify installation, especially for ensuring Codec2 and FreeDV blocks are properly installed.

#### Bash Script (macOS/Linux)

```bash
./scripts/install_blocks.sh --prefix /path/to/gnuradio
```

#### Python Script (Cross-platform)

```bash
./scripts/install_blocks.py --prefix /path/to/gnuradio
```

Both scripts support the same options:

- `-p, --prefix PATH`: Set GNU Radio installation prefix (default: /opt/homebrew/Cellar/gnuradio/3.10.12.0_1)
- `-b, --build-dir DIR`: Set build directory (default: build)
- `--disable-python`: Disable Python bindings
- `--disable-grc`: Disable GRC blocks
- `-c, --clean`: Clean build directory before building
- `-v, --verbose`: Enable verbose output
- `-h, --help`: Show help message

The scripts will automatically verify that Codec2 and FreeDV blocks are installed correctly and attempt to fix any installation issues.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](LICENSE) file for details.
