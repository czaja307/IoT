#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from . import oled_config
import RPi.GPIO as GPIO
import time
import numpy as np

DRAW_LINE                       = 0x21
DRAW_RECTANGLE                  = 0x22
COPY_WINDOW                     = 0x23
DIM_WINDOW                      = 0x24
CLEAR_WINDOW                    = 0x25
FILL_WINDOW                     = 0x26
DISABLE_FILL                    = 0x00
ENABLE_FILL                     = 0x01
CONTINUOUS_SCROLLING_SETUP      = 0x27
DEACTIVE_SCROLLING              = 0x2E
ACTIVE_SCROLLING                = 0x2F

SET_COLUMN_ADDRESS              = 0x15
SET_ROW_ADDRESS                 = 0x75
SET_CONTRAST_A                  = 0x81
SET_CONTRAST_B                  = 0x82
SET_CONTRAST_C                  = 0x83
MASTER_CURRENT_CONTROL          = 0x87
SET_PRECHARGE_SPEED_A           = 0x8A
SET_PRECHARGE_SPEED_B           = 0x8B
SET_PRECHARGE_SPEED_C           = 0x8C
SET_REMAP                       = 0xA0
SET_DISPLAY_START_LINE          = 0xA1
SET_DISPLAY_OFFSET              = 0xA2
NORMAL_DISPLAY                  = 0xA4
ENTIRE_DISPLAY_ON               = 0xA5
ENTIRE_DISPLAY_OFF              = 0xA6
INVERSE_DISPLAY                 = 0xA7
SET_MULTIPLEX_RATIO             = 0xA8
DIM_MODE_SETTING                = 0xAB
SET_MASTER_CONFIGURE            = 0xAD
DIM_MODE_DISPLAY_ON             = 0xAC
DISPLAY_OFF                     = 0xAE
NORMAL_BRIGHTNESS_DISPLAY_ON    = 0xAF
POWER_SAVE_MODE                 = 0xB0
PHASE_PERIOD_ADJUSTMENT         = 0xB1
DISPLAY_CLOCK_DIV               = 0xB3
SET_GRAy_SCALE_TABLE            = 0xB8
ENABLE_LINEAR_GRAY_SCALE_TABLE  = 0xB9
SET_PRECHARGE_VOLTAGE           = 0xBB

SET_V_VOLTAGE                   = 0xBE


OLED_WIDTH = 96
OLED_HEIGHT  = 64

class SSD1331(object):
    def __init__(self):
        self.width = OLED_WIDTH
        self.height = OLED_HEIGHT
        #Initialize DC RST pin
        self._dc = oled_config.DC_PIN
        self._rst = oled_config.RST_PIN
        self._bl = oled_config.BL_PIN



    """    Write register address and data     """
    def command(self, cmd):
        GPIO.output(self._dc, GPIO.LOW)  # pylint: disable=no-member
        oled_config.spi_writebyte([cmd])

    # def data(self, val):
        # GPIO.output(self._dc, GPIO.HIGH)
        # config.spi_writebyte([val])

    def Init(self):
        if (oled_config.module_init() != 0):
            return -1
        """Initialize dispaly"""    
        self.reset()

        self.command(DISPLAY_OFF)           #Display Off
        self.command(SET_CONTRAST_A)        #Set contrast for color A
        self.command(0xFF)                      #145 0x91
        self.command(SET_CONTRAST_B)        #Set contrast for color B
        self.command(0xFF)                      #80 0x50
        self.command(SET_CONTRAST_C)        #Set contrast for color C
        self.command(0xFF)                      #125 0x7D
        self.command(MASTER_CURRENT_CONTROL) #master current control
        self.command(0x06)                      #6
        self.command(SET_PRECHARGE_SPEED_A) #Set Second Pre-change Speed For ColorA
        self.command(0x64)                      #100
        self.command(SET_PRECHARGE_SPEED_B) #Set Second Pre-change Speed For ColorB
        self.command(0x78)                      #120
        self.command(SET_PRECHARGE_SPEED_C) #Set Second Pre-change Speed For ColorC
        self.command(0x64)                      #100
        self.command(SET_REMAP)             #set remap & data format
        self.command(0x72)                      #0x72              
        self.command(SET_DISPLAY_START_LINE) #Set display Start Line
        self.command(0x0) 
        self.command(SET_DISPLAY_OFFSET)    #Set display offset
        self.command(0x0) 
        self.command(NORMAL_DISPLAY)        #Set display mode
        self.command(SET_MULTIPLEX_RATIO)   #Set multiplex ratio
        self.command(0x3F) 
        self.command(SET_MASTER_CONFIGURE)  #Set master configuration
        self.command(0x8E) 
        self.command(POWER_SAVE_MODE)       #Set Power Save Mode
        self.command(0x00)                      #0x00
        self.command(PHASE_PERIOD_ADJUSTMENT) #phase 1 and 2 period adjustment
        self.command(0x31)                      #0x31
        self.command(DISPLAY_CLOCK_DIV)     #display clock divider/oscillator frequency
        self.command(0xF0) 
        self.command(SET_PRECHARGE_VOLTAGE) #Set Pre-Change Level
        self.command(0x3A) 
        self.command(SET_V_VOLTAGE)         #Set vcomH
        self.command(0x3E) 
        self.command(DEACTIVE_SCROLLING)    #disable scrolling
        self.command(NORMAL_BRIGHTNESS_DISPLAY_ON) #set display onH

    def reset(self):
        """Reset the display"""
        GPIO.output(self._rst,GPIO.HIGH) # pylint: disable=no-member
        time.sleep(0.1)
        GPIO.output(self._rst, GPIO.LOW)  # pylint: disable=no-member
        time.sleep(0.1)
        GPIO.output(self._rst, GPIO.HIGH)  # pylint: disable=no-member
        time.sleep(0.1)
        
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        self.command(SET_COLUMN_ADDRESS) 
        self.command(0)          #cloumn start address
        self.command(OLED_WIDTH - 1)  #cloumn end address
        self.command(SET_ROW_ADDRESS) 
        self.command(0)          #page atart address
        self.command(OLED_HEIGHT - 1)  #page end address
    
    def ShowImage(self,Image,Xstart,Ystart):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = np.asarray(Image)
        pix = np.zeros((self.height,self.width,2), dtype = np.uint8)
        pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
        pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0),np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.SetWindows ( 0, 0, self.width, self.height)
        GPIO.output(self._dc, GPIO.HIGH)  # pylint: disable=no-member
        for i in range(0,len(pix),1):
            oled_config.spi_writebyte(pix[i:i+1])		

    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindows ( 0, 0, self.width, self.height)
        GPIO.output(self._dc, GPIO.HIGH)  # pylint: disable=no-member
        for i in range(0,len(_buffer),1):
            oled_config.spi_writebyte(_buffer[i:i+1])		
            #print "%d",_buffer[i:i+4096]
