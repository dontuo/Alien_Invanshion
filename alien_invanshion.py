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
        self.row = 2
        self.column = 4
        self.x1 = 0
        self.y1 = 0
        # alien
        self.alienx = 3
        self.alieny = 3
        self.initial_alienx = self.alienx
        self.initial_alieny = self.alieny
        self.alienwidth = 3
        self.alienheight = 3
        self.group_aliens = []
        self.group_aliens2 = []
        self.dead_aliens = []
        self.game_over = 1
        # ship
        self.shipx = 64 //2
        self.shipy = 36
        self.ship_rectx = 4
        self.ship_recty = 4
        self.add_alien = 1
        self.scaled_value = self.shipx
        # bullet
        self.bulletx = self.shipx + 1
        self.bullety = self.shipy + self.ship_recty
        self.bullet_rectx = 3
        self.bullet_recty = 2
        
        #health
        self.health = 3
        self.healthx = 2
        self.healthy = 2
        self.health_rectx = 2
        self.health_recty = 2
        # score
        self.score = 0
    def start_game(self):
        # початок гри та головний цикл
        self._draw_aliens()
        while self.game_over:
            if not self.health:
                self.game_over = 0
            self.map()
            self._move_aliens()
            self._draw_bullet()
            self._draw_ship()
            self._draw_score()
            self._draw_health()
            #self.display.invert(1)
            #utime.sleep(0.3)
            self.display.show()
            
            
        self.display.fill(0)
        
        self.display.text("Game", 3,3,1)
        self.display.text("over", 3, 13, 1)
        self.display.text(f"score:", 3, 23, 1)
        self.display.text(f"{self.score}", 3, 33, 1)
        self.display.show()
            
    def _move_aliens(self):
        self.display.fill(0)
        #рух прибульців
        if self.group_aliens:
            for i in self.group_aliens:
                self.x = i[0]
                self.y = i[1]
                
                self.num_alien = 0
                # перевірка вектора прибульців
                for b in self.group_aliens:
                    self.b1 = b[0]
                    self.b2 = b[1]
                    if self.b1 >= 64 - self.alienwidth:self.x1 = 1; self.y1 = 1; break
                    if self.b1 <= 0: self.x1 = 0; self.y1 = 1; break
                    if self.b2 >= 48 - self.alienheight: self.health -= 1; self.group_aliens = []
                    if self.b2 + self.ship_recty >= self.shipy:
                        if self.b1 >= self.shipx and self.b1 <= self.shipx + self.ship_rectx:
                            self.health -= 1; self.group_aliens = []
                    
                if self.x1: self.x -= 1
                else: self.x += 1
                if self.y1: self.y += self.alienwidth; self.y1 = 0

                if self.y  >= self.bullety and self.y + 3 <= self.bullety + self.bullet_recty:
                    if self.x >= self.bulletx and self.x <= self.bulletx + self.bullet_rectx:
                        self.bullety = self.shipy - 1; self.bulletx = self.shipx; self.score += 1
                    else: self.group_aliens2.append([self.x,self.y])
                elif self.y + 3 >= self.bullety and self.y + 3 <= self.bullety + self.bullet_recty:
                    if self.x >= self.bulletx and self.x + 3 <= self.bulletx + self.bullet_rectx:
                        self.bullety = self.shipy - 1; self.bulletx = self.shipx; self.score += 1
                    else: self.group_aliens2.append([self.x,self.y])
                elif self.y + 3 >= self.bullety and self.y <= self.bullety + self.bullet_recty:
                    if self.x >= self.bulletx and self.x + 3 <= self.bulletx + self.bullet_rectx:
                        self.bullety = self.shipy - 1; self.bulletx = self.shipx; self.score += 1
                    else: self.group_aliens2.append([self.x,self.y])
                elif self.y >= self.bullety and self.y <= self.bullety+ self.bullet_rectx:
                    if self.x + 3 >= self.bulletx and self.x + 3 <= self.bulletx:
                        self.bullety = self.shipy- 1; self.bulletx = self.shipx; self.score += 1
                    else: self.group_aliens2.append([self.x,self.y])
                else: self.group_aliens2.append([self.x,self.y])
            
                # намалювати прибульця
                self.display.fill_rect(self.x, self.y, self.alienwidth, self.alienheight, 1)
                #self.display.show()
                # добавлення прибульця в допоміжний список
             
            if self.group_aliens:
                self.group_aliens = self.group_aliens2
                self.group_aliens2 = []
            else:
                self.display.fill(0)
                self.group_aliens = []
                self.group_aliens2 = []
            
        else: self.group_aliens = [];self.group_aliens2 = [];self._draw_aliens(); self.bullety = self.shipy + 1; utime.sleep(1)
    def _draw_aliens(self):
        # малює всіх прибульців та задає їм координати
        for i in range(self.row):
            for b in range(self.column):
                self.display.fill_rect(self.alienx, self.alieny, self.alienwidth, self.alienheight, 1)
                self.alienx += self.alienwidth + 5
                self.group_aliens.append([self.alienx, self.alieny])
            self.alienx = self.initial_alienx
            self.alieny += self.alienheight + 4
            
        self.alieny = self.initial_alieny
        
    def _draw_ship(self):
        self.display.fill_rect(self.shipx, self.shipy, self.ship_rectx, self.ship_recty, 1)
        self.shipx = self.scaled_value
    def _draw_bullet(self):
        self.display.fill_rect(self.bulletx, self.bullety, self.bullet_recty,self.bullet_rectx, 1)
        if self.bullety <= 0:
            self.bullety = self.shipy + 1
            self.bulletx = self.shipx
        else: self.bullety -= 1
    
    def _draw_score(self):
        self.display.text(f"{self.score}", 45, 2, 1)
    
    def _draw_health(self):
        for i in range(0, self.health):
            self.display.fill_rect(self.healthx, self.healthy, self.health_rectx, self.health_recty, 1)
            self.healthx += self.health_rectx + 2
        self.healthx = 2
    def map(self):
        adc = ADC(0)
        self.scaled_value = (adc.read() - 0) * (60 - 0) // (1024 - 0) + 0

AlienInvanshion().start_game()
