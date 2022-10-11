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
        self.repeat = 3
        self.row = 5
        self.column = 1
        self.x1 = 0
        self.y1 = 0
        
        self.alienx = 2
        self.alieny = 2
        self.initial_alienx = self.alienx
        self.initial_alieny = self.alieny
        self.alienwidth = 3
        self.alienheight = 3
        
        self.group_aliens = []
        self.group_layer1 = []
        self.group_layer2 = []
        self.group_layer3 = []
        
        self.group_aliens1 = []
        self.group_layer11 = []
        self.group_layer21 = []
        self.group_layer31 = []
        
        self.num_group = 1
    def start_game(self):
        
        self._draw_aliens()
        
        while True:
            self.display.fill(0)
            self._move_aliens()
            self.display.show()
            
            
    def _move_aliens(self):
        self.num_group = 1
        for i in self.group_aliens:
            for a in i:
                self.x = a[0]
                self.y = a[1]
                
                if self.x >= 64: self.x1 = 1
                elif self.x <= -2: self.x1 = 0
                
                if self.x1: self.x -= 1
                else: self.x += 1
                
                self.display.fill_rect(self.x, self.y, self.alienwidth, self.alienheight, 1)
                if self.num_group == 1:
                    self.group_layer11.append([self.x, self.y])
                elif self.num_group == 2:
                    self.group_layer21.append([self.x, self.y])
                elif self.num_group == 3:
                    self.group_layer31.append([self.x, self.y])
                    
        self.group_aliens1.append(self.group_layer11)
        self.group_aliens1.append(self.group_layer21)
        self.group_aliens1.append(self.group_layer31)
        self.group_layer11 = []
        self.group_layer21 = []
        self.group_layer31 = []
        self.group_aliens = self.group_aliens1
        self.group_aliens1 = []
    def _draw_aliens(self):
        for b in range(self.repeat):
            for i in range(self.row):
                # малюєм прибульця
                self.display.fill_rect(self.alienx, self.alieny, self.alienwidth, self.alienheight, 1)
                # робим відступ від минулого прибульця
                self.alienx += self.alienwidth + 5
                # додавання координат прибульців
                if self.num_group == 1: self.group_layer1.append([self.alienx, self.alieny])
                elif self.num_group == 2: self.group_layer2.append([self.alienx, self.alieny])
                elif self.num_group == 3: self.group_layer3.append([self.alienx, self.alieny])
            
            self.num_group += 1
            # вертаєм координату прибульця x на початкові координати
            self.alienx = self.initial_alienx
            # перехід на наступний ряд
            self.alieny += self.alienheight + 5
        # вертаєм координати прибульця x та y на початкові координати
        self.alieny = self.initial_alieny
        self.alienx = self.initial_alienx
        # додавання всіх списків в 1
        self.group_aliens.append(self.group_layer1)
        self.group_aliens.append(self.group_layer2)
        self.group_aliens.append(self.group_layer3)

AlienInvanshion().start_game()
