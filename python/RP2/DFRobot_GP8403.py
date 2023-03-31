# -*- coding: utf-8 -*
"""
@file  DFRobot_GP8403.py
@brief This is a function library of the DAC module.
@copyright  Copyright (c) 2023 Couillonnade
@license  The MIT License (MIT)
@author  [Rémi]
@version  V1.0
@date  2023-03-29
@url  https://github.com/couillonnade/DFRobot_GP8403
"""

import machine
import utime
import ustruct
import sys

# Select DAC output voltage of 0-5V
OUTPUT_RANGE_5V = 0
# Select DAC output voltage of 0-10V
OUTPUT_RANGE_10V = 17
# Select to output from channel 0
CHANNEL0 = 1
# Select to output from channel 1
CHANNEL1 = 2
# Select to output from all the channels
CHANNELALL = 3


class DfrobotGP8403():
    # Configure current sensor register
    GP8403_CONFIG_CURRENT_REG = 0x02
    # Store function timing start head
    GP8302_STORE_TIMING_HEAD = 0x02
    # The first address for entering store timing
    GP8302_STORE_TIMING_ADDR = 0x10
    # The command 1 to enter store timing
    GP8302_STORE_TIMING_CMD1 = 0x03
    # The command 2 to enter store timing
    GP8302_STORE_TIMING_CMD2 = 0x00
    # Total I2C communication cycle 5us
    I2C_CYCLE_TOTAL = 0.000005
    # The first half cycle of the total I2C communication cycle 2us
    I2C_CYCLE_BEFORE = 0.000002
    # The second half cycle of the total I2C communication cycle 3us
    I2C_CYCLE_AFTER = 0.000003
    # Store procedure interval delay time: 10ms, more than 7ms
    GP8302_STORE_TIMING_DELAY = 10


    def __init__(self, addr, sclpin, sdapin, i2cfreq, hard = False):
        """
        Initilize the I2C bus.
        On Pico, Software I2C (using bit-banging) works on all output-capable pins
        :param addr: I2C address
        :param sclpin: SCL pin
        :param sdapin: SDA pin
        :param i2cfreq: I2C frequency
        :param hard: I2C or SoftI2C
        """

        self._addr = addr
        self.outPutSetRange = 0x01
        self.voltage = 5000
        self._scl = machine.Pin(sclpin)
        self._sda = machine.Pin(sdapin)
        self._i2cfreq = i2cfreq
        self.dataTransmission = 0
        self._hard = hard

        self._initializeI2C()

    def _initializeI2C(self):
        if self._hard:
            self.i2c = machine.I2C(0,
                                   scl=self._scl,
                                   sda=self._sda,
                                   freq=self._i2cfreq)
        else:
            # Pylance is not happy with this because stubs are wrong.
            # see: https://github.com/paulober/Pico-W-Go/issues/55
            self.i2c = machine.SoftI2C(scl=self._scl,
                                sda=self._sda,
                                freq=self._i2cfreq)


    def begin(self):
        # Initialize the sensor
        if self.i2c.readfrom(self._addr, 1) != 0:
            return 0
        return 1

    def set_dac_out_range(self, mode):
        """
        Set DAC output range
        :param mode: 5V or 10V OUTPUT_RANGE mode
        """
        if mode == OUTPUT_RANGE_5V:
            self.voltage = 5000
        elif mode == OUTPUT_RANGE_10V:
            self.voltage = 10000
        self.i2c.writeto_mem(self._addr, self.outPutSetRange, mode)

    def set_dac_out_voltage(self, data, channel):
        """
        Select DAC output channel & range
        :param data: Set output data
        :param channel: Set output channel
        """
        self.dataTransmission = ((float(data) / self.voltage) * 4095)
        self.dataTransmission = int(self.dataTransmission) << 4
        self._send_data(self.dataTransmission, channel)

    def _send_data(self, data, channel):
        if channel == 0:
            self.i2c.writeto_mem(self._addr, self.GP8403_CONFIG_CURRENT_REG, data)

        elif channel == 1:
            self.i2c.writeto_mem(self._addr, self.GP8403_CONFIG_CURRENT_REG << 1, data)
        else:
            self.i2c.writeto_mem(self._addr, self.GP8403_CONFIG_CURRENT_REG, data)
            self.i2c.writeto_mem(self._addr, self.GP8403_CONFIG_CURRENT_REG << 1, data)


    def store(self):
        """
        Save the present current config, after the config is saved successfully,
        it will be enabled when the module is powered down and restarts
        
        This is done with bit-banging because the chip does custom I2C with less than 1 Byte data.
        """
        
        # Re-initialise Pin because it was initialized 
        # with SoftI2C and we need to use it as GPIO
        self._scl = machine.Pin(self._scl, machine.Pin.OUT)
        self._sda = machine.Pin(self._sda, machine.Pin.OUT)

        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_HEAD, 0, 3, False)
        self._stop_signal()
        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_ADDR)
        self._send_byte(self.GP8302_STORE_TIMING_CMD1)
        self._stop_signal()

        self._start_signal()
        self._send_byte(self._addr<<1, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2, 1)
        self._stop_signal()

        utime.sleep(self.GP8302_STORE_TIMING_DELAY)

        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_HEAD, 0, 3, False)
        self._stop_signal()
        self._start_signal()
        self._send_byte(self.GP8302_STORE_TIMING_ADDR)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._stop_signal()

        # re-initialize I2C
        self._initializeI2C()


    def _start_signal(self):
        self._scl.high()
        self._sda.high()
        utime.sleep(self.I2C_CYCLE_BEFORE)
        self._sda.low()
        utime.sleep(self.I2C_CYCLE_AFTER)
        self._scl.low()
        utime.sleep(self.I2C_CYCLE_TOTAL)
  
    def _stop_signal(self):
        self._sda.low()
        utime.sleep(self.I2C_CYCLE_BEFORE)
        self._scl.high()
        utime.sleep(self.I2C_CYCLE_TOTAL)
        self._sda.high()
        utime.sleep(self.I2C_CYCLE_TOTAL)

    def _recv_ack(self, ack = 0):
        ack_ = 0
        error_time = 0
        self._sda = machine.Pin(self._sda, machine.Pin.IN)

        utime.sleep(self.I2C_CYCLE_BEFORE)
        self._scl.high()
        utime.sleep(self.I2C_CYCLE_AFTER)
        while self._sda.value() != ack:
            utime.sleep(0.000001)
            error_time += 1
            if error_time > 250:
                break
        ack_ = self._sda.value() # suspicious to read the value here, should save it before the while loop?
        utime.sleep(self.I2C_CYCLE_BEFORE)
        self._scl.low()
        utime.sleep(self.I2C_CYCLE_AFTER)
        self._sda = machine.Pin(self._sda, machine.Pin.OUT)
        return ack_

    def _send_byte(self, data, ack = 0, bits = 8, flag = True):
        i = bits
        # Ensure 8 bits only
        data = data & 0xFF
        while i > 0:
            i -= 1
            if data & (1 << i):
                self._sda.high()
            else:
                self._sda.low()
            utime.sleep(self.I2C_CYCLE_BEFORE)
            self._scl.high()
            utime.sleep(self.I2C_CYCLE_TOTAL)
            self._scl.low()
            utime.sleep(self.I2C_CYCLE_AFTER)
        if flag:
            return self._recv_ack(ack)
        else:
            self._sda.low()
            self._scl.high()
        return ack