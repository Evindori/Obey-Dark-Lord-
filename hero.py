from pygame import*
import pyganim

h_speed = 3
h_jspeed = 6
h_width = 60
h_height = 90
COLOR =  "#000000"
h_delay = 0.1
gravity = 0.5

stay_a = [('lordoutfit/0.png', 0.1)]
j_a = [('lordoutfit/j.png', 0.1)]
right_a = [('lordoutfit/r1.png'),
            ('lordoutfit/r2.png'),
            ('lordoutfit/r3.png'),
            ('lordoutfit/r4.png'),
            ('lordoutfit/r5.png')]
left_a = [('lordoutfit/l1.png'),
            ('lordoutfit/l2.png'),
            ('lordoutfit/l3.png'),
            ('lordoutfit/l4.png'),
            ('lordoutfit/l5.png')]
jleft_a = [('lordoutfit/jl.png', 0.1)]
jright_a = [('lordoutfit/jr.png', 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.begX = x
        self.begY = y
        self.xspeed = 0
        self.yspeed = 0
        self.onground = False
        self.alive = True
        self.levelcompleted = False
        self.image = Surface((h_width,h_height))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, h_width, h_height)
        self.image.set_colorkey(Color(COLOR))


        self.boltAnimStay = pyganim.PygAnimation(stay_a)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))
        
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
        
        self.boltAnimJumpRight= pyganim.PygAnimation(jright_a)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJumpLeft= pyganim.PygAnimation(jleft_a)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJump= pyganim.PygAnimation(j_a)
        self.boltAnimJump.play()
        

    def update(self, left, right, up, platforms, enemies, ending):
        
        if up:
            if self.onground:
                self.yspeed = - h_jspeed
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))
               
                       
        if left:
            self.xspeed = - h_speed 
            self.image.fill(Color(COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))
 
        if right:
            self.xspeed = h_speed 
            self.image.fill(Color(COLOR))
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
        self.collide(0, self.yspeed, platforms)
        
        self.rect.x += self.xspeed 
        self.collide(self.xspeed, 0, platforms)
        
        self.ifalive(enemies)
        self.won(ending)
    def ifalive(self, enemies):
        for e in enemies:
            if sprite.collide_rect(self, e):
                self.alive = False
    def won(self, ending):
        for e in ending:
            if sprite.collide_rect(self, e): 
                self.levelcompleted = True
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
