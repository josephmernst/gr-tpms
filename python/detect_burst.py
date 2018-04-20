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

class detect_burst(gr.sync_block):
    """
    docstring for block detect_burst
    """
    def __init__(self, threshold_up=2, threshold_down=0, buffer_length=0):
        gr.sync_block.__init__(self,
            name="detect_burst",
            in_sig=[numpy.float32,numpy.float32],
            out_sig=[])

        self.threshold_up=threshold_up
        self.threshold_down=threshold_down
        if self.threshold_down is None:
            self.threshold_down=self.threshold_up
        self.message_port_register_out(pmt.intern("pdu"))
        self.prev_data=[]
        self.buffer_length=buffer_length
        self.data=[]
        self.in_burst=False
        self.finish_burst=False
        self.end_burst_data=[]

    def set_threshold_up(self,new_up):
        self.threshold_up=new_up
        if self.threshold_up<self.threshold_down:
            self.threshold_down=new_up
            
    def set_threshold_down(self,new_down):
        if new_down>self.threshold_up:
            return
        self.threshold_down=new_down

    def set_buffer_length(self,new_buffer):
        self.buffer_length=int(new_buffer)
        
    def update_prev_data(self,new_data):
        self.prev_data=numpy.append(self.prev_data,new_data)
        self.prev_data=self.prev_data[len(self.prev_data)-self.buffer_length:]

    def work(self, input_items, output_items):
	da=input_items[0]
	energy=input_items[1]
        if self.finish_burst:
            ## Found end of burst, but need to add buffer

            num=self.buffer_length-len(self.end_burst_data)

            if len(da)<num:
                ## If we need to add all of the data to the end burst
                self.end_burst_data=numpy.append(self.end_burst_data,da)
                return len(da)
            else:
                ## If we only need some of the data for the end burst
                self.end_burst_data=numpy.append(self.end_burst_data,da[:num])
                self.data=numpy.append(self.data,self.end_burst_data)
                
	        self.in_burst=False
                self.finish_burst=False

                self.prev_data=da[num:]

                ## Create pdu with burst
	        dpdu=pmt.init_f32vector(len(self.data),self.data)
	        msg=pmt.cons(pmt.PMT_NIL,dpdu)

                ## Send PDU
	        self.message_port_pub(pmt.intern("pdu"),msg)
	        self.data=numpy.array([])
	        return num

	elif not self.in_burst:
                # If not currently in a burst
		packet_start=numpy.argmax(energy>self.threshold_up)
		if max(energy)>self.threshold_up:
                        # If the energy exceeds the threshold
			self.in_burst=True # We are now in a burst
                        self.update_prev_data(da[:packet_start])

                        # Start data with a pad of 0's
                        #self.data=numpy.array([0]*1000)
                        self.data=numpy.array([])
                        # Add the "prev data"
                        self.data=numpy.append(self.data,self.prev_data)
                        
			return packet_start
		else:
                        # If no packet is detected save data into "previous data"
                        self.update_prev_data(da)
			return len(energy)
	else:
                # If we are already in a burst
		packet_end=numpy.argmax(energy<=self.threshold_down)
		if min(energy)>self.threshold_down:
                        # If the end of the packet is not found
			self.data=numpy.append(self.data,da)
			return len(da)
		else:
                        # If the end of the packet is found
                        self.finish_burst=True
			self.data=numpy.append(self.data,da[:packet_end])
                        return packet_end

	raise Exception("should never get here")

