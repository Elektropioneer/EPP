#!/usr/bin/python

import sys
import os
sys.path.append('src/')
import gpio
import com_serial

from logzero import logger
import time
import sliplib

import codecs

def init():
 
    global slip_driver

    logger.info("Starting up EPP...")
    
    try:
        #init everything heretup here       
        
        gpio.init()
        slip_driver = sliplib.Driver()

        #raise
        logger.info("Everything inited...")
    except:
        logger.error("Error while initing...")

def command_startexec():
    gpio.set_com()
    
    execute = ['s', 'e', 1, 1, 1, 1, 1, 1]
    logger.info("Sending " + str(execute))
    comserial.write_array(execute)
    time.sleep(0.01)
    logger.info(comserial.read_array())
    logger.info("Starting to execute code...")

    gpio.unset_com()

def command_ping():
    gpio.set_com()

    execute = ['p',1,1,1,1,1,1,1]
    logger.info("Sending ping");
    comserial.write_array(execute)
    time.sleep(0.01)
    logger.info(comserial.read_array())
    
    gpio.unset_com()

def command_odometry_ping():
    gpio.set_com()

    execute = ['o', 'h', 1, 1, 1, 1, 1, 1]
    logger.info("Sending ping to odometry")
    comserial.write_array(execute)
    time.sleep(0.01)
    logger.info(comserial.read_array())

    gpio.unset_com()

def command_abort():
    gpio.set_com()

    execute = ['o', 'a', 1, 1, 1, 1, 1 ,1]
    logger.info("Aborting...")
    comserial.write_array(execute)
    time.sleep(0.01)
    logger.info(comserial.read_array())

    gpio.unset_com()

def command_get_info():
    gpio.set_com()

    execute = ['o', 'd', 1, 1, 1, 1, 1, 1]
    logger.info("Sending get info")
    comserial.write_array(execute)
    time.sleep(0.01)
    recv = comserial.read_array()
    x = (recv[0] << 8) | recv[1]
    y = (recv[2] << 8) | recv[3]
    angle = (recv[4] << 8) | recv[5]
    state = chr(recv[6])
    spd = recv[7]

    logger.info("X: " + str(x) +
                "Y: " + str(y) +
                "Angle: " + str(angle) +
                "State: " + str(state) + 
                "Speed: " + str(spd))

    
    gpio.unset_com()

def bootup():
    
    global comserial

    load_firm_decision = raw_input("Load new firm onto main board? (Y/N)")
    if load_firm_decision.lower() == "y":
        # we want to load new firm 
        logger.info("New firm requested onto the board...")
        
        gpio.set_boot()
        gpio.reset()
        os.system("cd ~/epp/MB18/; sudo platformio run -t upload;")
        gpio.unset_boot()


    # force set to normal mode and reset
    logger.info("Setting the boot to NORMAL (0)...")
    gpio.unset_boot()
     
    # the type of control we want to do this time
    type_of_control = raw_input("Select what type of control do you want? \n 1-NORMAL, 2-Regulator Off/Get position, 3-Individual board control")

    raw_input("Press ENTER to unleash...")
  
    comserial = com_serial.ComSerial()
    
    command_startexec()

    return type_of_control

if __name__ == "__main__":
    
    init()

    control_type = bootup()
    
    # NORMAL control
    if control_type is "1":
        logger.info("Choosing NORMAL mode...")
     
        try:
            while True:
                command_get_info()
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

        command_abort()
           
                   
    elif control_type is "2":
        logger.info("Choosing Regulator OFF mode...")
        
        command_abort()

        try:
            while True:
                command_get_info()
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

    # Individual board control
    elif control_type is "3":
        logger.info("Choosing Individual control...")
        
    logger.info("EXITING...")
