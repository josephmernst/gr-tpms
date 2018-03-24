#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Virginia Tech.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import pmt
from gnuradio import gr

class print_burst(gr.sync_block):
    """
    docstring for block print_burst
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="print_burst",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern("pdu"))
        self.set_msg_handler(pmt.intern("pdu"),self.handler)

    def handler(self,msg):
        cdr=pmt.cdr(msg)
        data=numpy.array(pmt.u8vector_elements(cdr),dtype=numpy.uint8)
        for i in range(len(data)/8):
            val=0
            for j in range(8):
                val=val+data[i*8+j]*(2**(7-j))
            print "%02X" % val,
        print


    def work(self, input_items, output_items):
        pass

