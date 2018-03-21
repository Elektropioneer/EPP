#!/usr/bin/python

#http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/serial.inc.php

from logzero import logger
import serial
import time
import sliplib
from sliplib import encode, decode
import ast

port = "/dev/ttyS0"

class ComSerial:

    def __init__(self):

        self.ser = None
        self.slip = None

        logger.info("Initing Serial communicaion...")
        
        try:
            self.ser = serial.Serial(
                    port, 
                    baudrate=115200)
           
          
            logger.info("Opened serial...")
        except:
            logger.error("Couldn't open serial...")

    # function:    def read(self)
    # description: reads one character from serial
    def read(self):
        return ord(self.ser.read())
    
    # function:    def write(self, data)
    # description: write one character to serial
    def write(self, data):
        logger.info("Writing data: " + str(data))
   
    # function:    def read_array(self)
    # description: reads an array from arduino and returns an array
    def read_array(self):
     
        data = []
        
        for i in range(0, 8):
            data.append(ord(self.ser.read()))

        return data

    # function:    def write_array(self, dt)
    # description: writes an array to the arduino
    def write_array(self, dt):
        
        self.ser.write(bytearray(dt))
        
        self.ser.flush()


