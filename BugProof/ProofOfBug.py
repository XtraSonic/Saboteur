import threading
import pygame,sys
from pygame.locals import *

pygame.init()


def exitg():
    pygame.quit()
    sys.exit()


# noinspection PyArgumentList
class test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.windowWidth  = 800
        self.windowHeight = 480
        self.fontsize     = 20
        self.screen       = pygame.display.set_mode((self.windowWidth,self.windowHeight))
        self.background   = pygame.Surface(self.screen.get_size())
        self.background   = self.background.convert()
        cellsize     = 32
        nrcellsH     = self.windowHeight/cellsize-1
        self.background2  = pygame.Surface((self.windowWidth,cellsize))
        self.background2  = self.background2.convert()
        self.background.blit(self.background2,(0,(nrcellsH-1)*cellsize),self.background2.get_rect())
        pygame.display.set_caption('Tresure Hunt - WSU EDITION')
        self.font = pygame.font.SysFont("Times New Roman", self.fontsize + 35)
        text = self.font.render("Alege rezolutia:", True, (255, 255, 255))
        textpos = text.get_rect(centerx=self.windowWidth / 2, centery=1.5 * self.windowHeight / 8)
        self.screen.blit(text, textpos)

        self.font = pygame.font.SysFont("Times New Roman", self.fontsize + 20)
        rez1txt = self.font.render("800x480", True, (255, 255, 255))
        self.rez1pos = rez1txt.get_rect(centerx=self.windowWidth / 2, centery=3 * self.windowHeight / 8)
        self.screen.blit(rez1txt, self.rez1pos)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():

                # ---------------------------------------------------------------------------------------------------------------- Exit Game Buttons

                if event.type == QUIT:
                    exitg()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    exitg()

                # ---------------------------------------------------------------------------------------------------------------------- Menu Buttons

                pos = pygame.mouse.get_pos()

                if self.rez1pos.collidepoint(pos) and event.type == MOUSEBUTTONDOWN:
                    self.font = pygame.font.SysFont("Times New Roman", self.fontsize + 20)
                    rez1txt = self.font.render("800x480", True, (150, 150, 150))
                    self.screen.blit(rez1txt, self.rez1pos)
                    pygame.display.flip()
                    while not event.type == MOUSEBUTTONUP:
                        event = pygame.event.poll()
                    pos = pygame.mouse.get_pos()
                    if self.rez1pos.collidepoint(pos):
                        # -----------------------------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        pass
                    else:
                        self.font = pygame.font.SysFont("Times New Roman", self.fontsize + 20)
                        rez1txt = self.font.render("800x480", True, (255, 255, 255))
                        self.screen.blit(rez1txt, self.rez1pos)
                        pygame.display.flip()



t = test()
t.run()  # run makes the screen function, but does not start a new thread (we don`t get to ok)
# t.start()  # start (without run before it) makes the new thread, but the window becomes unresponsive
             # (we get to ok, but the window doesn`t work
while True:
    print("OK")