#!/bin/bash
#
# Script to install gr-vocoder blocks into a specified GNU Radio installation
# This is particularly useful for installing the Codec2 and FreeDV blocks
#

# Default values
GR_PREFIX="/opt/homebrew/Cellar/gnuradio/3.10.12.0_1"
BUILD_DIR="build"
ENABLE_PYTHON="ON"
ENABLE_GRC="ON"
CLEAN_BUILD=false
VERBOSE=false

# Display help
show_help() {
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -p, --prefix PATH       Set GNU Radio installation prefix (default: $GR_PREFIX)"
    echo "  -b, --build-dir DIR     Set build directory (default: $BUILD_DIR)"
    echo "  --disable-python        Disable Python bindings"
    echo "  --disable-grc           Disable GRC blocks"
    echo "  -c, --clean             Clean build directory before building"
    echo "  -v, --verbose           Enable verbose output"
    echo "  -h, --help              Show this help message"
    echo
    echo "Example:"
    echo "  $0 --prefix /usr/local --clean"
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--prefix)
            GR_PREFIX="$2"
            shift 2
            ;;
        -b|--build-dir)
            BUILD_DIR="$2"
            shift 2
            ;;
        --disable-python)
            ENABLE_PYTHON="OFF"
            shift
            ;;
        --disable-grc)
            ENABLE_GRC="OFF"
            shift
            ;;
        -c|--clean)
            CLEAN_BUILD=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Display configuration
echo "=== GNU Radio Vocoder Block Installation ==="
echo "GNU Radio prefix: $GR_PREFIX"
echo "Build directory: $BUILD_DIR"
echo "Python bindings: $ENABLE_PYTHON"
echo "GRC blocks: $ENABLE_GRC"
echo "Clean build: $CLEAN_BUILD"
echo "Verbose: $VERBOSE"
echo "========================================"

# Check if GNU Radio installation exists
if [ ! -d "$GR_PREFIX" ]; then
    echo "Error: GNU Radio installation not found at $GR_PREFIX"
    exit 1
fi

# Set up build directory
if [ "$CLEAN_BUILD" = true ] && [ -d "$BUILD_DIR" ]; then
    echo "Cleaning build directory..."
    rm -rf "$BUILD_DIR"
fi

if [ ! -d "$BUILD_DIR" ]; then
    echo "Creating build directory..."
    mkdir -p "$BUILD_DIR"
fi

# Configure and build
echo "Configuring build..."
cd "$BUILD_DIR" || exit 1

CMAKE_ARGS=(
    "-DCMAKE_INSTALL_PREFIX=$GR_PREFIX"
    "-DENABLE_PYTHON=$ENABLE_PYTHON"
    "-DENABLE_GRC=$ENABLE_GRC"
)

if [ "$VERBOSE" = true ]; then
    CMAKE_ARGS+=("-DCMAKE_VERBOSE_MAKEFILE=ON")
fi

cmake "${CMAKE_ARGS[@]}" ..

# Build
echo "Building..."
if [ "$VERBOSE" = true ]; then
    make VERBOSE=1
else
    make
fi

# Check if build was successful
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

# Install
echo "Installing..."
if [ "$VERBOSE" = true ]; then
    sudo make install VERBOSE=1
else
    sudo make install
fi

# Verify installation of Codec2 and FreeDV blocks
if [ "$ENABLE_GRC" = "ON" ]; then
    GRC_BLOCKS_DIR="$GR_PREFIX/share/gnuradio/grc/blocks"
    
    echo "Verifying installation of Codec2 and FreeDV blocks..."
    
    # Check for Codec2 blocks
    if [ -f "$GRC_BLOCKS_DIR/vocoder_codec2_decode_ps.block.yml" ] && [ -f "$GRC_BLOCKS_DIR/vocoder_codec2_encode_sp.block.yml" ]; then
        echo "✅ Codec2 blocks installed successfully"
    else
        echo "❌ Codec2 blocks not installed"
        echo "Attempting manual installation of Codec2 blocks..."
        sudo cp ../gr-vocoder/grc/vocoder_codec2_decode_ps.block.yml ../gr-vocoder/grc/vocoder_codec2_encode_sp.block.yml "$GRC_BLOCKS_DIR/"
        if [ $? -eq 0 ]; then
            echo "✅ Codec2 blocks manually installed"
        else
            echo "❌ Failed to manually install Codec2 blocks"
        fi
    fi
    
    # Check for FreeDV blocks
    if [ -f "$GRC_BLOCKS_DIR/vocoder_freedv_rx_ss.block.yml" ] && [ -f "$GRC_BLOCKS_DIR/vocoder_freedv_tx_ss.block.yml" ]; then
        echo "✅ FreeDV blocks installed successfully"
    else
        echo "❌ FreeDV blocks not installed"
        echo "Attempting manual installation of FreeDV blocks..."
        sudo cp ../gr-vocoder/grc/vocoder_freedv_rx_ss.block.yml ../gr-vocoder/grc/vocoder_freedv_tx_ss.block.yml "$GRC_BLOCKS_DIR/"
        if [ $? -eq 0 ]; then
            echo "✅ FreeDV blocks manually installed"
        else
            echo "❌ Failed to manually install FreeDV blocks"
        fi
    fi
fi

echo "Installation complete!"
echo "You can now use the vocoder blocks in GNU Radio Companion"
