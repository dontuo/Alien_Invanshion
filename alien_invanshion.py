import utime
import urandom
from machine import Pin, I2C, ADC
import ssd1306
class AlienInvanshion:
    
    def __init__(self):
        #setup display
        i2c = I2C(sda=Pin(4), scl=Pin(5))
        self.display = ssd1306.SSD1306_I2C(64, 48, i2c)
        
        #row and column
        self.row = 3
        self.column = 5
        self.x1 = 0
        self.y1 = 0
        
        self.alienx = 2
        self.alieny = 2
        self.initial_alienx = self.alienx
        self.initial_alieny = self.alieny
        self.alienwidth = 3
        self.alienheight = 3
        
        self.group_aliens = []
        self.group_aliens2 = []
    def start_game(self):
        self._draw_aliens()
        print(self.group_aliens)
        while True:
            self._move_aliens()
            self.display.show()
            
    def _move_aliens(self):
        self.display.fill(0)
        for i in self.group_aliens:
            self.x = i[0]
            self.y = i[1]
            
            if self.x >= 64:self.x1 = 1
            if self.x <= -2: self.x1 = 0
            
            if self.x1: self.x -= 1
            else: self.x += 1

            #utime.sleep(0.01)
            self.display.fill_rect(self.x, self.y, self.alienwidth, self.alienheight, 1)
            #self.display.show()
            print(self.x)
            self.group_aliens2.append([self.x,self.y])

        self.group_aliens = self.group_aliens2
        self.group_aliens2 = []
    def _draw_aliens(self):
        for b in range(self.row):
            for i in range(self.column):
                self.display.fill_rect(self.alienx, self.alieny, self.alienwidth, self.alienheight, 1)
                self.alienx += self.alienwidth + 5
                self.group_aliens.append([self.alienx, self.alieny])
            self.alienx = self.initial_alienx
            self.alieny += self.alienheight + 4
            
        self.alieny = self.initial_alieny

AlienInvanshion().start_game()