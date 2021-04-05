#!/usr/bin/python
# coding: utf-8

import time
from AS289R2_m import *
import Image

url = "http://www.nada.co.jp/"
tp = AS289R2_m(Pin(0), 57600)

def demo():
    tp.initialize()
    tp.putLineFeed(2)
    
    tp.printBitmapImage(0x65, 98, Image.image)

    tp.putLineFeed(2)

    tp.printf("** Thermal Printer Shield **\r\r")

    tp.setDoubleSizeWidth()
    tp.printf("  AS-289R2\r\r")
    tp.clearDoubleSizeWidth()

    tp.printf("日本語文字列の印字テスト:24x24\r")
    tp.setKanjiFont(const.KANJI_16x16)
    tp.setANKFont(const.ANK_8x16)
    tp.printf("日本語文字列の印字テスト:16x16\r\r")

    tp.setKanjiFont(const.KANJI_DEFAULT)
    tp.setANKFont(const.ANK_DEFAULT)
    tp.setDoubleSizeWidth()
    tp.printf("ABCDEFG 0123456789\r")
    tp.clearDoubleSizeWidth()

    tp.setDoubleSizeHeight()
    tp.printf("ABCDEFG 0123456789\r")
    tp.clearDoubleSizeHeight()
    tp.putLineFeed(2)

    tp.setANKFont(const.ANK_8x16)
    tp.printf("8x16: Test 012345 ｱｲｳｴｵ\r\r")
    tp.setANKFont(const.ANK_12x24)
    tp.printf("12x24: Test 012345 ｱｲｳｴｵ\r\r")
    tp.setANKFont(const.ANK_16x16)
    tp.printf("16x16: Test 012345 ｱｲｳｴｵ\r\r")
    tp.setANKFont(const.ANK_24x24)
    tp.printf("24x24: Test 012345 ｱｲｳｴｵ\r\r")
    tp.putLineFeed(1)

    tp.setANKFont(const.ANK_8x16)
    tp.printf("QR\r")
    tp.printQRCode(const.QR_ERR_LVL_M, url)
    tp.printf('    ')
    tp.setEnlargedQRCode()
    tp.printQRCode(const.QR_ERR_LVL_M, url)
    tp.clearEnlargedQRCode()
    tp.putLineFeed(1)

    tp.printf("\r{}\r".format(url))
    tp.putLineFeed(2)

    tp.printf("UPC-A\r")
    tp.printBarCode(const.BCODE_UPC_A, "01234567890")
    tp.putLineFeed(4)

while True:
    demo()
    time.sleep(5)
