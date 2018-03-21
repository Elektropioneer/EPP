import RPi.GPIO as GP
from logzero import logger
import time

GP.setwarnings(False)

reset_pin = 7
boot0_pin = 11
com_pin = 12
    
def init():
    logger.info("Initing GPIO...")
    GP.setmode(GP.BOARD)
    GP.setup(reset_pin, GP.OUT)
    GP.setup(boot0_pin, GP.OUT)
    GP.setup(com_pin, GP.OUT)

def reset():
    logger.warn("Resetting...")
    GP.output(reset_pin, 0)
    time.sleep(0.1)
    GP.output(reset_pin, 1)

def set_boot():
    logger.warn("Setting boot0 to 1...")
    GP.output(boot0_pin, 1)
    time.sleep(0.1)

def unset_boot():
    logger.warn("Setting boot0 to 0...")
    GP.output(boot0_pin, 0)
    time.sleep(0.1)

def set_com():
   # logger.warn("Setting com to 1...")
    GP.output(com_pin, 1)
    time.sleep(0.1)

def unset_com():
    #logger.warn("Setting com to 0...")
    GP.output(com_pin, 0)
    time.sleep(0.1)
