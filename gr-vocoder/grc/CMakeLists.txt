# Copyright 2011,2016 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# Set GRC blocks directory
set(GRC_BLOCKS_DIR ${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks)
message(STATUS "GRC blocks will be installed to: ${GRC_BLOCKS_DIR}")

# Install base vocoder blocks
install(FILES
    vocoder_alaw_decode_bs.block.yml
    vocoder_alaw_encode_sb.block.yml
    vocoder_cvsd_decode_bs.block.yml
    vocoder_cvsd_decode.block.yml
    vocoder_cvsd_encode_sb.block.yml
    vocoder_cvsd_encode.block.yml
    vocoder_g721_decode_bs.block.yml
    vocoder_g721_encode_sb.block.yml
    vocoder_g723_24_decode_bs.block.yml
    vocoder_g723_24_encode_sb.block.yml
    vocoder_g723_40_decode_bs.block.yml
    vocoder_g723_40_encode_sb.block.yml
    vocoder_ulaw_decode_bs.block.yml
    vocoder_ulaw_encode_sb.block.yml
    vocoder.tree.yml
    DESTINATION ${GRC_BLOCKS_DIR}
)

# Install Codec2 blocks if available
if(LIBCODEC2_FOUND)
    message(STATUS "Found Codec2: ${LIBCODEC2_LIBRARIES}")
    set(CODEC2_BLOCKS
        ${CMAKE_CURRENT_SOURCE_DIR}/vocoder_codec2_decode_ps.block.yml
        ${CMAKE_CURRENT_SOURCE_DIR}/vocoder_codec2_encode_sp.block.yml
    )
    foreach(block ${CODEC2_BLOCKS})
        if(EXISTS ${block})
            message(STATUS "Found Codec2 block: ${block}")
        else()
            message(WARNING "Missing Codec2 block: ${block}")
        endif()
    endforeach()
    install(FILES ${CODEC2_BLOCKS}
        DESTINATION ${GRC_BLOCKS_DIR}
    )
endif(LIBCODEC2_FOUND)

# Install FreeDV blocks if available
if(LIBCODEC2_HAS_FREEDV_API)
    message(STATUS "Found FreeDV API in Codec2")
    set(FREEDV_BLOCKS
        ${CMAKE_CURRENT_SOURCE_DIR}/vocoder_freedv_rx_ss.block.yml
        ${CMAKE_CURRENT_SOURCE_DIR}/vocoder_freedv_tx_ss.block.yml
    )
    foreach(block ${FREEDV_BLOCKS})
        if(EXISTS ${block})
            message(STATUS "Found FreeDV block: ${block}")
        else()
            message(WARNING "Missing FreeDV block: ${block}")
        endif()
    endforeach()
    install(FILES ${FREEDV_BLOCKS}
        DESTINATION ${GRC_BLOCKS_DIR}
    )
endif(LIBCODEC2_HAS_FREEDV_API)

# Install GSM blocks if available
if(LIBGSM_FOUND)
    message(STATUS "Found GSM: ${LIBGSM_LIBRARIES}")
    set(GSM_BLOCKS
        ${CMAKE_CURRENT_SOURCE_DIR}/vocoder_gsm_fr_decode_ps.block.yml
        ${CMAKE_CURRENT_SOURCE_DIR}/vocoder_gsm_fr_encode_sp.block.yml
    )
    foreach(block ${GSM_BLOCKS})
        if(EXISTS ${block})
            message(STATUS "Found GSM block: ${block}")
        else()
            message(WARNING "Missing GSM block: ${block}")
        endif()
    endforeach()
    install(FILES ${GSM_BLOCKS}
        DESTINATION ${GRC_BLOCKS_DIR}
    )
endif(LIBGSM_FOUND)
