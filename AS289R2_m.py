##
# AS-289R2_m Thermal Printer Shield for Raspberry Pi Pico
#
# This is a variation of the "AS289R2" written in CPP by
# Toyomasa Watarai and the code is ported to MicroPython.
#
# NADA ELECTRONICS, LTD.
# Copyright (c) 2021 Tomoaki Tabuchi, MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


##
# @file    AS289R2.cpp
# @author  Toyomasa Watarai
# @version V1.1.0
# @date    20 January 2020
# @brief   AS289R2 class implementation
# ****************************************************************************
# @attention
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


#!/usr/bin/python
# coding: utf-8

from machine import UART,Pin
import sys

##
# @class const
# @brief Constants in Python
class const:
    class _ConstTypeError(TypeError):
        pass
    def __repr__(self):
        return "Constant type definitions."
    def __setattr__(self, name, value):
        v = self.__dict__.get(name, value)
        if type(v) is not type(value):
            raise self._ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value
    def __del__(self):
        self.__dict__.clear()

sys.modules[__name__] = const()

##
# Kanji_font_size
## 24x24 dot font
const.KANJI_24x24 = 0x30
## 16x16 dot font
const.KANJI_16x16 = 0x31
## Default font size
const.KANJI_DEFAULT = const.KANJI_24x24

##
# ANK_font_size
## 8x16 dot font
const.ANK_8x16 = 0x30
## 12x24 dot font
const.ANK_12x24 = 0x31
## 16x16 dot font
const.ANK_16x16 = 0x32
## 24x24 dot font
const.ANK_24x24 = 0x33
## Default font size
const.ANK_DEFAULT = const.ANK_12x24

##
# QR_ERR_LVL
## Error correction lebel L (7%)
const.QR_ERR_LVL_L = 0x4C
## Error correction lebel M (15%)
const.QR_ERR_LVL_M = 0x4D
## Error correction lebel Q (25%)
const.QR_ERR_LVL_Q = 0x51
## Error correction lebel H (30%)
const.QR_ERR_LVL_H = 0x48

##
# BARCODE_MODE
## UPC-A : 11-digit, d1-d11, C/D.
const.BCODE_UPC_A = 0x30
## JAN13 : 12-digit, d1-d12, C/D.
const.BCODE_JAN13 = 0x32
## JAN8 : 7-digit, d1-d7, C/D.
const.BCODE_JAN8 = 0x33
## CODE39 : variable, d1-d20, C/D.
const.BCODE_CODE39 = 0x34
## ITF : variable, d1-d20. 
const.BCODE_ITF = 0x35
## CODABAR (NW7) : variable, d1-d20. 
const.BCODE_CODABAR = 0x36

##
# SCRIPT_MODE
## Cancel script mode
const.SCRIPT_CANCEL = 0
## Super script
const.SCRIPT_SUPER = 1
## Sub script
const.SCRIPT_SUB = 2

##
# @class AS289R2_m
# @brief A printer interface for driving AS-289R2 thermal printer shield of NADA Electronics, Ltd. 
class AS289R2_m():
    ##
    # @brief Create a AS289R2 instance which is connected to specified Serial pin with specified baud rate. 
    # @param self object pointer 
    # @param tx Serial TX pin
    # @param baud (option) serial baud rate (default: 57    600bps) 
    def __init__(self, _tx, baud=57600):
        self._serial = UART(
            0, #id?
            tx=_tx,
            baudrate=baud,
            bits=8,
            parity=None,
            stop=1,
        )
        self.initialize()

    ##
    # @brief Destructor of AS289R2. 
    # @param self object pointer 
    def __del__(self):
        self._serial.close()

    ##
    # @fn initialize(self)
    # @brief Initialize AS289R2.
    # @param self object pointer 
    def initialize(self):
        self.putc(0x1B)
        self.putc(0x40)

    ##
    # @fn putLineFeed(self, lines)
    # @brief Send line feed code which is connected to specified Serial pin with specified baud rate. 
    # @param self object pointer 
    # @param lines Number of line feed 
    def putLineFeed(self, lines):
        for i in range(lines):
            self._serial.write(b'\r')

    ##
    # @fn clearBuffer(self)
    # @brief Clear image buffer of the AS-289R2.
    # @param self object pointer
    def clearBuffer(self):
        self.putc(0x18)

    ##
    # @fn setDoubleSizeHeight(self)
    # @brief Set double height size font. 
    # @param self object pointer
    def setDoubleSizeHeight(self):
        self._serial.write(b'\x1B\x4E\x31')

    ##
    # @fn clearDoubleSizeHeight(self)
    # @brief Set normal height size font.
    # @param self object pointer
    def clearDoubleSizeHeight(self):
        self._serial.write(b'\x1B\x4E\x30')

    ##
    # @fn setDoubleSizeWidth(self)
    # @brief Set double width size font. 
    # @param self object pointer
    def setDoubleSizeWidth(self):
        self._serial.write(b'\x1B\x57\x31')

    ##
    # @fn clearDoubleSizeWidth(self)
    # @brief Set normal width size font.
    # @param self object pointer
    def clearDoubleSizeWidth(self):
        self._serial.write(b'\x1B\x57\x30')

    ##
    # @fn setLargeFont(self)
    # @brief Set large size font (48x96)
    # @param self object pointer
    def setLargeFont(self):
        self._serial.write(b'\x1B\x4C\x31')

    ##
    # @fn clearLargeFont(self)
    # @brief Set normal size font. 
    # @param self object pointer
    def clearLargeFont(self):
        self._serial.write(b'\x1B\x4C\x30')

    ##
    # @fn setANKFont(self, font)
    # @brief Set ANK font. 
    # @param self object pointer
    # @param font ANK font
    def setANKFont(self, font):
        self.putc(0x1B)
        self.putc(0x68)
        self.putc(font)

    ##
    # @fn setKanjiFont(self, font)
    # @brief Set Kanji font size. 
    # @param self object pointer
    # @param font Kanji font
    def setKanjiFont(self, font):
        self.putc(0x12)
        self.putc(0x53)
        self.putc(font)

    ##
    # @fn printQRCode(self, err, param)
    # @brief Print QR code. 
    # @param self object pointer
    # @param err QR code error correction level
    # @param param Data to be printed
    def printQRCode(self, err, param):
        l = len(param)
        buf = [0x1D, 0x78, err, l]

        for i in range(len(buf)):
            self.putc(buf[i])

        self._serial.write(param.encode())

    ##
    def setEnlargedQRCode(self):
        buf = [0x1D, 0x79, 0x31]
        for i in range(len(buf)):
            self.putc(buf[i])

    ##
    def clearEnlargedQRCode(self):
        buf = [0x1D, 0x79, 0x30]
        for i in range(len(buf)):
            self.putc(buf[i])

    ##
    # @fn printBarCode(self, code, param)
    # @brief printBarCode
    # @param self object pointer
    # @param code Type of Bar code
    # @param param Data to be printed 
    def printBarCode(self, code, param):
        buf = [0x1D, 0x6B, code]

        for i in range(len(buf)):
            self.putc(buf[i]);

        self._serial.write(param.encode())
        self.putc(0x00)

    ##
    # @fn printBitmapImage(self, mode, lines, image)
    # @brief Print bitmap image.
    # @param self object pointer
    # @param mode Type of operation mode, 0x61: print image buffer, 0x62: register image buffer, 0x63: register -> print, 0x64: print -> register, 0x65: line print
    # @param lines Number of print line
    # @param image Data to be printed
    def printBitmapImage(self, mode, lines, image):
        buf = [0x1C, 0x2A, mode]

        for i in range(len(buf)):
            self.putc(buf[i]);

        self.putc((lines >> 8) & 0xFF) # n1
        self.putc((lines >> 0) & 0xFF) # n2

        if mode == 0x61: return

        for i in range(48 * lines):
            self.putc(image[i]);

    ##
    # @fn setLineSpaceing(self, space)
    # @brief Set Line Spaceing. 
    # @param self object pointer
    # @param space line spacing
    def setLineSpaceing(self, space):
        self.putc(0x1B)
        self.putc(0x33)
        self.putc(space)

    ##
    # @fn defaultLineSpaceing(self)
    # @brief Set as default Line Spaceing. 
    # @param self object pointer
    def defaultLineSpaceing(self):
        self._serial.write(b'\x1b\x33\x04')

    ##
    # @fn setPrintDirection(self, direction)
    # @brief Set Print Direction.
    # @param self object pointer
    # @param direction Print direction, 0: lister, 1: texter
    def setPrintDirection(self, direction):
        self.putc(0x1B)
        self.putc(0x49)
        self.putc(direction)

    ##
    # @fn putPaperFeed(self, space)
    # @brief Send feed code.
    # @param self object pointer
    # @param space Paper feed
    def putPaperFeed(self, space):
        self.putc(0x1B)
        self.putc(0x4A)
        self.putc(space)

    ##
    # @fn setInterCharacterSpace(self, space)
    # @brief Set Inter Character Space.
    # @param self object pointer
    # @param space inter-character space
    def setInterCharacterSpace(self, space):
        self.putc(0x1B)
        self.putc(0x20)
        self.putc(space)

    ##
    # @fn defaultInterCharacterSpace(self)
    # @brief Set as default Inter Character Space.
    # @param self object pointer
    def defaultInterCharacterSpace(self):
        self._serial.write(b'\x1B\x20\x01')

    ##
    # @fn putPrintPosition(self, position)
    # @brief Send Print Position. 
    # @param self object pointer
    # @param position Print position
    def putPrintPosition(self, position):
        self.putc(0x1B)
        self.putc(0x6c)
        self.putc(position)

    ##
    # @fn setScript(self, script)
    # @brief Set Script.
    # @param self object pointer
    # @param script mode e.g. SCRIPT_MODE.SCRIPT_SUPER
    def setScript(self, script):
        self.putc(0x1B)
        self.putc(0x73)
        self.putc(script)

    ##
    # @fn clearScript(self)
    # @brief Clear Script.
    # @param self object pointer
    def clearScript(self):
        self._serial.write(b'\x1B\x73\x30')

    ##
    # @fn setQuadrupleSize(self)
    # @brief Set Quadruple size.
    # @param self object pointer
    def setQuadrupleSize(self):
        self._serial.write(b'\x1C\x57\x31')

    ##
    # @fn clearQuadrupleSize(self)
    # @brief Clear Quadruple size. 
    # @param self object pointer
    def clearQuadrupleSize(self):
        self._serial.write(b'\x1C\x57\x30')

    ##
    # @fn setEnlargement(self, width, height)
    # @brief Set Enlargement size.
    # @param self object pointer
    # @param width enlargement
    # @param height enlargement
    def setEnlargement(self, width, height):
        self.putc(0x1C)
        self.putc(0x65)
        self.putc(width)
        self.putc(height)

    ##
    # @fn clearEnlargement(self)
    # @brief Clear Enlargement size. 
    # @param self object pointer
    def clearEnlargement(self):
        self._serial.write(b"\x1C\x65\x31\x31");

    ##
    # @fn setBarCodeHeight(self, height)
    # @brief Set BarCode Height size. 
    # @param self object pointer
    # @param height Bar height 
    def setBarCodeHeight(self, height):
        self.putc(0x1D);
        self.putc(0x68);
        self.putc(height);

    ##
    # @fn defaultBarCodeHeight(self)
    # @brief Set as default BarCode Height size. 
    # @param self object pointer
    def defaultBarCodeHeight(self):
        self._serial.write(b"\x1D\x68\x50");

    ##
    # @fn setBarCodeBarSize(self, narrowbar, widebar)
    # @brief Set BarCode Bar size. 
    # @param self object pointer
    # @param narrowbar narrow bars size
    # @param widebar wide bars size
    def setBarCodeBarSize(self, narrowbar, widebar):
        self.putc(0x1D);
        self.putc(0x77);
        self.putc(narrowbar);
        self.putc(widebar);

    ##
    # @fn defaultBarCodeBarSize(self)
    # @brief Set as default BarCode Bar size. 
    # @param self object pointer
    def defaultBarCodeBarSize(self):
        self._serial.write(b"\x1D\x77\x02\x05");

    ##
    # @fn putc(self, value: int)
    # @brief Send data
    # @param self object pointer
    # @param value data to send
    def putc(self, value: int):
        self._serial.write(value.to_bytes(1, "big"))

    ##
    # @fn printf(self, s: str)
    # @brief Send data
    # @param self object pointer
    # @param s data to send
    def printf(self, s: str):
        self._serial.write(s.encode())
