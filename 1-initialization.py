# import basic pygame modules
import pygame as pg

# game constants
SCREENRECT = pg.Rect(0, 0, 640, 480)

def main():
    # initialize pygame
    pg.init()
    # set the display mode
    screen = pg.display.set_mode(SCREENRECT.size)
    # initialize clock
    clock = pg.time.Clock()
    # create the background
    background = pg.Surface(SCREENRECT.size)
    screen.blit(background, (0, 0))

    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return

        # draw the scene
        pg.display.update()
        # cap the framerate at 60fps. Also called 60HZ or 60 times per second.
        clock.tick(60)

main()
pg.quit()
