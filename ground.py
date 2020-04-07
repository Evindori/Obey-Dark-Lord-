from pygame import*
import os

gr_width = 55
gr_height = 35
gr_color = "#FF6262"
ICON_DIR = os.path.dirname(__file__) 

class Ground(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.begX = x
        self.begY = y
        self.image = Surface((gr_width, gr_height))
        self.image.fill(Color(gr_color))
        self.image = image.load("%s/gr/0.png" % ICON_DIR)
        self.rect = Rect(x, y, gr_width, gr_height)
        self.image.set_colorkey(Color(gr_color))
    def die(self):
        self.rect = Rect(-100, 10000, 1, 1)  
    def restart(self):
        self.rect = Rect(self.begX, self.begY, gr_width, gr_height)

class LevelEnd(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((gr_width, gr_height))
        self.image.fill(Color(gr_color))
        self.image = image.load("%s/gr/le.png" % ICON_DIR)
        self.rect = Rect(x, y, gr_width, gr_height)
        self.image.set_colorkey(Color(gr_color))
