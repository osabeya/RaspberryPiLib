# スライドショー
#  Picoにimageフォルダを作成し、BMPファイル（240x240/フルカラー/無圧縮）をお置いておきます。
#  実行するとLCD（ATM0130B3）に順番に表示します。
#
# 注1：めっちゃ遅いです。1枚表示するのに4秒ほどかかります。
# 注2：Picoのストレージは小さいのでBMPは3枚ほどしか置けないでしょう、
# 注3：画像データを1つのFrameBufferに入れるとメモリが足らないので分割して表示してます。
# 注4：dispDat()はFrameBuffer形式のファイルを表示します。
#     BMPをあらかじめFrameBuffer形式のファイルに変換しておき、これで表示すれば高速です。

from atm0130b3 import *
import framebuf
import os, sys, gc
from struct import unpack, pack
import time

SEEK_SET = 0
SEEK_CUR = 1

def dispBMP(fname):
    with open(fname, "rb") as f:
        filetype, = unpack("H", f.read(2))
        if filetype != 0x4D42:
            print(fname+" not BMP")
            sys.exit()
        f.seek(14, SEEK_SET)

        f.seek(4, SEEK_CUR)
        w, = unpack("i", f.read(4))
        h, = unpack("i", f.read(4))
        reverse = True if h > 0 else False
        if h < 0:
            h = -h
        f.seek(2, SEEK_CUR)
        colorbits, = unpack("H", f.read(2))
        if colorbits != 32:
            print(fname+" not Full-color")
            sys.exit()
        compress, = unpack("I", f.read(4))
        if compress != 0:
            print(fname+" compressed")
            sys.exit()
        f.seek(54, SEEK_SET)

        bh = 10000//w//2
        buf = bytearray(w*bh*2)
        if reverse:
            yp = h-bh
        else:
            yp = 0
        for y in range(h):
            if reverse:
                yy = (bh-y%bh-1)
            else:
                yy = y%bh
                
            for x in range(w):
                rgb = f.read(4)
                color = lcd.toColor(rgb[2], rgb[1], rgb[0])
                buf[(x+yy*w)*2] = (color >> 8) & 0xff
                buf[(x+yy*w)*2+1] = color & 0xff
            
            if yy == bh-1 or y == h-1:
                lcd.blit(framebuf.FrameBuffer(buf, w, bh, framebuf.RGB565), 0, yp)
        
                if reverse:
                    yp -= bh
                else:
                    yp += bh
                    
    lcd.show()

def dispDat(fname):
    with open(fname, "rb") as f:
        w, = unpack("i", f.read(4))
        h, = unpack("i", f.read(4))
        
        bh = 10000//w//2
        yp = 0

        while True:
            buf = f.read(w*bh*2)
            if len(buf) == 0:
                break
            lcd.blit(framebuf.FrameBuffer(bytearray(buf), w, bh, framebuf.RGB565), 0, yp)
            yp += bh
                    
    lcd.show()

lcd = LCD_ATM0130B3()
lcd.fill(0)
lcd.show()

while True:
    for file in os.listdir("image"):
        if file.upper().endswith(".BMP"):
            print(file)
            dispBMP("image/"+file)
            
            time.sleep(1)
    
