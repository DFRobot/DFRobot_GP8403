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

    def __init__(self, addr, sclpin, sdapin, i2cfreq):
        self._addr = addr
        self.outPutSetRange = 0x01
        self.voltage = 5000
        self._scl = sclpin
        self._sda = sdapin
        self.dataTransmission = 0
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

    def __init__(self, addr, sclpin, sdapin, i2cfreq):
        self._addr = addr
        self.outPutSetRange = 0x01
        self.voltage = 5000
        self._scl = sclpin
        self._sda = sdapin
        self.dataTransmission = 0

        # Initialize I2C with pins
        self.i2c = machine.I2C(0,
                               scl=machine.Pin(sclpin),
                               sda=machine.Pin(sdapin),
                               freq=i2cfreq)

    def begin(self):
        # Initialize the sensor
        if self.i2c.readfrom(self._addr, 1) != 0:
            return 0
        return 1
        # Initialize I2C with Pins
        self.i2c = machine.I2C(0,
                               scl=machine.Pin(sclpin),
                               sda=machine.Pin(sdapin),
                               freq=i2cfreq)

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

    # TODO: change this to bit banging to be in line with
    # spec that is not i2c compliant.
    def store(self):
        """
        Save the present current config, after the config is saved successfully,
        it will be enabled when the module is powered down and restarts
        """
        self.i2c.start()
        self._send_byte(self.GP8302_STORE_TIMING_HEAD)
        self.i2c.stop()
        self.i2c.start()
        self._send_byte(self.GP8302_STORE_TIMING_ADDR)
        self._send_byte(self.GP8302_STORE_TIMING_CMD1)
        self.i2c.stop()

        self.i2c.start()
        self._send_byte(self._addr << 1)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self.i2c.stop()

        utime.sleep(self.GP8302_STORE_TIMING_DELAY)

        self.i2c.start()
        self._send_byte(self.GP8302_STORE_TIMING_HEAD)
        self.i2c.stop()
        self.i2c.start()
        self._send_byte(self.GP8302_STORE_TIMING_ADDR)
        self._send_byte(self.GP8302_STORE_TIMING_CMD2)
        self.i2c.stop()

    def _send_byte(self, data):
        # ensure 8 bits only
        data = data & 0xFF
        return self.i2c.write(data.to_bytes(1, 'big'))
