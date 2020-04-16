import pygame
import time
import hero
import morph
import knight
import ground
import os
from ground import LevelEnd, Ground
from hero import Player
from morph import Morph
from knight import Knight

height = 463
width = 900
level_amount = 2
gr_width = 55
gr_height = 35

FILE_DIR = os.path.dirname(__file__)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + width / 2, -t + height / 2

    l = min(0, l)
    l = max(-(camera.width - width), l)
    t = max(-(camera.height - height), t)

    return pygame.Rect(l, t, w, h)


def load_level(n,
               level,
               morphs,
               entities,
               enemies,
               playerX,
               playerY):
    c_level = "%s\levels\level" + str(n) + ".txt"
    levelfile = open(c_level % FILE_DIR)
    line = " "
    tasks = []
    while line[0] != "/":
        line = levelfile.readline()
        if line[0] == '[':
            line = levelfile.readline()
            while line[0] != "]":
                ending = line.find("|")
                level.append(line[0: ending])
                line = levelfile.readline()
        if line[0] != '':
            charecters = line.split()
            if charecters[0] == 'player':
                playerX = int(charecters[1])
                playerY = int(charecters[2])
            if charecters[0] == 'morph':
                m = Morph(int(charecters[1]), int(charecters[2]))
                entities.add(m)
                morphs.add(m)
            if charecters[0] == 'knight':
                k = Knight(int(charecters[1]), int(charecters[2]))
                entities.add(k)
                enemies.add(k)


def death(hero, morphs, grave, enemies):
    for morph in morphs:
        morph.restart()
    hero.restart()
    for g in grave:
        g.restart()
    for e in enemies:
        e.restart()


def screen_saver(done):
    pygame.init()
    started = False
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Obey Dark Lord")
    bg = pygame.Surface((width, height))

    background_image = pygame.image.load("screensaver.jpg").convert()
    while not started and not done:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                started = True
            if e.type == pygame.QUIT:  # event handling
                done = True
            screen.blit(background_image, (0, 0))
        pygame.display.update()
    return done


def main(done):
    background_image = pygame.image.load("bg.png").convert()

    for i in range(level_amount):
        level = []
        pygame.mixer.music.load(str(i) + '.mp3')
        pygame.mixer.music.play(-1)
        entities = pygame.sprite.Group()
        grave = []
        morphs = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        ending = pygame.sprite.Group()
        playerX = playerY = 100
        load_level(i + 1,
                   level,
                   morphs,
                   entities,
                   enemies,
                   playerX,
                   playerY)
        hero = Player(playerX, playerY)
        entities.add(hero)
        x = 0
        y = 0
        for row in level:
            for col in row:
                if col == "-":
                    pf = Ground(x, y)
                    entities.add(pf)
                    grave.append(pf)
                if col == "E":
                    e = LevelEnd(x, y)
                    entities.add(e)
                    ending.add(e)
                x += gr_width
            y += gr_height
            x = 0

        timer = pygame.time.Clock()
        left = right = up = 0
        morph_left = morph_right = morph_up = food = 0
        total_level_width = len(level[0]) * gr_width
        total_level_height = len(level) * gr_height
        camera = Camera(camera_configure,
                        total_level_width,
                        total_level_height)
        while (not hero.levelcompleted) and (not done):
            timer.tick(30)
            if hero.alive:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:  # event handling
                        done = True

                    if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                        up = True
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                        left = True
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                        right = True
                    if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                        up = False
                    if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                        right = False
                    if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                        left = False

                    if e.type == pygame.KEYDOWN and e.key == pygame.K_w:
                        morph_up = True
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                        morph_left = True
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                        morph_right = True
                    if e.type == pygame.KEYUP and e.key == pygame.K_w:
                        morph_up = False
                    if e.type == pygame.KEYUP and e.key == pygame.K_d:
                        morph_right = False
                    if e.type == pygame.KEYUP and e.key == pygame.K_a:
                        morph_left = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                        food = True
                    if e.type == pygame.KEYUP and e.key == pygame.K_e:
                        food = False
                screen.blit(background_image, (0, 0))
                for morph in morphs:
                    morph.update(morph_left,
                                 morph_right,
                                 morph_up,
                                 food,
                                 grave,
                                 enemies)
                for enemy in enemies:
                    enemy.update(hero, grave)
                hero.update(left,
                            right,
                            up,
                            grave,
                            enemies,
                            ending)
                camera.update(hero)
                for e in entities:
                    screen.blit(e.image, camera.apply(e))
                pygame.display.update()

                if hero.rect.y > height:
                    hero.alive = False
                if not hero.alive:
                    death(hero, morphs, grave, enemies)

    return done


def end(done):
    background_image = pygame.image.load("end.png").convert()
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
            screen.blit(background_image, (0, 0))
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Obey Dark Lord")
    bg = pygame.Surface((width, height))
    done = False
    done = screen_saver(done)
    done = main(done)
    end(done)
