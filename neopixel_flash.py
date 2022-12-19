from machine import Pin
import neopixel
import random

# LED数
LED_NUM = 256
# DOUTピン
PIN_DOUT = 16

# パラメータ
# 光発生確率
APPEAR = 0.4
# 減光率1
REDUCE1 = 0.87
# 減光率2
REDUCE2 = 0.90
# 最初の明るさ
BRIGHT = 255

# LED
leds = neopixel.NeoPixel(Pin(PIN_DOUT, Pin.OUT), LED_NUM)
leds.fill((0,)*3)
leds.write()

# ピクセルの色番号(0〜7)
colors = {}

# ループ
while True:
    # 乱数が発生確率以下なら発生
    if random.random() <= APPEAR:
        # ピクセル位置
        index = random.randrange(len(leds))

        # 重複していない？
        if not index in colors:
            # 光発生
            leds[index] = (BRIGHT,)*3
            colors[index] = random.randrange(8)
        
    # 光ってるピクセルそれぞれの処理
    for index in colors.keys():
        # 消えている？
        if sum(leds[index]) == 0:
            # 色番号消去
            colors.pop(index)
        else:
            # RGB各減光率
            reduce = (REDUCE1 if colors[index] & 4 else REDUCE2,
                      REDUCE1 if colors[index] & 2 else REDUCE2,
                      REDUCE1 if colors[index] & 1 else REDUCE2)
            # 減光
            (r, g, b) = leds[index]
            leds[index] = (int(r*reduce[0]), int(g*reduce[1]), int(b*reduce[2]))

    leds.write()
    
