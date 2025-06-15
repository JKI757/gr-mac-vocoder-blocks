# Copyright 2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# Set GRC blocks directory
set(GRC_BLOCKS_DIR ${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks)

install(FILES 
    fft_fft_vxx.block.yml 
    fft_goertzel_fc.block.yml 
    fft.tree.yml 
    fft_logpwrfft_x.block.yml 
    fft_ctrlport_probe_psd.block.yml
    DESTINATION ${GRC_BLOCKS_DIR})
