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

class parse_burst(gr.sync_block):
    """
    docstring for block parse_burst
    """
    def __init__(self, samp_rate):
        gr.sync_block.__init__(self,
            name="parse_burst",
            in_sig=[],
            out_sig=[])

        self.samp_rate=samp_rate

        self.message_port_register_in(pmt.intern("pdu"))
        self.message_port_register_out(pmt.intern("data"))
        self.set_msg_handler(pmt.intern("pdu"),self.parser)
        
    def parser(self,msg):
        # Get data from pdu
        cdr = pmt.cdr(msg);
        data= copy(numpy.array(pmt.f32vector_elements(cdr), dtype=numpy.float32))

        # Calculate number of samples per half bit
        interpolation=30*self.samp_rate/250000
        self.threshold=.5

        # Find first transition
        first_transition=numpy.argmax(data>self.threshold)
        burst_width=numpy.argmax(data[first_transition:]<self.threshold)
        while burst_width<10:
            first_transition=numpy.argmax(data[first_transition+burst_width+1:]>self.threshold)+first_transition+burst_width+1
            burst_width=numpy.argmax(data[first_transition:]<self.threshold)
        next_expected_transition=first_transition
        next_expected_transition+=interpolation*2

        # The first transition is a zero bit
        bits=[0]

    def work(self, input_items, output_items):
        pass

