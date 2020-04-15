from pygame import*
import pyganim

h_speed = 3
h_width = 122
h_height = 95
h_delay = 0.1
COLOR =  "#000000"
gravity = 1.5

stay_a = [('knight/0.png', 0.1)]
right_a = ['knight/r1.png',
            'knight/r2.png',
            'knight/r3.png',
            'knight/r4.png']
left_a = ['knight/l1.png',
            'knight/l2.png',
            'knight/l3.png',
            'knight/l4.png']


class Knight(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.begX = x
        self.begY = y
        self.xspeed = 0
        self.yspeed = 0
        self.onground = False
        self.image = Surface((h_width,h_height))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, h_width, h_height)
        self.image.set_colorkey(Color(COLOR))
        
        boltAnim = []
        for anim in right_a:
            boltAnim.append((anim, h_delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
    
        boltAnim = []
        for anim in left_a:
            boltAnim.append((anim, h_delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        
        self.boltAnimStay = pyganim.PygAnimation(stay_a)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))        

    def update(self, hero, platforms):      
        if not self.onground:
            self.yspeed +=  gravity
        else:
            if hero.rect.x < self.rect.x - h_speed:
                self.xspeed = - h_speed 
                self.image.fill(Color(COLOR))
                self.boltAnimLeft.blit(self.image, (0, 0))
     
            elif hero.rect.x > self.rect.x + h_speed:
                self.xspeed = h_speed 
                self.image.fill(Color(COLOR))
                self.boltAnimRight.blit(self.image, (0, 0))
             
            else:
                self.xspeed = 0
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
        self.onground = False
        self.rect.y += self.yspeed
        self.collide(0, self.yspeed, platforms)
        
        self.rect.x += self.xspeed 
        self.collide(self.xspeed, 0, platforms)
    def restart(self):
        self.xspeed = self.yspeed = 0
        self.rect.x = self.begX
        self.rect.y = self.begY
        self.alive = True
        self.onground = False    
    def collide(self, xspeed, yspeed, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xspeed > 0:
                    self.rect.right = p.rect.left
                    self.xspeed = 0

                if xspeed < 0:
                    self.rect.left = p.rect.right
                    self.xspeed = 0

                if yspeed > 0:
                    self.rect.bottom = p.rect.top
                    self.onground = True
                    self.yspeed = 0

                if yspeed < 0:
                    self.rect.top = p.rect.bottom
                    self.yspeed = 0
   
