# Tieu chi: giao dien don gian, than thien, truc quan, de choi, gioi han thoi gian choi <60p !

import random
from time import sleep
import pygame
from sympy import false
from pygame import mixer
pygame.init()
mixer.init()

white = (255, 255, 255)
black = (0, 0, 0)
purple = (172, 172, 255)
light_brown = (230, 204, 179)
brown = (153, 102, 51)
color_list1 = [black, brown]
default_screen = (1720, 760)


class Text:
    def __init__(self, screen, txt, x, y, size, color=black, font='cambria'):
        font = pygame.font.SysFont(font, size)
        text = font.render(txt, True, color)
        screen.blit(text, (x, y))
        pygame.display.update()


class Snake:
    def __init__(self):
        # draw snake with 3 circle:
        pass


class Game:
    def __init__(self, screen):
        # create board, some main contain
        mixer.music.load('Sound/play.mp3')
        mixer.music.play()
        __w = screen.get_width()
        __h = screen.get_height()
        Text(screen, 'Your score: ', __w / 30, __h / 35, 36)
        # ve board
        edge = pygame.draw.rect(screen, brown, (0, __h/10, __w, __h*0.9))
        board = pygame.draw.rect(screen, light_brown, (50, __h/10+50, __w - 100, __h*0.9 -100))
        pygame.display.update()
        sleep(10)

    def Run(self):
        # init the state of game (snake, score, food)
        pass


class Menu:
    def __init__(self):
        scr_size = pygame.display.get_desktop_sizes()
        x = scr_size[0][0] - 60
        y = scr_size[0][1] - 60
        self.screen = pygame.display.set_mode((x, y))
        self.screen.fill(light_brown)
        pygame.display.update()
        pygame.display.set_caption('SNAKE GAME')
        mixer.music.load('Sound/openning.mp3')
        mixer.music.play()

    def button(self, elip, rect, command=None):
        click = pygame.mouse.get_pressed()
        if elip.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.ellipse(self.screen, brown, rect)
            if click[0] and command != None:
                mixer.music.load('Sound/click.wav')
                mixer.music.play()
                pygame.event.wait()
                command()
        else:
            pygame.draw.ellipse(self.screen, white, rect)

    def Show(self):
        w = self.screen.get_width()
        h = self.screen.get_height()
        Text(self.screen, 'SNAKE GAME', w/3 + 70,
             h/10, 60, random.choice(color_list1))

        rect = (w/8, h/4, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.New)
        Text(self.screen, '    START', rect[0] + rect[2]/4,
             rect[1] + rect[3]/3, 30, random.choice(black))

        rect = (w/8, h/2, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, '  SETTING', rect[0] + rect[2] /
             4, rect[1] + rect[3]/3, 30, black)

        rect = (w/8, h / 4 * 3, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, 'HIGH SCORES', rect[0] + rect[2] /
             5, rect[1] + rect[3]/3, 30, black)

        rect = (w/2 + 270, h/4, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, '   RESUME', rect[0] + rect[2] /
             4, rect[1] + rect[3]/3, 30, black)

        rect = (w/2 + 270, h/2, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, 'HOW TO PLAY', rect[0] + rect[2] /
             6, rect[1] + rect[3]/3, 30, black)

        rect = (w/2 + 270, h/4*3, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.Quit)
        Text(self.screen, '  QUIT', rect[0] + rect[2] /
             3, rect[1] + rect[3]/3, 30, black)
        pygame.display.update()

    def New(self):
        # khoi tao game:
        # chay game + luu trang thai game (neu ko bi thua), luu diem cao nhat (neu co)
        self.screen.fill(white)
        pygame.display.update()
        G = Game(self.screen)
        G.Run()

    def Resume(self):
        # khoi phuc trang thai game
        # chay game + luu trang thai game (neu ko bi thua)
        pass

    def HighScore(self):
        # show 5 highest score, day time and scores
        print('')

    def HowTo(self):
        # easy to understand tutorial
        print('')

    def Setting(self):
        # che do sang toi, am thanh...
        pass

    def Quit(self):
        exit()


def main():
    menu = Menu()
    quit_game = False
    while not quit_game:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            menu.Show()
            if event.type == pygame.QUIT:
                quit_game = True
            clock.tick(30)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
