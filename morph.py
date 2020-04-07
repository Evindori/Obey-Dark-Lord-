from pygame import*
import pyganim

h_speed = 7
h_jspeed = 6
h_width = 40
h_height = 60
COLOR =  "#000000"
h_delay = 0.1
gravity = 0.5

stay_f_a = [('morphoutfit/0.png'), 0.1]
stay_a = [('morphoutfit/0.png'),
          ('morphoutfit/1.png')]
j_a = [('morphoutfit/j.png', 0.1)]
right_a = [('morphoutfit/r1.png'),
            ('morphoutfit/r2.png'),
            ('morphoutfit/r3.png'),
            ('morphoutfit/r4.png'),
            ('morphoutfit/r5.png')]
left_a = [('morphoutfit/l1.png'),
            ('morphoutfit/l2.png'),
            ('morphoutfit/l3.png'),
            ('morphoutfit/l4.png'),
            ('morphoutfit/l5.png')]
jleft_a = [('morphoutfit/jl.png', 0.1)]
jright_a = [('morphoutfit/jr.png', 0.1)]

left_eat_a = [('morphoutfit/le1.png'),
            ('morphoutfit/le2.png'),
            ('morphoutfit/le3.png')]

right_eat_a = [('morphoutfit/re1.png'),
            ('morphoutfit/re2.png'),
            ('morphoutfit/re3.png')]
d_a = [('morphoutfit/d.png', 0.1)]

class Morph(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.begX = x
        self.begY = y
        self.xspeed = 0
        self.yspeed = 0
        self.onground = False
        self.alive = True
        self.image = Surface((h_width,h_height))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, h_width, h_height)
        self.image.set_colorkey(Color(COLOR))
        

        boltAnim = []
        for anim in stay_a:
            boltAnim.append((anim, h_delay*1.5))
        self.boltAnimStay = pyganim.PygAnimation(boltAnim)
        self.boltAnimStay.play()
        
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
        
        boltAnim = []
        for anim in left_eat_a:
            boltAnim.append((anim, h_delay))
        self.boltAnimLeftEat = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeftEat.play()  
        
        boltAnim = []
        for anim in right_eat_a:
            boltAnim.append((anim, h_delay))
        self.boltAnimRightEat = pyganim.PygAnimation(boltAnim)
        self.boltAnimRightEat.play()        
        
        self.boltAnimJumpRight = pyganim.PygAnimation(jright_a)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJumpLeft = pyganim.PygAnimation(jleft_a)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJump = pyganim.PygAnimation(j_a)
        self.boltAnimJump.play()
        
        self.boltAnimDeath = pyganim.PygAnimation(d_a)
        self.boltAnimDeath.play()        
             

    def update(self, left, right, up, food, platforms, enemies):
        if self.alive:
            if up:
                if self.onground:
                    self.yspeed = - h_jspeed
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
                   
                           
            if left:
                self.xspeed = - h_speed 
                self.image.fill(Color(COLOR))
                if food:
                    self.boltAnimLeftEat.blit(self.image, (0, 0))    
                else:
                    self.boltAnimLeft.blit(self.image, (0, 0))
     
            if right:
                self.xspeed = h_speed 
                self.image.fill(Color(COLOR))
                if food:
                    self.boltAnimRightEat.blit(self.image, (0, 0))    
                else:
                    self.boltAnimRight.blit(self.image, (0, 0))
             
            if not(left or right):
                self.xspeed = 0
                if not up:
                    self.image.fill(Color(COLOR))
                    self.boltAnimStay.blit(self.image, (0, 0))
                
            if not self.onground:
                self.yspeed +=  gravity
                
            self.onground = False
            self.rect.y += self.yspeed
            self.collide(0, self.yspeed, food, platforms)
            
            self.rect.x += self.xspeed 
            self.collide(self.xspeed, 0, food, platforms)
            
            self.ifalive(enemies)
        else:
            if not self.onground:
                self.yspeed += gravity
                self.rect.y += self.yspeed
                self.collide(0, self.yspeed, food, platforms)
            self.image.fill(Color(COLOR))
            self.boltAnimDeath.blit(self.image, (0, 0))            
    def ifalive(self, enemies):
        for e in enemies:
            if sprite.collide_rect(self, e):
                self.alive = False
    def restart(self):
        self.xspeed = self.yspeed = 0
        self.rect.x = self.begX
        self.rect.y = self.begY
        self.alive = True
        self.onground = False
    def collide(self, xspeed, yspeed, food, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if food:
                    p.die()
                else:
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
   
