import os
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
