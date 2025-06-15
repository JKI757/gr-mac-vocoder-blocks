#!/usr/bin/env python3
"""
Script to install gr-vocoder blocks into a specified GNU Radio installation.
This is particularly useful for installing the Codec2 and FreeDV blocks.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, verbose=False):
    """Run a shell command and return the output and status."""
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if verbose:
        print(process.stdout)
        if process.returncode != 0:
            print(f"Error: {process.stderr}", file=sys.stderr)
    
    return process.returncode, process.stdout, process.stderr


def main():
    # Default values
    default_prefix = "/opt/homebrew/Cellar/gnuradio/3.10.12.0_1"
    default_build_dir = "build"
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Install gr-vocoder blocks into a specified GNU Radio installation"
    )
    parser.add_argument(
        "-p", "--prefix",
        default=default_prefix,
        help=f"GNU Radio installation prefix (default: {default_prefix})"
    )
    parser.add_argument(
        "-b", "--build-dir",
        default=default_build_dir,
        help=f"Build directory (default: {default_build_dir})"
    )
    parser.add_argument(
        "--disable-python",
        action="store_true",
        help="Disable Python bindings"
    )
    parser.add_argument(
        "--disable-grc",
        action="store_true",
        help="Disable GRC blocks"
    )
    parser.add_argument(
        "-c", "--clean",
        action="store_true",
        help="Clean build directory before building"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Display configuration
    print("=== GNU Radio Vocoder Block Installation ===")
    print(f"GNU Radio prefix: {args.prefix}")
    print(f"Build directory: {args.build_dir}")
    print(f"Python bindings: {'OFF' if args.disable_python else 'ON'}")
    print(f"GRC blocks: {'OFF' if args.disable_grc else 'ON'}")
    print(f"Clean build: {args.clean}")
    print(f"Verbose: {args.verbose}")
    print("========================================")
    
    # Check if GNU Radio installation exists
    if not os.path.isdir(args.prefix):
        print(f"Error: GNU Radio installation not found at {args.prefix}", file=sys.stderr)
        return 1
    
    # Get script directory and project root
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent
    
    # Set up build directory
    build_dir = project_root / args.build_dir
    if args.clean and build_dir.exists():
        print("Cleaning build directory...")
        shutil.rmtree(build_dir)
    
    if not build_dir.exists():
        print("Creating build directory...")
        build_dir.mkdir(parents=True)
    
    # Configure and build
    print("Configuring build...")
    os.chdir(build_dir)
    
    cmake_args = [
        "cmake",
        f"-DCMAKE_INSTALL_PREFIX={args.prefix}",
        f"-DENABLE_PYTHON={'OFF' if args.disable_python else 'ON'}",
        f"-DENABLE_GRC={'OFF' if args.disable_grc else 'ON'}"
    ]
    
    if args.verbose:
        cmake_args.append("-DCMAKE_VERBOSE_MAKEFILE=ON")
    
    cmake_args.append("..")
    
    returncode, _, _ = run_command(cmake_args, args.verbose)
    if returncode != 0:
        print("CMake configuration failed!", file=sys.stderr)
        return 1
    
    # Build
    print("Building...")
    make_args = ["make"]
    if args.verbose:
        make_args.append("VERBOSE=1")
    
    returncode, _, _ = run_command(make_args, args.verbose)
    if returncode != 0:
        print("Build failed!", file=sys.stderr)
        return 1
    
    # Install
    print("Installing...")
    install_args = ["sudo", "make", "install"]
    if args.verbose:
        install_args.append("VERBOSE=1")
    
    returncode, _, _ = run_command(install_args, args.verbose)
    if returncode != 0:
        print("Installation failed!", file=sys.stderr)
        return 1
    
    # Verify installation of Codec2 and FreeDV blocks
    if not args.disable_grc:
        grc_blocks_dir = Path(args.prefix) / "share" / "gnuradio" / "grc" / "blocks"
        
        print("Verifying installation of Codec2 and FreeDV blocks...")
        
        # Check for Codec2 blocks
        codec2_decode = grc_blocks_dir / "vocoder_codec2_decode_ps.block.yml"
        codec2_encode = grc_blocks_dir / "vocoder_codec2_encode_sp.block.yml"
        
        if codec2_decode.exists() and codec2_encode.exists():
            print("✅ Codec2 blocks installed successfully")
        else:
            print("❌ Codec2 blocks not installed")
            print("Attempting manual installation of Codec2 blocks...")
            
            src_codec2_decode = project_root / "gr-vocoder" / "grc" / "vocoder_codec2_decode_ps.block.yml"
            src_codec2_encode = project_root / "gr-vocoder" / "grc" / "vocoder_codec2_encode_sp.block.yml"
            
            if src_codec2_decode.exists() and src_codec2_encode.exists():
                returncode, _, _ = run_command([
                    "sudo", "cp", 
                    str(src_codec2_decode), 
                    str(src_codec2_encode), 
                    str(grc_blocks_dir)
                ], args.verbose)
                
                if returncode == 0:
                    print("✅ Codec2 blocks manually installed")
                else:
                    print("❌ Failed to manually install Codec2 blocks")
            else:
                print("❌ Codec2 block source files not found")
        
        # Check for FreeDV blocks
        freedv_rx = grc_blocks_dir / "vocoder_freedv_rx_ss.block.yml"
        freedv_tx = grc_blocks_dir / "vocoder_freedv_tx_ss.block.yml"
        
        if freedv_rx.exists() and freedv_tx.exists():
            print("✅ FreeDV blocks installed successfully")
        else:
            print("❌ FreeDV blocks not installed")
            print("Attempting manual installation of FreeDV blocks...")
            
            src_freedv_rx = project_root / "gr-vocoder" / "grc" / "vocoder_freedv_rx_ss.block.yml"
            src_freedv_tx = project_root / "gr-vocoder" / "grc" / "vocoder_freedv_tx_ss.block.yml"
            
            if src_freedv_rx.exists() and src_freedv_tx.exists():
                returncode, _, _ = run_command([
                    "sudo", "cp", 
                    str(src_freedv_rx), 
                    str(src_freedv_tx), 
                    str(grc_blocks_dir)
                ], args.verbose)
                
                if returncode == 0:
                    print("✅ FreeDV blocks manually installed")
                else:
                    print("❌ Failed to manually install FreeDV blocks")
            else:
                print("❌ FreeDV block source files not found")
    
    print("Installation complete!")
    print("You can now use the vocoder blocks in GNU Radio Companion")
    return 0


if __name__ == "__main__":
    sys.exit(main())
