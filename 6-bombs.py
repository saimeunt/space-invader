import os
import random
from typing import List
# import basic pygame modules
import pygame as pg

# game constants
MAX_SHOTS = 2  # most player bullets onscreen
ALIEN_ODDS = 22  # chances a new alien appears
BOMB_ODDS = 60  # chances a new bomb will drop
ALIEN_RELOAD = 12  # frames between new aliens
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
    gun_offset = -11
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
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

    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top

class Alien(pg.sprite.Sprite):
    # An alien space ship. That slowly moves down the screen.

    speed = 13
    animcycle = 12
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % 3]

class Explosion(pg.sprite.Sprite):
    defaultlife = 12
    animcycle = 3
    images: List[pg.Surface] = []

    def __init__(self, actor, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        self.life = self.life - 1
        self.image = self.images[self.life // self.animcycle % 2]
        if self.life <= 0:
            self.kill()

class Shot(pg.sprite.Sprite):
    speed = -11
    images: List[pg.Surface] = []

    def __init__(self, pos, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()

class Bomb(pg.sprite.Sprite):
    speed = 9
    images: List[pg.Surface] = []

    def __init__(self, alien, explosion_group, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=alien.rect.move(0, 5).midbottom)
        self.explosion_group = explosion_group

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 470:
            Explosion(self, self.explosion_group)
            self.kill()

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
    img = load_image("explosion1.gif")
    Explosion.images = [img, pg.transform.flip(img, 1, 1)]
    Alien.images = [load_image(im) for im in ("alien1.gif", "alien2.gif", "alien3.gif")]
    Shot.images = [load_image("shot.gif")]
    Bomb.images = [load_image("bomb.gif")]

    # Initialize Game Groups
    aliens = pg.sprite.Group()
    shots = pg.sprite.Group()
    bombs = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()
    lastalien = pg.sprite.GroupSingle()

    alienreload = ALIEN_RELOAD

    # initialize our starting sprites
    player = Player(all)
    Alien(aliens, all, lastalien) # note, this 'lives' because it goes into a sprite group

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
        firing = keystate[pg.K_SPACE]
        if not player.reloading and firing and len(shots) < MAX_SHOTS:
            Shot(player.gunpos(), shots, all)
        player.reloading = firing
        # Create new alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            Alien(aliens, all, lastalien)
            alienreload = ALIEN_RELOAD
        # Drop bombs
        if lastalien and not int(random.random() * BOMB_ODDS):
            Bomb(lastalien.sprite, all, bombs, all)
        # Detect collisions between aliens and players.
        for alien in pg.sprite.spritecollide(player, aliens, 1):
            Explosion(alien, all)
            Explosion(player, all)
            player.kill()
        # See if shots hit the aliens.
        for alien in pg.sprite.groupcollide(aliens, shots, 1, 1).keys():
            Explosion(alien, all)
        # See if alien bombs hit the player.
        for bomb in pg.sprite.spritecollide(player, bombs, 1):
            Explosion(player, all)
            Explosion(bomb, all)
            player.kill()
        # draw the scene
        dirty = all.draw(screen)
        pg.display.update(dirty)
        # cap the framerate at 60fps. Also called 60HZ or 60 times per second.
        clock.tick(60)

main()
pg.quit()
