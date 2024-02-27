import os
from typing import List
# import basic pygame modules
import pygame as pg

# game constants
SCREENRECT = pg.Rect(0, 0, 640, 480)

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    # loads an image, prepares it for play
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()

# Each type of game object gets an init and an update function.
# The update function is called once per frame, and it is when each object should
# change its current position and state.
#
# The Player object actually gets a "move" function instead of update,
# since it is passed extra information about the keyboard.

class Player(pg.sprite.Sprite):
    # Representing the player as a moon buggy type car.
    speed = 10
    bounce = 24
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left // self.bounce % 2)

def main():
    # initialize pygame
    pg.init()
    # set the display mode
    screen = pg.display.set_mode(SCREENRECT.size)
    # initialize clock
    clock = pg.time.Clock()
    # create the background, tile the bgd image
    bgdtile = load_image("background.gif")
    background = pg.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()
    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    img = load_image("player1.gif")
    Player.images = [img, pg.transform.flip(img, 1, 0)]

    # Initialize Game Groups
    all = pg.sprite.RenderUpdates()

    # initialize our starting sprites
    player = Player(all)

    while player.alive():
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return

        keystate = pg.key.get_pressed()
        # clear/erase the last drawn sprites
        all.clear(screen, background)
        # update all the sprites
        all.update()
        # handle player input
        direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        player.move(direction)
        # draw the scene
        dirty = all.draw(screen)
        pg.display.update(dirty)
        # cap the framerate at 60fps. Also called 60HZ or 60 times per second.
        clock.tick(60)

main()
pg.quit()
