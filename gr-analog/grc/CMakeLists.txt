# Copyright 2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# Set GRC blocks directory
set(GRC_BLOCKS_DIR ${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks)

file(GLOB yml_files "*.yml")
install(FILES ${yml_files} DESTINATION ${GRC_BLOCKS_DIR})
