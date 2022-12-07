from atm0130b3 import *
import framebuf

lcd = LCD_ATM0130B3()
lcd.fill(0)

for i in range(8):
    g = 255 * (1 - ((i & 0x04) >> 2))
    r = 255 * (1 - ((i & 0x02) >> 1))
    b = 255 * (1 - ((i & 0x01)))
    
    lcd.fill_rect(i * 30, 0, 30, 180, lcd.toColor(r, g, b))
lcd.show()
